import time, os
import random, json
from helpers.helper import helper
from helpers.helper import config_values
from helpers.hamilton import hamilton_ui

class mbd_setup:
    helper = helper()
    hamilton_ui = hamilton_ui()

    def __init__(self, logger):
        self.logger = logger

    def mbd_setup_workflow(self,logger,number_of_batches):
        ple_plate_id = helper.create_ple_plate_id(self,logger)
        helper.update_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file,
                                           'cfdna_extraction_ex_elution_plate_barcode', ple_plate_id)
        hamilton_star = helper.add_hamilton_start_in_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file)
        logger.info(f"hamilton_star:::{config_values.instrument_serial_number}")
        time.sleep(2)
        archive_path = os.path.join(config_values.e2e_folder_path, 'Archive.zip')
        helper.archive_zip_file(self,logger,config_values.e2e_folder_path, archive_path)
        variables_from_response = helper.process_samples_new(self,logger,config_values.host, config_values.username, config_values.password,
                                               config_values.stop_at_mbd_setup, archive_path)
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
                                     pipeline_id, "MBD Setup")
        helper.post_api_for_starting_workflow(self,logger,config_values.host,config_values.username,config_values.password,
                                              pipeline_id,node_id,config_values.instrument_type,config_values.instrument_serial_number)
        time.sleep(20)
        hamilton_ui.click_on_simulation_mode_ok_button(self)
        time.sleep(3)
        hamilton_ui.check_options_on_the_window(self, ["No Wait","No Pipetting","Stoppable Timers"])
        hamilton_ui.enter_username_and_batchid(self,number_of_batches)
        hamilton_ui.click_on_method_start_ok_button(self)
        barcodes_mbb_plate_id = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username, config_values.password,variables.get('mbd_setup_bead_tube_lot_number'))
        random_number = random.randint(10000, 99999)
        DWE_plate_id1 = config_values.dwe_plate_id + str(random_number)
        random_number = random.randint(10000, 99999)
        DWE_plate_id2 = config_values.dwe_plate_id + str(random_number)
        barcodes_mbp_plate_id = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username,
                                                              config_values.password,variables.get('mbd_setup_buffer_plate_lot_number'))
        barcodes_epc_plate_id = helper.get_plate_from_control_lots(self, logger, config_values.host,config_values.username, config_values.password,
                                                                   variables.get('mbd_setup_positive_control_lot_number'))
        barcodes_fcr_plate_id = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username,
                                                              config_values.password, variables.get('mbd_setup_carrier_plate_lot_number'))
        if number_of_batches == "1":
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_setup_load11_deck_setup)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_tube1, texts_to_enter=[config_values.nocode, config_values.nocode, barcodes_mbb_plate_id[0], config_values.nocode,
                                                                config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode, config_values.nocode,
                                                                config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode, config_values.nocode,
                                                                config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,config_values.nocode,
                                                                config_values.nocode,config_values.nocode,config_values.nocode])
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_pltCar3, texts_to_enter=[config_values.nocode,DWE_plate_id1, config_values.nocode, barcodes_mbp_plate_id[0],config_values.nocode])
            hamilton_ui.enter_value_on_bulk_reagent_scan_window(self, variables.get('mbd_setup_mbd_protein_tube_lot_1_number'))
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_setup_load12_deck_setup)
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_tube1,texts_to_enter=[barcodes_epc_plate_id[0],config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode,config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode])
            output_plates = helper.get_plates_for_completed_instrument_job(self, logger, config_values.host,config_values.username,config_values.password, 'BE Elution Plate')
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar2, texts_to_enter=[config_values.nocode,barcodes_fcr_plate_id[0], config_values.nocode,
                                                                 output_plates[0],config_values.nocode])
        else:
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_setup_load21_deck_setup)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_tube1,
                                                 texts_to_enter=[config_values.nocode, config_values.nocode, barcodes_mbb_plate_id[0], config_values.nocode,
                                                                 config_values.nocode, barcodes_mbb_plate_id[1],config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode,config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode,config_values.nocode])
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar3,texts_to_enter=[config_values.nocode, DWE_plate_id1, DWE_plate_id2, barcodes_mbp_plate_id[0], barcodes_mbp_plate_id[1]])
            hamilton_ui.enter_value_on_bulk_reagent_scan_window(self, variables.get('mbd_setup_mbd_protein_tube_lot_1_number'))
            hamilton_ui.enter_value_on_bulk_reagent_scan_window(self, variables.get('mbd_setup_mbd_protein_tube_lot_2_number'))
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_mbd_setup_load22_deck_setup)
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_tube1,texts_to_enter=[barcodes_epc_plate_id[0], config_values.nocode,
                                                                 config_values.nocode, barcodes_epc_plate_id[1], config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode,
                                                                 config_values.nocode, config_values.nocode, config_values.nocode, config_values.nocode])
            output_plates = helper.get_plates_for_completed_instrument_job(self, logger, config_values.host, config_values.username,config_values.password, 'BE Elution Plate')
            hamilton_ui.enter_simulated_barcodes(self, logger, config_values.window_name_pltCar2,texts_to_enter=[config_values.nocode, barcodes_fcr_plate_id[0],
                                                                 barcodes_fcr_plate_id[1], output_plates[0], output_plates[1]])
        helper.check_if_method_is_complete(self,  logger, config_values.host, config_values.username, config_values.password)