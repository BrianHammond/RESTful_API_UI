import sys
import qdarkstyle
import requests
import json
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
from PySide6.QtCore import QSettings, QTimer
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Dialog as about_ui

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.api = API() # initialize FlaskAPI class

        # Connect line_server to the update_base_url method
        self.line_server.returnPressed.connect(self.update_base_url)       

        # Update label_connection based on connection status
        self.label_connection.setText("Not Connected to FastAPI")
        #self.update_connection_status()

        # Set up a timer to poll the connection status every 30 seconds
        self.connection_timer = QTimer(self)
        self.connection_timer.timeout.connect(self.update_connection_status)
        self.connection_timer.start(10000)  # 10 seconds in milliseconds

        # button
        self.button_post.clicked.connect(self.api_post)
        self.button_get.clicked.connect(self.api_get)
        self.button_put.clicked.connect(self.api_put)
        self.button_delete.clicked.connect(self.api_delete)
        
        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about_qt.triggered.connect(lambda: QApplication.aboutQt())
        self.action_about.triggered.connect(lambda: AboutWindow(dark_mode=self.action_dark_mode.isChecked()).exec())

    def employee_data(self, id, first_name, middle_name, last_name, age, title, address1, address2, country, misc):
        if age.strip() == "":
            age = 0
        else:
            age = int(age)
        
        data = {
            "employee_id": int(id),
            "name": {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name
            },
            "age": age,
            "title": title,
            "address": {
                "address_1": address1,
                "address_2": address2,
                "country": country
            },
            "misc": misc
        }
        return data

    def update_base_url(self):
        new_url = f"http://{self.line_server.text()}"

        self.api.base_url = new_url
        print(f"API base URL updated to: {self.api.base_url}")

        # check the connection if base_url is set
        if self.api.base_url:
            self.api.is_connected = self.api.check_connection()
            self.update_connection_status()
            self.initialize_table()
            self.api_get()

    def api_post(self): # add data
        self.current_date = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        id = self.current_date
        
        # Get the values from the QLineEdits
        first_name = self.line_firstname.text()
        middle_name = self.line_middlename.text()
        last_name = self.line_lastname.text()
        age = self.line_age.text()
        title = self.line_title.text()
        address1 = self.line_address1.text()
        address2 = self.line_address2.text()
        country = self.line_country.text()
        misc = self.line_misc.text()

        row = self.table.rowCount()
        self.populate_table(row, id, first_name, middle_name, last_name, age, title, address1, address2, country, misc)

        # Prepare the data in the format required by the API
        data = self.employee_data(id, first_name, middle_name, last_name, age, title, address1, address2, country, misc)

        # Send the data using FlaskAPI's send_post method
        response = self.api.send_post(data)
        if response:
            print("Data sent successfully:", response)
        else:
            print("Failed to send data.")

        self.clear_fields()

    def api_get(self): # get data
        # Fetch the employee_id from the QLineEdit
        employee_id = self.line_employee_id.text()

        # Prepare the parameters for the GET request
        params = {}
        if employee_id:
            params = {'employee_id': employee_id}  # Add employee_id to query parameters if present

        # Call the send_get method from API class
        data = self.api.send_get(params)  # Pass params to send_get method

        if data:
            print("Data received from API:", data)  # Log the received data

            # Check if the data contains the 'employees' key
            if "employees" in data:
                employees = data["employees"]  # Get the list of employees
                
                # Initialize the table to ensure it is cleared before populating new data
                self.initialize_table()

                # Iterate over the employees data and populate the table
                for record in employees:
                    if isinstance(record, dict):
                        # Extract values for each record
                        id = record.get("employee_id")
                        first_name = record.get("name", {}).get("first_name", "")
                        middle_name = record.get("name", {}).get("middle_name", "")
                        last_name = record.get("name", {}).get("last_name", "")
                        age = record.get("age")
                        title = record.get("title")
                        address1 = record.get("address", {}).get("address_1", "")
                        address2 = record.get("address", {}).get("address_2", "")
                        country = record.get("address", {}).get("country", "")
                        misc = record.get("misc")

                        # Find the next available row in the table
                        row = self.table.rowCount()

                        # Populate the table with the values
                        self.populate_table(row, id, first_name, middle_name, last_name, age, title, address1, address2, country, misc)
            else:
                print("Unexpected data format: Missing 'Employees' key")
        else:
            print("Failed to retrieve data.")

    def api_put(self): # update data
        selected_row = self.table.currentRow()
        
        if selected_row == -1:  # No row selected
            QMessageBox.warning(self, "Error", "Please select a row to update.")
            return

        # Extract updated data from the table's cells
        id = self.table.item(selected_row, 0).text()
        first_name = self.table.item(selected_row, 1).text()
        middle_name = self.table.item(selected_row, 2).text()
        last_name = self.table.item(selected_row, 3).text()
        age = self.table.item(selected_row, 4).text()
        title = self.table.item(selected_row, 5).text()
        address1 = self.table.item(selected_row, 6).text()
        address2 = self.table.item(selected_row, 7).text()
        country = self.table.item(selected_row, 8).text()
        misc = self.table.item(selected_row, 9).text()

        # Prepare the data to be sent in the PUT request
        data = self.employee_data(id, first_name, middle_name, last_name, age, title, address1, address2, country, misc)

        # Debugging output
        print(f"Data to be sent in PUT request: {data}")

        response = self.api.send_put(data)
        
        # Debugging response
        print(f"Response from PUT request: {response}")

        if response:
            print("Data updated successfully:", response)
            QMessageBox.information(self, "Success", "Employee data updated successfully.")
        else:
            print("Failed to update data.")
            QMessageBox.warning(self, "Error", "Failed to update employee data.")
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def api_delete(self): # delete data
        # Get the selected rows from the table
        selected_rows = self.table.selectedIndexes()

        if not selected_rows:  # No rows selected
            QMessageBox.warning(self, "Error", "Please select rows to delete.")
            return

        # Create a list to store the selected row indices (this avoids modifying the table while iterating)
        rows_to_delete = list(set([index.row() for index in selected_rows]))  # Remove duplicates

        # Confirm before deleting
        reply = QMessageBox.question(self, 'Delete Confirmation',
                                    f"Are you sure you want to delete {len(rows_to_delete)} employee(s)?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Iterate over the rows and delete each
            for row in sorted(rows_to_delete, reverse=True):  # Sort rows in descending order to avoid index shift
                employee_id = self.table.item(row, 0).text()  # Extract the ID of the employee

                # Send DELETE request using FlaskAPI's send_delete method
                response = self.api.send_delete(employee_id)

                if response:
                    print(f"Employee with ID {employee_id} deleted successfully:", response)
                    self.table.removeRow(row)  # Remove the row from the table
                else:
                    print(f"Failed to delete employee with ID {employee_id}.")
                    QMessageBox.warning(self, "Error", f"Failed to delete employee with ID {employee_id}.")

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(['ID', 'First Name', 'Middle Name', 'Last Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Country', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, first_name, middle_name, last_name, age, title, address1, address2, country, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(first_name))
        self.table.setItem(row, 2, QTableWidgetItem(middle_name))
        self.table.setItem(row, 3, QTableWidgetItem(last_name))
        self.table.setItem(row, 4, QTableWidgetItem(str(age)))
        self.table.setItem(row, 5, QTableWidgetItem(title))
        self.table.setItem(row, 6, QTableWidgetItem(address1))
        self.table.setItem(row, 7, QTableWidgetItem(address2))
        self.table.setItem(row, 8, QTableWidgetItem(country))
        self.table.setItem(row, 9, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.line_firstname.clear()
        self.line_middlename.clear()
        self.line_lastname.clear()
        self.line_age.clear()
        self.line_title.clear()
        self.line_address1.clear()
        self.line_address2.clear()
        self.line_country.clear()
        self.line_misc.clear()

    def update_connection_status(self):
        self.api.is_connected = self.api.check_connection()
        if self.api.is_connected:
            self.label_connection.setText("Connected to FastAPI")
        else:
            self.label_connection.setText("Failed to connect to FastAPI")

    def dark_mode(self, checked):
        if checked:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            self.setStyleSheet('')

    def closeEvent(self, event):  # Save settings when closing the app
        self.settings_manager.save_settings()  # Save settings using the manager
        event.accept()

class API: # Connects to the API
    def __init__(self):
        self.base_url = None
        self.is_connected = False

    def check_connection(self):
        if not self.base_url:
            return False  # No base_url means we can't connect
        try:
            response = requests.get(self.base_url)
            if response.status_code // 100 == 2:  # checks for any 2xx status code
                return True
        except requests.RequestException:
            pass
        return False
    
    def send_post(self, data):
        try:
            response = requests.post(f'{self.base_url}/postdata', json=data)
            
            if response.status_code // 100 == 2:  # Success: checks for 2xx status codes
                print("POST request successful:", response.json())
                return response.json()
            else:
                print(f"POST request failed with status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"POST request error: {e}")
            return None

    def send_get(self, params=None):
        try:
            # If params are provided, add them as query parameters to the URL
            url = f'{self.base_url}/getdata'
            if params:
                response = requests.get(url, params=params)  # Use params for query parameters
            else:
                response = requests.get(url)

            if response.status_code // 100 == 2:  # Success: checks for 2xx status codes
                print("GET request successful:", response.text)  # Print the raw response text

                try:
                    # Attempt to parse the JSON response
                    data = response.json()  # This will automatically parse JSON if it's valid
                    print("Parsed data:", data)
                    return data
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    return None
            else:
                print(f"GET request failed with status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"GET request error: {e}")
            return None

    def send_put(self, data):
        try:
            url = f'{self.base_url}/putdata/{data["employee_id"]}'  # Use the ID directly in the URL
            response = requests.put(url, json=data)  # Send the PUT request with the ID in the URL
            
            # Debugging output
            print(f"PUT response status code: {response.status_code}")
            print(f"PUT response text: {response.text}")
            
            if response.status_code // 100 == 2:  # Success: checks for 2xx status codes
                return response.json()
            else:
                print(f"PUT request failed with status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"PUT request error: {e}")
            return None

    def send_delete(self, employee_id):
        try:
            response = requests.delete(f'{self.base_url}/deletedata/{employee_id}')

            if response.status_code // 100 == 2:  # Success: checks for 2xx status codes
                print("DELETE request successful:", response.json())
                return response.json()
            else:
                print(f"DELETE request failed with status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"DELETE request error: {e}")
            return None

class SettingsManager: # used to load and save settings when opening and closing the app
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        server_url = self.settings.value('server_url')
        
        if size is not None:
            self.main_window.resize(size)
        if pos is not None:
            self.main_window.move(pos)
        if dark == 'true':
            self.main_window.action_dark_mode.setChecked(True)
            self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        if server_url is not None:
            self.main_window.line_server.setText(server_url)

    def save_settings(self):
        self.settings.setValue('window_size', self.main_window.size())
        self.settings.setValue('window_pos', self.main_window.pos())
        self.settings.setValue('dark_mode', self.main_window.action_dark_mode.isChecked())
        self.settings.setValue('server_url', self.main_window.line_server.text())

class AboutWindow(QDialog, about_ui): # this is the About Window
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)
        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        self.button_ok.clicked.connect(self.accept)

if __name__ == "__main__":
    app = QApplication(sys.argv) # needs to run first
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())