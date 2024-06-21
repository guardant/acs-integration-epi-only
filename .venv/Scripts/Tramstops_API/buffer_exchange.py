import string, time, requests, os, yaml, shutil, zipfile
import csv,re, random, ruamel.yaml, json
from helper import helper
from helper import config_values
from hamilton import hamilton_ui

class buffer_exchange:
    helper = helper()
    hamilton_ui = hamilton_ui()

    def __init__(self, logger):
        self.logger = logger

    def buffer_exchange_workflow(self,logger,number_of_batches):
        helper.abort_instrument_job_for_started_state(self,logger,config_values.host, config_values.username, config_values.password,config_values.instrument_serial_number)
        helper.abort_instrument_job_for_assigned_state(self,logger,config_values.host, config_values.username,
                                                      config_values.password,
                                                      config_values.instrument_serial_number)
        ple_plate_id = helper.create_ple_plate_id(self,logger)
        helper.update_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file,
                                           'cfdna_extraction_ex_elution_plate_barcode', ple_plate_id)
        hamilton_star = helper.add_hamilton_start_in_artifacts_yaml_file(self,logger,config_values.artifacts_yaml_file)
        logger.info(f"hamilton_star:::{config_values.instrument_serial_number}")
        time.sleep(2)
        archive_path = os.path.join(config_values.e2e_folder_path, 'Archive.zip')
        helper.archive_zip_file(self,logger,config_values.e2e_folder_path, archive_path)
        variables_from_response = helper.process_samples_new(self,logger,config_values.host, config_values.username, config_values.password,
                                               config_values.stop_at_buffer_exchange, archive_path)
        variables = json.loads(variables_from_response.replace("'", "\""))
        logger.info(f"variable:::::{variables}")
        workflow_id = helper.get_workflow_id(self,logger,config_values.host,config_values.username,config_values.password)
        logger.info(f"workflow_id:::::{workflow_id}")
        latest_operation_id = helper.get_reponse_from_pipeline_runs(self,logger,config_values.host,config_values.username,
                                                                       config_values.password, config_values.buffer_exchange_trampstop)
        pipeline_id = helper.get_pipeline_id(self,logger,config_values.host,config_values.username,config_values.password)
        node_id = helper.get_node_id(self,logger,config_values.host, config_values.username, config_values.password,
                                     pipeline_id, "Buffer Exchange")
        helper.post_api_for_starting_workflow(self,logger,config_values.host,config_values.username,config_values.password,
                                              pipeline_id,node_id,config_values.instrument_type,config_values.instrument_serial_number)
        time.sleep(20)
        hamilton_ui.click_on_simulation_mode_ok_button(self)
        time.sleep(3)
        hamilton_ui.check_options_on_the_window(self, ["No Wait","No Pipetting","Stoppable Timers"])
        hamilton_ui.enter_username_and_batchid(self,number_of_batches)
        hamilton_ui.click_on_method_start_ok_button(self)
        hamilton_ui.enter_value_on_bulk_reagent_scan_window(self,variables.get('buffer_exchange_etoh_lot_number'))
        random_number = random.randint(10000, 99999)
        DWT_plate_id = config_values.dwt_plate_id + str(random_number)
        barcodes_usb_plate_id = helper.get_plate_from_labware(self, logger, config_values.host, config_values.username,
                                                              config_values.password,
                                                              variables.get('buffer_exchange_be_spri_plate_lot_number'))
        barcodes_universal_te_plate_id = helper.get_plate_from_labware(self, logger, config_values.host,
                                                                       config_values.username,config_values.password,
                                                                       variables.get('buffer_exchange_be_te_plate_lot_number'))
        if number_of_batches == "1":
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_be_load1_deck_setup)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_buffer_exchange_pltCar2, texts_to_enter=[config_values.eto_plate, barcodes_usb_plate_id[0],
                                                                 DWT_plate_id, config_values.nocode, ple_plate_id])
            time.sleep(30)
            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_buffer_exchange_pltCar1, texts_to_enter=[config_values.nocode,
                                                                       barcodes_universal_te_plate_id[0], ple_plate_id, config_values.nocode, config_values.nocode])
        else:
            hamilton_ui.clicks_on_deck_setup_window(self, config_values.epionly_be_load2_deck_setup)
            time.sleep(5)
            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_buffer_exchange_pltCar3,
                                                 texts_to_enter=[config_values.nocode, barcodes_usb_plate_id[0],
                                                                 DWT_plate_id, config_values.nocode, ple_plate_id])
            random_number = random.randint(10000, 99999)
            DWT_plate_id_2 = config_values.dwt_plate_id + str(random_number)
            ple_plate_id_2 = helper.create_ple_plate_id(self, logger)

            hamilton_ui.enter_simulated_barcodes(self,logger,config_values.window_name_buffer_exchange_pltCar2,
                                                 texts_to_enter=[config_values.eto_plate, barcodes_usb_plate_id[1],
                                                                 DWT_plate_id_2, config_values.nocode, ple_plate_id_2])
            output_plates = helper.get_ex_elution_plates(self, logger, config_values.host, config_values.username,config_values.password)

            hamilton_ui.enter_simulated_barcodes(self,logger, config_values.window_name_buffer_exchange_pltCar1,
                                                 texts_to_enter=[config_values.nocode,
                                                                 barcodes_universal_te_plate_id[0], output_plates[0],
                                                                 output_plates[1], config_values.nocode])
