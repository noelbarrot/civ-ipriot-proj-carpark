import random
import threading
import time
import tkinter as tk
from typing import Iterable
import paho.mqtt.client as paho


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


class CarPark_Display:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay(
            'Moondalup', CarPark_Display.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription
        while True:
            PAHO_HOST = 'localhost'
            PAHO_PORT = 1883
            PAHO_KEEP_ALIVE = 300

            PAHO_CLIENT_NAME = 'car_park_sensor'
            PAHO_TOPIC = 'car_park/data'

            client = paho.Client(PAHO_CLIENT_NAME)
            client.connect(PAHO_HOST, PAHO_PORT, PAHO_KEEP_ALIVE)

            client.subscribe(PAHO_TOPIC)

            def on_message_callback(client, userdata, message):
                pass
            # NOTE: Dictionary keys *must* be the same as the class fields
            # field_values = dict(zip(CarPark_Display.fields, [
            #     f'{random.randint(0, 150):03d}',
            #     f'{random.randint(0, 45):02d}℃',
            #     time.strftime("%H:%M:%S")]))
            # # Pretending to wait on updates from MQTT
            # time.sleep(random.randint(1, 10))
            # # When you get an update, refresh the display.
            # self.window.update(field_values)





CarPark_Display()