import time, os
import random, json
from helpers.helper import helper
from helpers.helper import config_values
from helpers.hamilton import hamilton_ui

class mbd_wash:
    helper = helper()
    hamilton_ui = hamilton_ui()

    def __init__(self, logger):
        self.logger = logger

    def mbd_wash_workflow(self,logger,number_of_batches):

        ple_plate_id = helper.create_ple_plate_id(self,logger)
        helper.update_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file,
                                           'cfdna_extraction_ex_elution_plate_barcode', ple_plate_id)
        hamilton_star = helper.add_hamilton_start_in_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file)
        logger.info(f"hamilton_star:::{config_values.instrument_serial_number}")
        time.sleep(2)
        archive_path = os.path.join(config_values.e2e_folder_path, 'Archive.zip')
        helper.archive_zip_file(self,logger,config_values.e2e_folder_path, archive_path)
        variables_from_response = helper.process_samples_new(self,logger,config_values.host, config_values.username, config_values.password,
                                               config_values.stop_at_mbd_wash, archive_path)
        variables = json.loads(variables_from_response.replace("'", "\""))
        logger.info(f"variable:::::{variables}")
        helper.abort_instrument_job_for_started_state(self, logger, config_values.host, config_values.username,config_values.password, config_values.instrument_serial_number)
        helper.abort_instrument_job_for_assigned_state(self, logger, config_values.host, config_values.username,config_values.password, config_values.instrument_serial_number)
        workflow_id = helper.get_workflow_id(self,logger,config_values.host,config_values.username,config_values.password)
        logger.info(f"workflow_id:::::{workflow_id}")

        latest_operation_id = helper.get_reponse_from_pipeline_runs(self,logger,config_values.host,config_values.username,
                                                                       config_values.password, config_values.mbd_setup_tramstop)
        pipeline_id = helper.get_pipeline_id(self,logger,config_values.host,config_values.username,config_values.password)
        node_id = helper.get_node_id(self,logger,config_values.host, config_values.username, config_values.password,
                                     pipeline_id, "MBD Wash")
        helper.post_api_for_starting_workflow(self,logger,config_values.host,config_values.username,config_values.password,
                                              pipeline_id,node_id,config_values.instrument_type,config_values.instrument_serial_number)
        time.sleep(20)
        hamilton_ui.click_on_simulation_mode_ok_button(self)
        time.sleep(3)
        hamilton_ui.check_options_on_the_window(self, ["No Wait","No Pipetting","Stoppable Timers"])
        hamilton_ui.enter_username_and_batchid(self,number_of_batches)
        hamilton_ui.click_on_method_start_ok_button(self)
        barcodes_mbd_wash_mw1_buffer_plate = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username, config_values.password,variables.get('mbd_wash_mw1_buffer_plate_lot_number'))
        random_number = random.randint(10000, 99999)
        DWT_plate_id1 = config_values.dwt_plate_id + str(random_number)
        random_number = random.randint(10000, 99999)
        DWT_plate_id2 = config_values.dwt_plate_id + str(random_number)
        barcodes_mbd_wash_mw3_buffer_plate = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username,
                                                              config_values.password,variables.get('mbd_wash_mw3_buffer_plate_lot_number'))
        barcodes_for_mbd_dwe_plate_ = helper.get_plates_for_completed_instrument_job(self, logger, config_values.host,
                                                                       config_values.username, config_values.password,
                                                                       'MBD Plate')
        if number_of_batches == "1":
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_wash_load1_deck_setup)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar2,texts_to_enter=[barcodes_mbd_wash_mw1_buffer_plate[0],
                                                                barcodes_for_mbd_dwe_plate_[0], DWT_plate_id1,config_values.nocode,
                                                                barcodes_mbd_wash_mw3_buffer_plate[0]])
        else:
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_wash_load2_deck_setup)
            time.sleep(5)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar3,texts_to_enter=[barcodes_mbd_wash_mw1_buffer_plate[0],
                                                                 barcodes_for_mbd_dwe_plate_[0], config_values.nocode,config_values.nocode, barcodes_mbd_wash_mw3_buffer_plate[0]])
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar2,texts_to_enter=[barcodes_mbd_wash_mw1_buffer_plate[1],
                                                                 barcodes_for_mbd_dwe_plate_[1], DWT_plate_id1, DWT_plate_id2, barcodes_mbd_wash_mw3_buffer_plate[1]])
        helper.check_if_method_is_complete(self,logger, config_values.host, config_values.username,config_values.password)