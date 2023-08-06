# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import sys

from distributed.scheduler import KilledWorker
from dask.distributed import Client, LocalCluster

from s1tiling.libs.S1FileManager import S1FileManager
# from libs import S1FilteringProcessor
from s1tiling.libs import Utils
from s1tiling.libs.configuration import Configuration
from s1tiling.libs.otbpipeline import FirstStep, PipelineDescriptionSequence
from s1tiling.libs.otbwrappers import AnalyseBorders, Calibrate, CutBorders, OrthoRectify, Concatenate, BuildBorderMask, SmoothBorderMask
from s1tiling.libs import exits
from s1tiling.libs.vis import SimpleComputationGraph

logger = None
# logger = logging.getLogger('s1tiling')


def remove_files(files):
    """
    Removes the files from the disk
    """
    logger.debug("Remove %s", files)
    for file_it in files:
        if os.path.exists(file_it):
            os.remove(file_it)


def extract_tiles_to_process(cfg, s1_file_manager):
    """
    Deduce from the configuration all the tiles that need to be processed.
    """
    tiles_to_process = []

    all_requested = False

    for tile in cfg.tile_list:
        if tile == "ALL":
            all_requested = True
            break
        elif True:  # s1_file_manager.tile_exists(tile):
            tiles_to_process.append(tile)
        else:
            logger.info("Tile %s does not exist, skipping ...", tile)
    logger.info('Requested tiles: %s', cfg.tile_list)

    # We can not require both to process all tiles covered by downloaded products
    # and and download all tiles

    if all_requested:
        if cfg.download and "ALL" in cfg.roi_by_tiles:
            logger.critical("Can not request to download 'ROI_by_tiles : ALL' if 'Tiles : ALL'."
                    + " Change either value or deactivate download instead")
            sys.exit(exits.CONFIG_ERROR)
        else:
            tiles_to_process = s1_file_manager.get_tiles_covered_by_products()
            logger.info("All tiles for which more than %s%% of the surface is covered by products will be produced: %s",
                    100 * cfg.TileToProductOverlapRatio, tiles_to_process)

    return tiles_to_process


def check_tiles_to_process(tiles_to_process, s1_file_manager):
    """
    Search the SRTM tiles required to process the tiles to process.
    """
    needed_srtm_tiles = []
    tiles_to_process_checked = []  # TODO: don't they exactly match tiles_to_process?

    # Analyse SRTM coverage for MGRS tiles to be processed
    srtm_tiles_check = s1_file_manager.check_srtm_coverage(tiles_to_process)

    # For each MGRS tile to process
    for tile in tiles_to_process:
        logger.info("Check SRTM coverage for %s", tile)
        # Get SRTM tiles coverage statistics
        srtm_tiles = srtm_tiles_check[tile]
        current_coverage = 0
        current_needed_srtm_tiles = []
        # Compute global coverage
        for (srtm_tile, coverage) in srtm_tiles:
            current_needed_srtm_tiles.append(srtm_tile)
            current_coverage += coverage
        # If SRTM coverage of MGRS tile is enough, process it
        needed_srtm_tiles += current_needed_srtm_tiles
        tiles_to_process_checked.append(tile)
        if current_coverage < 1.:
            logger.warning("Tile %s has insuficient SRTM coverage (%s%%)",
                    tile, 100 * current_coverage)

    # Remove duplicates
    needed_srtm_tiles = list(set(needed_srtm_tiles))
    return tiles_to_process_checked, needed_srtm_tiles


def check_srtm_tiles(cfg, srtm_tiles_id, srtm_suffix='.hgt'):
    """
    Check the SRTM tiles exist on disk.
    """
    res = True
    for srtm_tile in srtm_tiles_id:
        tile_path_hgt = Path(cfg.srtm, srtm_tile + srtm_suffix)
        if not tile_path_hgt.exists():
            res = False
            logger.critical("%s is missing!", tile_path_hgt)
    return res


def clean_logs(config, nb_workers):
    """
    Clean all the log files.
    Meant to be called once, at startup
    """
    filenames = []
    for _, cfg in config['handlers'].items():
        if 'filename' in cfg and '%' in cfg['filename']:
            pattern = cfg['filename'] % ('worker-%s',)
            filenames += [pattern%(w,) for w in range(nb_workers)]
    remove_files(filenames)


def setup_worker_logs(config, dask_worker):
    """
    Set-up the logger on Dask Worker.
    """
    d_logger = logging.getLogger('distributed.worker')
    r_logger = logging.getLogger()
    old_handlers = d_logger.handlers[:]

    for _, cfg in config['handlers'].items():
        if 'filename' in cfg and '%' in cfg['filename']:
            cfg['mode']     = 'a'  # Make sure to not reset worker log file
            cfg['filename'] = cfg['filename'] % ('worker-' + str(dask_worker.name),)

    logging.config.dictConfig(config)
    # Restore old dask.distributed handlers, and inject them in root handler as well
    for hdlr in old_handlers:
        d_logger.addHandler(hdlr)
        r_logger.addHandler(hdlr)  # <-- this way we send s1tiling messages to dask channel

    # From now on, redirect stdout/stderr messages to s1tiling
    Utils.RedirectStdToLogger(logging.getLogger('s1tiling'))


def process_one_tile(
        tile_name, tile_idx, tiles_nb,
        s1_file_manager, pipelines, client,
        searched_items_per_page,
        debug_otb=False, dryrun=False, do_watch_ram=False, debug_tasks=False):
    """
    Process one S2 tile.

    I.E. run the OTB pipeline on all the S1 images that match the S2 tile.
    """
    s1_file_manager.ensure_tile_workspaces_exist(tile_name)

    logger.info("Processing tile %s (%s/%s)", tile_name, tile_idx + 1, tiles_nb)

    s1_file_manager.keep_X_latest_S1_files(1000)

    try:
        with Utils.ExecutionTimer("Downloading images related to " + tile_name, True):
            s1_file_manager.download_images(tiles=tile_name,
                    searched_items_per_page=searched_items_per_page, dryrun=dryrun)
    except BaseException as e:
        logger.exception('Cannot download S1 images associated to %s', tile_name)
        sys.exit(exits.DOWNLOAD_ERROR)

    with Utils.ExecutionTimer("Intersecting raster list w/ " + tile_name, True):
        intersect_raster_list = s1_file_manager.get_s1_intersect_by_tile(tile_name)

    if len(intersect_raster_list) == 0:
        logger.info("No intersection with tile %s", tile_name)
        return []

    dsk, required_products = pipelines.generate_tasks(tile_name, intersect_raster_list,
            debug_otb=debug_otb, dryrun=dryrun, do_watch_ram=do_watch_ram)
    logger.debug('Summary of tasks related to S1 -> S2 transformations of %s', tile_name)
    results = []
    if debug_otb:
        for product, how in reversed(dsk):
            logger.debug('- task: %s <-- %s', product, how)
        logger.info('Executing tasks one after the other for %s (debugging OTB)', tile_name)
        for product, how in reversed(dsk):
            logger.info('- execute: %s <-- %s', product, how)
            if not issubclass(type(how), FirstStep):
                results += [how[0](*list(how)[1:])]
        return results
    else:
        for product, how in dsk.items():
            logger.debug('- task: %s <-- %s', product, how)

        if debug_tasks:
            SimpleComputationGraph().simple_graph(
                    dsk,
                    filename='tasks-%s-%s.svg' % (tile_idx + 1, tile_name))
        logger.info('Start S1 -> S2 transformations for %s', tile_name)
        nb_tries = 2
        for run in range(1, nb_tries+1):
            try:
                results = client.get(dsk, required_products)
                return results
            except KilledWorker as e:
                logger.critical('%s', dir(e))
                logger.exception("Worker %s has been killed when processing %s on %s tile: (%s). Workers will be restarted: %s/%s",
                        e.last_worker.name, e.task, tile_name, e, run, nb_tries)
                # TODO: don't overwrite previous logs
                # And we'll need to use the synchronous=False parameter to be able to check successful executions
                # but then, how do we clean up futures and all??
                client.restart()
                # Update the list of remaining tasks
                if run < nb_tries:
                    dsk, required_products = pipelines.generate_tasks(tile_name, intersect_raster_list,
                            debug_otb=debug_otb, dryrun=dryrun, do_watch_ram=do_watch_ram)
                else:
                    raise


# Main code
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option()
@click.option(
        "--cache-before-ortho/--no-cache-before-ortho",
        is_flag=True,
        default=False,
        help="""Force to store Calibration|Cutting result on disk before orthorectorectification.

        BEWARE, this option will produce temporary files that you'll need to explicitely delete.""")
@click.option(
        "--searched_items_per_page",
        default=20,
        help="Number of products simultaneously requested by eodag"
        )
@click.option(
        "--dryrun",
        is_flag=True,
        help="Display the processing shall would be realized, but none is done.")
@click.option(
        "--debug-otb",
        is_flag=True,
        help="Investigation mode were OTB Applications are directly used without Dask in order to run them through gdb for instance.")
@click.option(
        "--watch-ram",
        is_flag=True,
        help="Trigger investigation mode for watching memory usage")
@click.option(
        "--graphs", "debug_tasks",
        is_flag=True,
        help="Generate SVG images showing task graphs of the processing flows")
@click.argument('config_filename', type=click.Path(exists=True))
def main(searched_items_per_page, dryrun, debug_otb, watch_ram, debug_tasks, cache_before_ortho, config_filename):
    """
      On demand Ortho-rectification of Sentinel-1 data on Sentinel-2 grid.

      It performs the following steps:
      1. Download S1 images from S1 data provider (through eodag)
      2. Calibrate the S1 images to gamma0
      3. Orthorectify S1 images and cut their on geometric tiles
      4. Concatenate images from the same orbit on the same tile
      5. Build mask files

      Parameters have to be set by the user in the S1Processor.cfg file
    """
    config = Configuration(config_filename)
    os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = str(config.OTBThreads)
    global logger
    logger = logging.getLogger('s1tiling')
    with S1FileManager(config) as s1_file_manager:
        tiles_to_process = extract_tiles_to_process(config, s1_file_manager)
        if len(tiles_to_process) == 0:
            logger.critical("No existing tiles found, exiting ...")
            sys.exit(exits.NO_S2_TILE)

        tiles_to_process_checked, needed_srtm_tiles = check_tiles_to_process(tiles_to_process, s1_file_manager)

        logger.info("%s images to process on %s tiles",
                s1_file_manager.nb_images, tiles_to_process_checked)

        if len(tiles_to_process_checked) == 0:
            logger.critical("No tiles to process, exiting ...")
            sys.exit(exits.NO_S1_IMAGE)

        logger.info("Required SRTM tiles: %s", needed_srtm_tiles)

        if not check_srtm_tiles(config, needed_srtm_tiles):
            logger.critical("Some SRTM tiles are missing, exiting ...")
            sys.exit(exits.MISSING_SRTM)

        if not os.path.exists(config.GeoidFile):
            logger.critical("Geoid file does not exists (%s), exiting ...", config.GeoidFile)
            sys.exit(exits.MISSING_GEOID)

        # Prepare directories where to store temporary files
        # These directories won't be cleaned up automatically
        S1_tmp_dir = os.path.join(config.tmpdir, 'S1')
        os.makedirs(S1_tmp_dir, exist_ok=True)

        config.tmp_srtm_dir = s1_file_manager.tmpsrtmdir(needed_srtm_tiles)

        pipelines = PipelineDescriptionSequence(config)
        if cache_before_ortho:
            pipelines.register_pipeline([AnalyseBorders, Calibrate, CutBorders], 'PrepareForOrtho', product_required=False)
            pipelines.register_pipeline([OrthoRectify],                          'OrthoRectify',    product_required=False)
        else:
            pipelines.register_pipeline([AnalyseBorders, Calibrate, CutBorders, OrthoRectify], 'FullOrtho', product_required=False)

        pipelines.register_pipeline([Concatenate],                                              product_required=True)
        if config.mask_cond:
            pipelines.register_pipeline([BuildBorderMask, SmoothBorderMask], 'GenerateMask',    product_required=True)

        # filtering_processor = S1FilteringProcessor.S1FilteringProcessor(config)

        if not debug_otb:
            clean_logs(config.log_config, config.nb_procs)
            cluster = LocalCluster(threads_per_worker=1, processes=True, n_workers=config.nb_procs, silence_logs=False)
            client = Client(cluster)
            client.register_worker_callbacks(lambda dask_worker: setup_worker_logs(config.log_config, dask_worker))
        else:
            client = None

        log_level = lambda res: logging.INFO if bool(res) else logging.WARNING
        results = []
        for idx, tile_it in enumerate(tiles_to_process_checked):
            with Utils.ExecutionTimer("Processing of tile " + tile_it, True):
                res = process_one_tile(
                        tile_it, idx, len(tiles_to_process_checked),
                        s1_file_manager, pipelines, client,
                        searched_items_per_page=searched_items_per_page,
                        debug_otb=debug_otb, dryrun=dryrun, do_watch_ram=watch_ram, debug_tasks=debug_tasks)
                results += res

        nb_error_detected = 0
        for res in results:
            if not bool(res):
                nb_error_detected += 1

        if nb_error_detected > 0:
            logger.warning('Execution report: %s errors detected', nb_error_detected)
        else:
            logger.info('Execution report: no error detected')

        if results:
            for res in results:
                logger.log(log_level(res), ' - %s', res)
        else:
            logger.info(' -> Nothing has been executed')

        if nb_error_detected > 0:
            sys.exit(exits.TASK_FAILED)


import ntpath
import shutil

import boto3
import botocore


def get_s3_data(s1_product_url):

    s3_data = s1_product_url.replace('s3://', '').split('/')
    bucket_name = s3_data[0]
    prefix = '/'.join(s3_data[1:-1])
    s3_file = s3_data[-1]
    return bucket_name, prefix, s3_file

def download_s3_file(s3_client, s3_file_url, bucket_name="", prefix="", type="", dst_dir="."):
        
    s3_file = ""
    if bucket_name and prefix:
        _, _, s3_file = get_s3_data(s3_file_url)
    else:
        bucket_name, prefix, s3_file = get_s3_data(s3_file_url)

    logger.debug("Working on bucket '" + bucket_name + "', prefix '" + prefix + "', s3_file '" + s3_file + "'")

    dst_dir_path = os.path.abspath(dst_dir)
    s3_file_path = os.path.join(dst_dir_path, s3_file)
    logger.debug("s3_file_path = {} | dst_dir_path = {}".format(s3_file_path, dst_dir_path))
    
    if os.path.isdir(s3_file_path): # The product dir already exists
        logger.info("Dir '" + s3_file_path + "' already exists")
        return s3_file, s3_file_path

    if os.path.isfile(s3_file_path): # The hgt file already exists
        logger.info("File '" + s3_file_path + "' already exists")
        return s3_file, s3_file_path
    logger.info("Creating local dest dir: {}".format(dst_dir_path))                
    os.makedirs(dst_dir_path, exist_ok=True)
    logger.debug("bucket_name ={}| s3_file ={}| s3_file_url={}".format(bucket_name, s3_file, s3_file_url))
    try:
        s3_object_files = [f['Key'] for f in s3_client.list_objects_v2(Bucket=bucket_name,
            Prefix=prefix + "/" + s3_file,
            MaxKeys=100,
            RequestPayer='requester')['Contents']]
    except Exception as e:
        logger.error("list_objects_v2 exception :{}".format(e))
        return None, None
    logger.debug("s3_object_files = {}".format(s3_object_files))
    for s3_object_file in s3_object_files:
        s3_file_tree = s3_object_file.replace(prefix + "/", "")
        if len(s3_file_tree) == 0:
            continue
        logger.debug("s3_file_tree: {}".format(s3_file_tree))                
        #if type == "s1_product":
        #    filename = os.path.join(dst_dir_path, "{}/{}.SAFE{}".format(s3_file, s3_file, s3_file_tree.replace(s3_file, "")))
        #else:
        filename = os.path.join(dst_dir_path, s3_file_tree)
        logger.debug("filename: {}".format(filename))                

        # create dirs tree if necessary
        dirname = os.path.dirname(filename)
        if dirname != dst_dir_path:
            logger.debug("Creating directory: {}".format(dirname))                
            os.makedirs(dirname, exist_ok=True)

        # Downloads file
        logger.debug("function download_file")
        s3_client.download_file(Bucket=bucket_name, Key=s3_object_file, Filename=filename, ExtraArgs=dict(RequestPayer='requester'))

    return s3_file, s3_file_path

def get_s3_client():
    client_config = botocore.config.Config(max_pool_connections=100)
    s3_client = None
    if "amazon" in os.environ["S3_ENDPOINT"]:
        s3_client = boto3.client('s3',
            aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
            region_name="eu-central-1",
            config=client_config)
    if "cloudferro" in os.environ["S3_ENDPOINT"]:
        s3_client = boto3.client('s3',
            aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
            endpoint_url=os.environ["S3_ENDPOINT"],
            config=client_config)
    
    return s3_client

# TODO: update to Path
def get_filename_only(task_file):
    path, filename = ntpath.split(task_file)
    return filename or ntpath.basename(path)

def generate_s1_ard(s1_prd_filepath, s2_tile_id, output_rootpath):
    
    # => Configures logger
    logFormatter = logging.Formatter('[%(asctime)-20s] [%(name)-10s] [%(levelname)-6s] %(message)s')
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.propagate = True
    
    logger = logging.getLogger('world-cereal')
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.addHandler(consoleHandler)
    log_filename = None
    s3_log_filename = None

    root_dir = "/data/"
    input_dir = "/data"
    s1_preprocess_dir = root_dir + "out/"
    s1_tiling_s3_output_dir = os.environ["OUTPUT_DIRECTORY"]
    s1_input_dir = input_dir
    hgt_input_dir = os.path.join(input_dir, "srtm/")
    success_dir = s1_preprocess_dir + "success/"
    bucket_succes_dir_prefix = success_dir.lstrip(root_dir)
    error_dir = s1_preprocess_dir + "error/"
    log_dir = s1_preprocess_dir + s1_tiling_s3_output_dir + "log_s1tiling/workflow/"
    log_dir_products = s1_preprocess_dir + s1_tiling_s3_output_dir + "log_s1tiling/products/"

    task_file = "{{inputs.parameters.scheduled-tasks-file}}"
            
    # Set log file
    executor_name = get_filename_only(task_file).replace(".txt", "")
    log_filename = "./" + executor_name + "_" + time.strftime("%Y%m%d_%H%M%S") + "_" + os.environ["CURRENT_NODE_NAME"] + ".log"
    s3_log_filename = log_dir.lstrip(s1_preprocess_dir) + log_filename.replace("./", "")
    fileHandler = logging.FileHandler(log_filename)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    logger.info("=> Enter script...")
    #logger.info("Tasks file name: {}. Executed on node: {} ".format(task_file, os.environ["CURRENT_NODE_NAME"]))

    s3_client = get_s3_client()
    if s3_client is None:
        logger.debug("Could not get the handler for s3 bucket endpoint")
        sys.exit(-1)

    # Retrieve dem files
    try:
        logger.info("Downloading hgt files from s3://world-cereal/srtm_test/ to {}".format(hgt_input_dir))
        # Change path to dem hgt s3 on creodias or aws ?
        download_s3_file(s3_client, "s3://world-cereal/srtm_test/", type="hgt", dst_dir=hgt_input_dir)
    except Exception as e:
        logger.error("Exception when downloading hgt files: {}".format(e))
        logger.critical("Error while downloading the hgt files from s3://world-cereal/srtm_test/ The workflow can't continue without these file, exit... ")
        sys.exit(-1)

    logger.info("Downloaded HGT files: {}".format(os.listdir(hgt_input_dir)))

    # Creates file tree
    shutil.rmtree(s1_preprocess_dir, ignore_errors=True)
    logger.debug("Creating s1_preprocess_dir :{}".format(s1_preprocess_dir))
    os.makedirs(s1_preprocess_dir, exist_ok=True)

    # build the path to s3 bucket:
    s3_dir_base = os.path.join(s1_tiling_s3_output_dir, "SAR", s2_tile.s2_tile_name[:2], s2_tile.s2_tile_name[2], s2_tile.s2_tile_name[3:])                
    products = s2_tile.s1_products.split(",")
    logger.info("Total number of products to process:{}".format(len(products)))

    underscore_split = s1_product.split("_")
    if len(underscore_split) != S1_PRODUCT_FIELDS_NUMBER:
        logger.error("Failed to check product name {}".format(s1_product))
        logger.info("Updating database status for {} to error.".format(s2_tile.s2_tile_name))
        S2Tile.update_status(db_index, "error")
        logger.info("Trying to continue with the next S1 products.")
        continue
    # get the year                  
    year, month, day = get_year_month_day_from_str(underscore_split[4])
    unique_id = "{}{}{}".format(underscore_split[6], underscore_split[7], underscore_split[8])
    last_level_dir = "{}_{}_ORBDIR_RELORB_{}_{}".format(underscore_split[0], underscore_split[4], unique_id, s2_tile.s2_tile_name)
    yyyymmdd = "{}{}{}".format(year, month, day)
    s3_dir = os.path.join(s3_dir_base, year, yyyymmdd, last_level_dir)
    logger.debug("s3_dir = {}".format(s3_dir))
    if get_products_for_creodias(s1_product, input_dir, "/eodata/Sentinel-1/SAR/GRD", logger) is False:
        logger.error("Error while downloading data for S1 product '{}'. Exception: {}. Traceback: {}".format(s1_product, e, tb))
        logger.info("Updating database status for {} to error.".format(s1_product))
        S2Tile.update_status(db_index, "error")
        logger.info("EXIT.")
        sys.exit(-1)

    logger.info("Creating the pre-process directory {}".format(s1_preprocess_dir))
    os.makedirs(s1_preprocess_dir, exist_ok=True)

    # modify the input configuration file
    cfg_file_name = os.path.join(input_dir, "S1Processor.cfg")
    shutil.copyfile("/opt/s1tiling-venv/s1processor_config/S1Processor.cfg", cfg_file_name)         
    with fileinput.FileInput(cfg_file_name, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("tile_to_be_processed", "tiles : {}".format(s2_tile.s2_tile_name)), end='')

    full_s1_preprocess_dir = os.path.join(s1_preprocess_dir, s2_tile.s2_tile_name) + "/"
    try:
        cmd = "/opt/entrypoint.sh {}".format(cfg_file_name)
      
        logger.info("Starting the execution of s1 tiling processor with cmd : '" + str(cmd) + "'")

        process = subprocess.run(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        processor_output = format_string(process.stdout)
        logger.debug("Output : " + processor_output)

        if len(processor_output) > 0 and "INFO -  - Failed to produce" in processor_output:
            status = "uncomplete"

    except subprocess.CalledProcessError as e:
        logger.error("Failed to execute command '" + str(e.cmd) + "'")

    # uploading the result                    
    uploading_error, tif_files_number, total_output_size = recursive_upload_dir_to_s3(s3_client, full_s1_preprocess_dir, s3_dir, BUCKET_NAME, logger)       
    # handling upload error, will try to process the next s1 product
    total_tif_files_number += tif_files_number
    logger.info("Finished uploading the results for {}. Total size: {}".format(s2_tile.s2_tile_name, total_output_size))
    total_uploaded_size += total_output_size 
    
    logger.info("Deleting the product directory {}".format(os.path.join(input_dir, s1_product)))
    shutil.rmtree(os.path.join(input_dir, s1_product), ignore_errors=True)
    logger.info("Deleting the process directory {}".format(s1_preprocess_dir))
    shutil.rmtree(s1_preprocess_dir, ignore_errors=True)
     
def build_parser():
    '''Creates a parser suitable for parsing a command line invoking this program.

    :return: An parser.
    :rtype: :class:`argparse.ArgumentParser`
    '''
    parser = ArgumentParser()
    parser.add_argument("s1_product_filepath", type=Path, help="Sentinel 1 product filepath")
    parser.add_argument("s2_tile_id", type=str, help="Sentinel 2 MGRS tile id")
    parser.add_argument("output_dirpath", help="Output directory")
    parser.add_argument("--working_dirpath", "-w", help="Working directory")
    
    return parser

def main(arguments=None):
    '''
    Command line interface to perform S1 pre processing for EWoC

    :param list arguments: list of arguments
    '''

    arg_parser = build_parser()

    args = arg_parser.parse_args(args=arguments)

    generate_s1_ard(args.args.s1_product_filepath, args.args.s2_tile_id, args.args.output_dirpath)

if __name__ == '__main__':  # Required for Dask: https://github.com/dask/distributed/issues/2422
    sys.exit(main())

