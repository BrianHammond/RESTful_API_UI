import sys
import qdarkstyle
import requests
import json
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QSettings, QTimer
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Form as about_ui

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.flask_api = FlaskAPI() # initialize FlaskAPI class

        # Connect line_server to the update_base_url method
        self.line_server.returnPressed.connect(self.update_base_url)       

        # Update label_connection based on connection status
        self.update_connection_status()

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
        self.action_about.triggered.connect(self.show_about)
        self.action_about_qt.triggered.connect(self.about_qt)

        self.initialize_table()

    def update_base_url(self):
        new_url = f"http://{self.line_server.text()}"

        self.flask_api.base_url = new_url
        print(f"Flask API base URL updated to: {self.flask_api.base_url}")

        # check the connection if base_url is set
        if self.flask_api.base_url:
            self.flask_api.is_connected = self.flask_api.check_connection()
            self.update_connection_status()

    def api_post(self):
        self.current_date = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        id = self.current_date
        
        # Get the values from the QLineEdits
        name = self.line_name.text()  # QLineEdit for Name
        age = self.line_age.text()    # QLineEdit for Age
        title = self.line_title.text()  # QLineEdit for Title
        address1 = self.line_address1.text()  # QLineEdit for Address 1
        address2 = self.line_address2.text()  # QLineEdit for Address 2
        misc = self.line_misc.text()  # QLineEdit for Misc

        row = self.table.rowCount()
        self.populate_table(row, id, name, age, title, address1, address2, misc)

        # Prepare the data in the format expected by Flask
        data = {
            "ID": id,
            "Name": name,
            "Age": age,
            "Title": title,
            "Address": {
                "Address 1": address1,
                "Address 2": address2
            },
            "Misc": misc
        }

        # Send the data using FlaskAPI's send_post method
        response = self.flask_api.send_post(data)
        if response:
            print("Data sent successfully:", response)
        else:
            print("Failed to send data.")

        self.clear_fields()

    def api_get(self):
        print("get pressed")
        
        # Fetch the data from the Flask API using the send_get method
        data = self.flask_api.send_get()
        
        if data:
            print("Data received from API:", data)  # Log the received data

            # Check if the data contains the 'Employees' key
            if "Employees" in data:
                employees = data["Employees"]  # Get the list of employees
                
                # Initialize the table to ensure it is cleared before populating new data
                self.initialize_table()

                for record in employees:
                    if isinstance(record, dict):
                        # Extract values for each record
                        id = record.get("ID")
                        name = record.get("Name")
                        age = record.get("Age")
                        title = record.get("Title")
                        address1 = record.get("Address", {}).get("Address 1", "")
                        address2 = record.get("Address", {}).get("Address 2", "")
                        misc = record.get("Misc")

                        # Find the next available row in the table
                        row = self.table.rowCount()

                        # Populate the table with the values
                        self.populate_table(row, id, name, age, title, address1, address2, misc)
            else:
                print("Unexpected data format: Missing 'Employees' key")
        else:
            print("Failed to retrieve data.")

    def api_put(self):
        # Get the selected row from the table
        selected_row = self.table.currentRow()
        
        if selected_row == -1:  # No row selected
            QMessageBox.warning(self, "Error", "Please select a row to update.")
            return

        # Extract updated data from the table's cells
        id = self.table.item(selected_row, 0).text()
        name = self.table.item(selected_row, 1).text()
        age = self.table.item(selected_row, 2).text()
        title = self.table.item(selected_row, 3).text()
        address1 = self.table.item(selected_row, 4).text()
        address2 = self.table.item(selected_row, 5).text()
        misc = self.table.item(selected_row, 6).text()

        # Prepare the data to be sent in the PUT request
        data = {
            "ID": id,
            "Name": name,
            "Age": age,
            "Title": title,
            "Address": {
                "Address 1": address1,
                "Address 2": address2
            },
            "Misc": misc
        }

        # Send the updated data using FlaskAPI's send_put method
        response = self.flask_api.send_put(data)
        if response:
            print("Data updated successfully:", response)
            QMessageBox.information(self, "Success", "Employee data updated successfully.")
        else:
            print("Failed to update data.")
            QMessageBox.warning(self, "Error", "Failed to update employee data.")

        self.table.resizeColumnsToContents()

    def api_delete(self):
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
                response = self.flask_api.send_delete(employee_id)

                if response:
                    print(f"Employee with ID {employee_id} deleted successfully:", response)
                    self.table.removeRow(row)  # Remove the row from the table
                else:
                    print(f"Failed to delete employee with ID {employee_id}.")
                    QMessageBox.warning(self, "Error", f"Failed to delete employee with ID {employee_id}.")

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, name, age, title, address1, address2, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(age))
        self.table.setItem(row, 3, QTableWidgetItem(title))
        self.table.setItem(row, 4, QTableWidgetItem(address1))
        self.table.setItem(row, 5, QTableWidgetItem(address2))
        self.table.setItem(row, 6, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.line_name.clear()
        self.line_age.clear()
        self.line_title.clear()
        self.line_address1.clear()
        self.line_address2.clear()
        self.line_misc.clear()

    def update_connection_status(self):
        self.flask_api.is_connected = self.flask_api.check_connection()
        if self.flask_api.is_connected:
            self.label_connection.setText("Connected to FlaskAPI")
        else:
            self.label_connection.setText("Failed to connect to FlaskAPI")

    def dark_mode(self, checked):
        if checked:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            self.setStyleSheet('')

    def show_about(self): #loads the About window
        self.about_window = AboutWindow(dark_mode=self.action_dark_mode.isChecked())
        self.about_window.show()

    def about_qt(self): #loads the About Qt window
        QApplication.aboutQt()

    def closeEvent(self, event):  # Save settings when closing the app
        self.settings_manager.save_settings()  # Save settings using the manager
        event.accept()

class FlaskAPI: # Connects to the Flask API
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
            # Send a POST request to the Flask API
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
        
    def send_get(self):
        try:
            # Send a GET request to the Flask API
            response = requests.get(f'{self.base_url}/getdata')

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
            # Send PUT request to Flask API
            response = requests.put(f'{self.base_url}/putdata', json=data)
            if response.status_code // 100 == 2:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"PUT request error: {e}")
            return None

    def send_delete(self, employee_id):
        try:
            # Send a DELETE request to the Flask API
            response = requests.delete(f'{self.base_url}/deletedata', json={"ID": employee_id})

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

class AboutWindow(QWidget, about_ui): # Configures the About window
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)

        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

if __name__ == "__main__":
    app = QApplication(sys.argv) # needs to run first
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())