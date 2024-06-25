import string, time, requests, os, yaml, shutil, zipfile
import csv,re, random, ruamel.yaml, json,re
import numpy as np
import base64
import datetime

class config_values:
    curr_dir = os.path.dirname(__file__)
    config_path = os.path.join(curr_dir, 'config.json')

    with open(config_path, 'r') as file:
        config = json.load(file)

    instrument_type = config['instrument_type']
    instrument_serial_number = config['instrument_serial_number']
    instrument_serial_name = config['instrument_serial_name']
    artifacts_yaml_file = config['artifacts_yaml_file']
    optic_env_file_path =  config['optic_env_file_path']
    e2e_folder_path = config['e2e_folder_path']
    host = config['host']
    username = config['username']
    password = config['password']
    dwt_plate_id = config['dwt_plate_id']
    window_name_buffer_exchange_pltCar3 = config['window_name_buffer_exchange_pltCar3']
    window_name_buffer_exchange_pltCar2 = config['window_name_buffer_exchange_pltCar2']
    window_name_buffer_exchange_pltCar1 = config['window_name_buffer_exchange_pltCar1']
    stop_at_buffer_exchange = config['stop_at_buffer_exchange']
    operator_id = config['operator_id']
    batch_id = config['batch_id']
    epionly_be_load1_deck_setup = config['epionly_be_load1_deck_setup']
    epionly_be_load2_deck_setup = config['epionly_be_load2_deck_setup']
    epionly_mbd_setup_load11_deck_setup = config['epionly_mbd_setup_load11_deck_setup']
    epionly_mbd_setup_load12_deck_setup = config['epionly_mbd_setup_load12_deck_setup']
    eto_plate = config['eto_plate']
    stop_at_mbd_setup = config['stop_at_mbd_setup']
    dwe_plate_id = config['dwe_plate_id']
    xqt_plate = config['xqt_plate']
    nocode = config['nocode']
    buffer_exchange_trampstop = config['buffer_exchange_trampstop']
    mbd_setup_tramstop = config['mbd_setup_tramstop']
    stop_at_mbdc = config['stop_at_mbdc']
    stop_at_library_prep = config['stop_at_library_prep']
    subtitle_project_for_library_prep = config['subtitle_project_for_library_prep']
    version_for_library_prep = config['version_for_library_prep']
    siriusLDT_library_prep_load3_deck_setup = config['siriusLDT_library_prep_load3_deck_setup']
    usb_plate_id_for_lp = config['usb_plate_id_for_lp']
    usb_plate_id_for_lp_1= config['usb_plate_id_for_lp_1']
    mbd_cleanup_trampstop = config['mbd_cleanup_trampstop']
    lp_oligo_mix_plate = config['lp_oligo_mix_plate']
    dna_suspension_buffer_plate = config['dna_suspension_buffer_plate']
    siriusLDT_library_prep_load302_deck_setup = config['siriusLDT_library_prep_load302_deck_setup']
    siriusLDT_library_prep_load303_deck_setup = config['siriusLDT_library_prep_load303_deck_setup']
    usb_plate_id_for_lp_2 = config['usb_plate_id_for_lp_2']
    msre_cleanup_trampstop = config['msre_cleanup_trampstop']
    mbd_was_tramstop = config['mbd_was_tramstop']
    stop_at_ens = config['stop_at_ens']
    subtitle_project_for_ens = config['subtitle_project_for_ens']
    version_for_be_ens = config['version_for_be_ens']
    siriusLDT_ens_load3_deck_setup = config['siriusLDT_ens_load3_deck_setup']
    enrichment_setup_trampstop = config['enrichment_setup_trampstop']
    library_prep_tramstop = config['library_prep_tramstop']

class helper:
    # def __init__(self, logger):
    #     self.logger = logger

    def generate_random_code():
        return np.base_repr(np.random.randint(100000, 999999), base=36)

    def generate_random_word(length=8):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(length))

    def create_ple_plate_id(self,logger):
        #if 'Source Plate ID' in df.columns:
        new_id = 'PLEJUN24' + helper.generate_random_code() + '0001'
        logger.info(f"ple_plate::::{new_id}")
        return new_id

    def update_artifacts_yaml_file(self,logger,artifacts_yaml_file_path, plate_name_asc, plate_value):
        # Open the file and load the data using ruamel.yaml
        yaml = ruamel.yaml.YAML()
        with open(artifacts_yaml_file_path, 'r') as file:
            data = yaml.load(file)

        # Update the value
        if plate_name_asc in data['objects'] and 'value' in data['objects'][plate_name_asc]:
            data['objects'][plate_name_asc]['value'] = plate_value
        else:
            logger.info(f"Key {plate_name_asc} or 'value' not found in the YAML file.")

        # Write the updated content back to the file using ruamel.yaml
        with open(artifacts_yaml_file_path, 'w') as file:
            yaml.dump(data, file)

    def add_hamilton_start_in_artifacts_yaml_file(self,logger,artifacts_yaml_file_path):
        yaml = ruamel.yaml.YAML()
        hamilton_star = helper.generate_random_word()
        #hamilton_star = "Workstation"
        with open(artifacts_yaml_file_path, 'r') as file:
            data = yaml.load(file)

        if 'hamilton_star' in data['objects']:
            hamilton_star_obj = data['objects']['hamilton_star']
            logger.info("Updating 'hamilton_star' object...")

            # Recreate the hamilton_star object with 'name' after 'type'
            updated_hamilton_star_obj = {}
            for key, value in hamilton_star_obj.items():
                updated_hamilton_star_obj[key] = value
                #if key == 'type':
                updated_hamilton_star_obj['name'] = hamilton_star
                updated_hamilton_star_obj['serial_number'] = hamilton_star
            data['objects']['hamilton_star'] = updated_hamilton_star_obj

        else:
            logger.info("Key 'hamilton_star' not found in the YAML file. Adding new 'hamilton_star' object.")
            data['objects']['hamilton_star'] = {'type': 'instrument', 'name': hamilton_star}
            data['objects']['hamilton_star'] = {'type': 'instrument', 'serial_number': hamilton_star}

            # Write the updated content back to the file using ruamel.yaml
        with open(artifacts_yaml_file_path, 'w') as file:
            yaml.dump(data, file)

        return hamilton_star

    def add_hamilton_start_in_artifacts_yaml_file_for_post_methods(self,logger,artifacts_yaml_file_path):
        yaml = ruamel.yaml.YAML()
        #hamilton_star = helper.generate_random_word()
        hamilton_star = "Workstation"
        hamilton_star_serial_number = "SN0000"
        with open(artifacts_yaml_file_path, 'r') as file:
            data = yaml.load(file)

        if 'hamilton_star' in data['objects']:
            hamilton_star_obj = data['objects']['hamilton_star']
            logger.info("Updating 'hamilton_star' object...")

            # Recreate the hamilton_star object with 'name' after 'type'
            updated_hamilton_star_obj = {}
            for key, value in hamilton_star_obj.items():
                updated_hamilton_star_obj[key] = value
                #if key == 'type':
                updated_hamilton_star_obj['name'] = hamilton_star
                updated_hamilton_star_obj['serial_number'] = hamilton_star_serial_number
            data['objects']['hamilton_star'] = updated_hamilton_star_obj

        else:
            logger.info("Key 'hamilton_star' not found in the YAML file. Adding new 'hamilton_star' object.")
            data['objects']['hamilton_star'] = {'type': 'instrument', 'name': hamilton_star}
            data['objects']['hamilton_star'] = {'type': 'instrument', 'serial_number': hamilton_star_serial_number}

            # Write the updated content back to the file using ruamel.yaml
        with open(artifacts_yaml_file_path, 'w') as file:
            yaml.dump(data, file)
        logger.info(f"hamilton_star_serial_number:::::{hamilton_star_serial_number}")
        return hamilton_star_serial_number

    def archive_zip_file(self,logger,e2e_folder_path,archive_path):
        # Check if archive.zip exists and delete it if it does
        if os.path.exists(archive_path):
            os.remove(archive_path)
            logger.info("Existing archive.zip found and deleted.")

            # Create a new zip archive of the folders
        with zipfile.ZipFile(archive_path, 'w') as archive:
            # Walk through the directory
            for folder_name, subfolders, filenames in os.walk(e2e_folder_path):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    file_path = os.path.join(folder_name, filename)
                    # Avoid adding the archive file itself
                    if file_path == archive_path:
                        continue
                    # Add file to zip, storing the path relative to the e2e_folder_path
                    archive.write(file_path, os.path.relpath(file_path, e2e_folder_path))
            logger.info("New archive.zip created with current folder contents.")

    def process_samples_new(self,logger,host,username,password,stop_at,archive_path):
        # Open the file and post it to the server
        with open(archive_path, 'rb') as f:
            response = requests.post(
                f"http://{host}/api/v1/seed/process_samples_new/",
                auth=(username, password),
                files={
                    "file": (archive_path.split('/')[-1], f, 'application/zip')
                },
                data={"stop_at": stop_at},
                stream=True
            )
        logger.info("Process samples is running")
        # Check the response status and logger.info relevant information
        try:
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            json_response = response.json()
            logger.info("Okay")  # Indicate that the post was successful
            #logger.info(json_response.get('log', 'No log information available'))
            variables = str(response.json()['objects']['variables'])
            json_string = json.dumps(json_response)
            if 'error' in json_response:
                logger.info(json_response['error'])
            else:
                logger.info("No errors reported.")
            return variables
        except requests.exceptions.HTTPError as err:
            logger.info(f"HTTP Error occurred: {err}")
        except ValueError:
            logger.info("Error decoding JSON")

    def get_reponse_from_pipeline_runs(self,logger,host,username,password,workflow_name):
        url = f"http://{host}/api/v2/pipeline_runs/?latest_operation_name={workflow_name}"
        logger.info(f"url::::{url}")
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        latest_operation_id =  json_response['results'][0]['latest_operation_id']
        logger.info(f"latest_operation_id:::{latest_operation_id}")
        return latest_operation_id

    def post_api_for_instrument_job_for_hamilton_star(self,logger,host,username,password,latest_operation_id,hamilton_star):
        payload = {
            "operation_state": {
                "paused_action_index": -1,
                "finished": False,
                "operation_id": latest_operation_id
            },
            "inputs": {
                "form": {
                    "Operators": {},
                    "Instrument": {
                        "hamilton_star": hamilton_star
                    }
                }
            }
        }

        response = requests.post(
            f"http://{host}/api/v2/operations/advance/",
            auth=(username, password),
            json=payload  # Add the payload here
        )
        time.sleep(4)
        json_response = response.json()
        logger.info(f"Advanced to the instrument job")

    def post_api_for_instrument_job_for_Hamilton_STAR(self,logger,host,username,password,latest_operation_id,hamilton_star):

        payload = {"inputs": {"form": {"Operators": {}, "Instruments": {"Hamilton STAR": hamilton_star}}},
                   "operation_state": {"operation_id": latest_operation_id, "finished": False,
                                       "paused_action_index": -1}}

        response = requests.post(
            f"http://{host}/api/v2/operations/advance/",
            auth=(username, password),
            json=payload  # Add the payload here
        )
        time.sleep(4)
        json_response = response.json()
        logger.info("Post API for instument job is completed")

    def get_output_plates_from_timeline(self,logger,host,username,password,latest_operation_id,tramstop_name):
        url = f"http://{host}/api/v2/operations/{latest_operation_id}/timeline/"
        logger.info(f"url::::{url}")
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, auth=(username, password))
        trams = response.json()['timeline']

        for tram in trams:
            print('Tramstop UUID and Tramstop Name : ' + {str(tram['uuid'])} + " -- " + tram['name'])
            if tram['name'] == tramstop_name:
                    workflow_uuid = tram['uuid']

        url = f"http://{host}/api/v2/operations/{workflow_uuid}/"
        logger.info(f"url:::{url}")
        response = requests.get(url, auth=(username, password))
        json_response = response.json()

        output_plates = []
        outputs = json_response.get('outputs', [])

        def extract_inventory_ids(output):
            if isinstance(output, dict):
                value = output.get('value', {})
                if isinstance(value, dict):
                    inventory_id = value.get('inventory_id')
                    if inventory_id:
                        output_plates.append(inventory_id)

        for output in outputs:
            extract_inventory_ids(output)
            # Check nested outputs if any
            nested_outputs = output.get('outputs', [])
            for nested_output in nested_outputs:
                extract_inventory_ids(nested_output)

        logger.info(f"output_plates::::{output_plates}")
        logger.info(f"workflow_uuid:::::{workflow_uuid}")
        return output_plates, workflow_uuid

    def get_plate_from_labware(self,logger,host,username,password,labware_lot_number):
        url = f"http://{host}/api/v2/labware_lots/?is_imported=true&lot_number={labware_lot_number}"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        uuid_for_labware = json_response['results'][0]['uuid']
        url = f"http://{host}/api/v2/labware_lots/{uuid_for_labware}/"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        # Extract the barcodes
        barcodes = [item['barcode'] for item in json_response['labware']]
        logger.info(f"barcodes from labware::::{barcodes}")
        return barcodes

    def abort_instrument_job_for_started_state(self,logger,host,username,password,instrument_serial_number):
        url=f"http://{host}/api/v1/instrument_jobs/?state=started"
        response = requests.get(url, auth=(username, password))
        if response.json():
            json_response = response.json()
            self.logger.info(json_response)
            counts = len(json_response['results'])
            logger.info(f"instrument job count to abort for started state:::::{counts}")
            for count in range(counts):
                uuid_for_instrument_job = json_response['results'][count]['uuid']
                payload = {"errors": {"errorkey": ["e", "r", "r", "o", "r", "v", "a", "l", "u", "e"]}}
                response = requests.put(
                    f"http://{host}/api/v1/instrument_jobs/{uuid_for_instrument_job}/abort/",
                    auth=(username, password),
                    json=payload  # Add the payload here
                )
                time.sleep(4)

    def abort_instrument_job_for_assigned_state(self,logger,host,username,password,instrument_serial_number):
        url=f"http://{host}/api/v1/instrument_jobs/?state=assigned"
        response = requests.get(url, auth=(username, password))
        if response.json():
            json_response = response.json()
            counts = len(json_response['results'])
            logger.info(f"instrument job count to abort for assigned state:::::{counts}")
            for count in range(counts):
                uuid_for_instrument_job = json_response['results'][count]['uuid']
                payload = {"errors": {"errorkey": ["e", "r", "r", "o", "r", "v", "a", "l", "u", "e"]}}
                response = requests.put(
                    f"http://{host}/api/v1/instrument_jobs/{uuid_for_instrument_job}/abort/",
                    auth=(username, password),
                    json=payload
                )
                time.sleep(4)

    def get_workflow_id(self,logger,host,username,password):
        url=f"http://{host}/api/v2/pipeline_runs/?in_progress=true"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        workflow_id = json_response['results'][0]['execution_name']
        logger.info(f"workflow_id::::{workflow_id}")
        return workflow_id

    def get_pipeline_id(self,logger,host,username,password):
        url = f"http://{host}/api/v2/pipelines/"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        pipeline_id = json_response[0]['uuid']
        logger.info(f"pipeline_id::::{pipeline_id}")
        return pipeline_id

    def get_node_id(self,logger,host,username,password,pipeline_id,workflow_name):
        url = f"http://{host}/api/v2/pipelines/get_starting_nodes/?pipeline_id={pipeline_id}&selected_mode=default"
        logger.info(f"URL for get node:::::{url}")
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        logger.info(f"json from pipeline api to fetch the node::::::{json_response}")
        logger.info(workflow_name)
        time.sleep(3)
        node_id = None
        for workflow_names in json_response:
            logger.info(f"workflow_name['operation_name']:::{workflow_names['operation_name']}")
            if workflow_names['operation_name'] == workflow_name:
                node_id = workflow_names['node_id']
                break
        logger.info(f"node_id::::{node_id}")
        return node_id

    def post_api_for_starting_workflow(self,logger,host,username,password,pipeline_id,node_id,instrument_type,instrument_serial_number):
        payload = {"pipeline_id": pipeline_id,"start_node_id":node_id,
                   "instrument":{"instrument_type":instrument_type,"serial_number":instrument_serial_number},
                   "mode":"default"}
        headers = {"X-Action-Auth": "eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJBQ1NQQHNzd29yZDEifQ=="}

        response = requests.post(
            f"http://{host}/api/v2/pipelines/start/",
            auth=(username, password),
            headers = headers,
            json=payload  # Add the payload here
        )
        time.sleep(4)
        json_response = response.json()
        logger.info("json_response from post api for starting a workflow:::::", json_response)

    def get_operation_details_by_uuid(self, logger, host, username, password, operation_uuid):
        url = f"http://{host}/api/v2/operations/{operation_uuid}/"
        logger.info(f"url::::{url}")
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        logger.info(f"operation_details response:::{json_response}")
        return json_response

    def get_operation_id(self,logger,host,username,password,operation_name):
        url = f"http://{host}/api/v2/pipeline_runs/"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        operations = json_response.get('results')
        sorted_operations = sorted(operations, key=lambda x: datetime.datetime.strptime(x['created'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse = True)
        assert sorted_operations
        if not operation_name:
            latest_operation_id = sorted_operations[0].get('latest_operation_id')
        else:
            for operation in sorted_operations:
                if operation['latest_operation_name'] == operation_name:
                    latest_operation_id = operation.get('latest_operation_id')
        logger.info(f"latest_operation_id::::{latest_operation_id}")
        return latest_operation_id

    def get_be_elution_plate(self,logger,host,username,password,operation_name):
        be_operation_uuid = helper.get_operation_id(self,logger,host,username,password,operation_name)
        url = f"http://{host}/api/v2/operations/{be_operation_uuid}/"
        response = requests.get(url, auth=(username, password))
        json_response = response.json()
        print(json_response)
        be_elution_plate = json_response['outputs'][0]['value']['inventory_id']
        assert be_elution_plate
        logger.info(f"be_operation_uuid:::::{be_operation_uuid}")
        logger.info(f"be_elution_plate::::{be_elution_plate}")
        return be_operation_uuid,be_elution_plate

    def get_instrument_job_id_for_started_state(self,logger,host,username,password,instrument_serial_number):
        url=f"http://{host}/api/v1/instrument_jobs/?state=started"
        response = requests.get(url, auth=(username, password))
        if response.json():
            json_response = response.json()
            self.logger.info(json_response)
            uuid = json_response['results'][0]['uuid']
            logger.info(f"instrument job uuid for Hamilton:::::{uuid}")

    def get_ex_elution_plates(self,logger,host,username,password):
        query_params = {'latest_operation_name' : 'cfDNA Extraction Upload'}
        url = f"http://{host}/api/v2/pipeline_runs/"
        response = requests.get(url, auth=(username, password), params = query_params)
        if response.json():
            json_response = response.json()
            self.logger.info(json_response)
            plate_id1 = json_response['results'][0]['input_plates'][1]
            plate_id2 = json_response['results'][1]['input_plates'][1]
            logger.info(f"ex elution plate id:::::{plate_id1} and {plate_id2}")
        return plate_id1, plate_id2

    # def get_be_output_samples(self,logger,host,username,password):
    #     tag_components = ["artifact_set", "name", config_values.buffer_exchange_trampstop]
    #     tag = b",".join(map(lambda tag_part: base64.b64encode(tag_part.encode()), tag_components))
    #     url = f"http://{host}/api/v1/chain_of_custody/"
    #     chain_of_custody_reponse = requests.get(url, auth=(username, password),params = {'tag': tag})
    #     events = chain_of_custody_reponse.json().get('results')
    #
    #     be_opertaion_id = None
    #     for event in events:
    #         if event['operation_name'] == config_values.buffer_exchange_trampstop:
    #             be_operation_id = event['operation_id']
    #             break
    #     assert be_operation_id
    #
    #     be_operation_id_details = helper.get_operation_details_by_uuid(self, logger, host, username, password,
    #                                                                  be_operation_id)
    #     logger.info(f"be elution plates for buffer exchange:::::{be_operation_id_details.outputs[0].value['tubes']}")
    #     return be_operation_id_details.outputs[0].value['tubes']