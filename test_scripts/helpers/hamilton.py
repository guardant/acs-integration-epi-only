
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from helpers.helper import config_values
import time


class hamilton_ui:
    def click_on_simulation_mode_ok_button(self):
        app = Application(backend="uia").connect(title_re = "Running in simulation mode")
        for w in app.windows():
            print(w.window_text())
        time.sleep(2)
        dlg = app.window(title_re="Running in simulation mode")
        dlg.set_focus()
        time.sleep(2)
            # Print available controls to ensure we can see the button
        send_keys('{ENTER}')
        time.sleep(2)
        return app

    def check_options_on_the_window(self,desired_texts):
        app = Application(backend="uia").connect(title="Set Test Flags")
        popup_window = app.window(title="Set Test Flags")
        popup_window.set_focus()
        checkboxes = popup_window.children(control_type='CheckBox')
        for checkbox in checkboxes:
            if checkbox.window_text() in desired_texts:
                checkbox.click_input()
        ok_button = popup_window.child_window(title="OK", control_type="Button")
        ok_button.click()
        time.sleep(4)

    def enter_username_and_batchid(self,no_of_batches):
        app = Application(backend="uia").connect(title_re="User Name and Batch_ID Selection Window")
        username_selection_window = app.window(title="User Name and Batch_ID Selection Window", control_type="Window")
        username_selection_window.print_control_identifiers()
        operator_id = username_selection_window.child_window(auto_id="textBox1", control_type="Edit")
        operator_id.set_text(config_values.operator_id)
        batch_id = username_selection_window.child_window(auto_id="textBox2", control_type="Edit")
        batch_id.set_text(config_values.batch_id)
        number_of_batches = username_selection_window.child_window(auto_id="PART_TextBox", control_type="Edit")
        number_of_batches.set_text(no_of_batches)
        start_button = username_selection_window.child_window(title="START", control_type="Button")
        time.sleep(2)
        start_button.click()
        # Wait for the button click to take effect
        app.wait_cpu_usage_lower(threshold=5, timeout=30, usage_interval=1.0)
        time.sleep(3)

    def click_on_method_start_ok_button(self):
        app = Application(backend="uia").connect(title_re="Method Start")
        method_start_window = app.window(title="Method Start", control_type="Window")
        method_start_window.print_control_identifiers()
        OK_button = method_start_window.child_window(title="OK", control_type="Button")
        OK_button.click()
        app.wait_cpu_usage_lower(threshold=5, timeout=30, usage_interval=1.0)

    def enter_value_on_bulk_reagent_scan_window(self,plate_id):
        time.sleep(5)
        app = Application(backend="uia").connect(title_re="Bulk Reagent Scan")
        bulk_reagent_scan_window = app.window(title="Bulk Reagent Scan", control_type="Window")
        bulk_reagent_scan_window.set_focus()
        eoth_plate = bulk_reagent_scan_window.child_window(auto_id="textBox1", control_type="Edit")
        eoth_plate.set_text(plate_id)
        time.sleep(2)
        OK_button = bulk_reagent_scan_window.child_window(title="OK", control_type="Button")
        OK_button.click()
        app.wait_cpu_usage_lower(threshold=5, timeout=30, usage_interval=1.0)

    def clicks_on_deck_setup_window(self, title):
        time.sleep(3)
        app = Application(backend="uia").connect(title_re=title)
        load_deck_setup_window = app.window(title=title, control_type="Window")
        load_deck_setup_window.set_focus()
        load_deck_setup_window.child_window(title="OK", control_type="Button").click()

    def enter_simulated_barcodes(self,logger,window_name_pltCar,texts_to_enter):
        # Simulate Scanned Barcodes
        time.sleep(5)
        app = Application(backend="uia").connect(title_re=window_name_pltCar)
        simulate_scanned_barcodes_window = app.window(title=window_name_pltCar, control_type="Window")
        simulate_scanned_barcodes_window.set_focus()
        pane = simulate_scanned_barcodes_window.child_window(title="Custom1", control_type="Pane")
        help_button = simulate_scanned_barcodes_window.child_window(title="Help", control_type="Button")
        help_button.set_focus()
        send_keys('{TAB}{TAB}{UP}')
        pane.set_focus()
        send_keys('{UP}')
        # Enter text in each box, assuming they are now focused one after the other
        for text in texts_to_enter:
            if text == "No Code":
                send_keys('{DOWN}')
            else:
                send_keys(text + '{DOWN}')
                logger.info(f"Entered barcode is {text}")
            time.sleep(0.5)
        simulate_scanned_barcodes_window.child_window(title="OK", control_type="Button").click()
        # Wait for the button click to take effect
        app.wait_cpu_usage_lower(threshold=5, timeout=7, usage_interval=1.0)

    def method_complete_ok_button_click(self):
        app = Application(backend="uia").connect(title_re="Method Status")
        method_status_window = app.child_window(title="Method Status", control_type="Window")
        if method_status_window.exists():
            method_status_window.set_focus()
            # Wait for the button click to take effect
            method_status_window.child_window(title="OK", control_type="Button").click()

    def select_options_from_dialog_window(self,desired_texts):
        app = Application(backend="uia").connect(title="Dialog")
        popup_window = app.window(title="Dialog")
        popup_window.set_focus()
        popup_window.print_control_identifiers()
        checkboxes = popup_window.children(control_type='CheckBox')
        for checkbox in checkboxes:
            if checkbox.window_text() in desired_texts:
                checkbox.click_input()
        ok_button = popup_window.child_window(title="OK", control_type="Button")
        ok_button.click()
        time.sleep(4)

    def click_ok_on_simulation_mode_activated_window(self,main_window):
        simulation_mode_activated_window = main_window.child_window(title="Simulation mode activated", control_type="Window")
        simulation_mode_activated_window.set_focus()
        simulation_mode_activated_window.child_window(title="OK", control_type="Button").click()

    def close_application_window(self,app,main_window):
        # Close the application
        app.wait_cpu_usage_lower(threshold=5, timeout=5, usage_interval=1.0)
        main_window.child_window(title="Close", control_type="Button").click_input()

    def click_ok_button_on_buffer_plate_handling_window(self,app,main_window):
        buffer_plate_handling_window = main_window.child_window(title="Fast Hybridization Buffer Plate Handling continued",
                                                                    control_type="Window")
        buffer_plate_handling_window.set_focus()
        buffer_plate_handling_window.child_window(title="OK", control_type="Button").click()

    def enter_value_on_manual_barcode_entry_window(self,app,main_window,plate_id):
        manual_barcode_entry_window = main_window.child_window(title="Manual Barcode Entry", control_type="Window")
        manual_barcode_entry_window.set_focus()
        text_box = manual_barcode_entry_window.child_window(auto_id="textBox1", control_type="Edit")
        text_box.set_edit_text(plate_id)
        time.sleep(2)
        manual_barcode_entry_window.child_window(title="OK", control_type="Button").click()

