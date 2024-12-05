import os
import threading
import time
import flet as ft
from flet import FilePicker, FilePickerResultEvent, TextField, ElevatedButton, Column, Text, Row, AlertDialog, Radio, RadioGroup
from observer import FileObserver

def main(page: ft.Page):
    # Default values
    default_interval = 10
    default_count_threshold = 5
    default_observe_dir = ""
    default_instr = ""
    full_observe_dir = default_observe_dir
    observer = None  # Variable to hold the FileObserver instance
    monitor_thread = None  # To hold the monitoring thread

    # Create an alert dialog and add it to the overlay
    dialog_content = Text("")  # Text for updating the dialog message
    dialog = AlertDialog(content=dialog_content)
    page.overlay.append(dialog)

    # Define fields for user input
    interval_field = TextField(
        label="Interval (min)", value=str(default_interval), width=150
    )
    count_threshold_field = TextField(
        label="Count Threshold", value=str(default_count_threshold), width=150
    )
    instr_field = TextField(
        label="Instrument", value=str(default_instr), width=150
    )
    observe_dir_text = Text(default_observe_dir)
    start_button = ElevatedButton("Start Observing", disabled=True)
    stop_button = ElevatedButton("Stop Observing", disabled=True)

    # Radio buttons for enabling/disabling screenshot
    screenshot_radio_group = RadioGroup(
        content=Row(
            [
                Radio(value="enabled", label="Enable Screenshot"),
                Radio(value="disabled", label="Disable Screenshot"),
            ]
        )
    )

    # Directory selection 
    def pick_directory(e: FilePickerResultEvent):
        nonlocal full_observe_dir
        if e.path:
            full_observe_dir = e.path  # Store the full path
            split_path = e.path.strip(os.sep).split(os.sep)
            displayed_path = os.sep.join(split_path[-3:])  # Display the last 3 parts of the path
            
            observe_dir_text.value = f"...{os.sep}{displayed_path}" if len(split_path) > 3 else e.path
            observe_dir_text.update()
            update_start_button_state()

    file_picker = FilePicker(on_result=pick_directory)
    page.overlay.append(file_picker)

    def update_start_button_state():
        """Enable or disable the Start button based on conditions"""
        start_button.disabled = not (
            observe_dir_text.value != default_observe_dir and screenshot_radio_group.value
        )
        start_button.update()

    def check_process():
        """Periodically check whether the process is running"""
        nonlocal observer
        while observer and observer.process.is_alive():
            time.sleep(1)  # Check every 1 seconds
        if observer:
            stop_observing(None)
            show_dialog("Observing has been stopped automatically and email sent.")

    def show_dialog(message: str):
        """Show an alert dialog"""
        dialog_content.value = message
        dialog_content.update()
        dialog.open = True
        page.update()

    def start_observing(e):
        nonlocal observer, monitor_thread
        try:
            interval = float(interval_field.value)
            count_threshold = int(count_threshold_field.value)
            observe_dir = full_observe_dir
            instr = instr_field.value
            screenshot_enabled = screenshot_radio_group.value == "enabled"

            observer = FileObserver(
                interval=interval,
                count_threshold=count_threshold,
                observe_dir=observe_dir,
                instr=instr,
                screen_shot=screenshot_enabled,
            )
            observer.start()  # Assume the start method exists
            start_button.disabled = True
            stop_button.disabled = False  # Enable the stop button
            start_button.update()
            stop_button.update()

            show_dialog("Observing started")

            # Start monitoring thread
            monitor_thread = threading.Thread(target=check_process, daemon=True)
            monitor_thread.start()

        except ValueError as ex:
            show_dialog(f"Error: {str(ex)}")

    def stop_observing(e):
        nonlocal observer
        if observer:
            observer.stop()  # Call the stop method
            observer = None
            stop_button.disabled = True
            start_button.disabled = False  # Re-enable the start button
            stop_button.update()
            start_button.update()

            show_dialog("Observing stopped successfully")

    # GUI Layout
    page.title = "File Observer GUI"
    page.window.width = 500
    page.window.height = 300
    page.add(
        Column(
            [
                Row([interval_field, count_threshold_field, instr_field]),
                Row(
                    [
                        ElevatedButton("Select Directory", on_click=lambda _: file_picker.get_directory_path()),
                        observe_dir_text,
                    ]
                ),
                Row([Text("Screenshot:"), screenshot_radio_group]),
                Row([start_button, stop_button]),
            ],
            spacing=10,
        )
    )

    # Event Handlers
    start_button.on_click = start_observing
    stop_button.on_click = stop_observing
    screenshot_radio_group.on_change = lambda _: update_start_button_state()


# Run the application
if __name__ == "__main__":
    ft.app(target=main)
