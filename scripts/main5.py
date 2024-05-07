import sys
import csv
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QLabel, QTextEdit, QDialog, QTabWidget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtWidgets import *
import pyttsx3


engine = pyttsx3.init()
engine.say("LinkedIn Automation Software Is Opening")
engine.runAndWait()

class MessageDialog(QDialog):
    def __init__(self, driver, parent=None):
        super(MessageDialog, self).__init__(parent)
        self.driver = driver
        self.setWindowTitle("Compose Message")
        layout = QVBoxLayout(self)
        self.message_edit = QTextEdit()
        layout.addWidget(self.message_edit)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)
        
    def send_message(self):
        message = self.message_edit.toPlainText()
        try:
            # Assuming self.driver is the WebDriver instance
            # Locate the message input field and fill it with the message
            message_input = self.driver.find_element_by_css_selector("input[aria-label='Write a message...']")
            message_input.send_keys(message)

            # Locate and click the send button
            send_button = self.driver.find_element_by_css_selector("button[data-control-name='send']")
            send_button.click()
            
            # Close the message dialog
            self.close()
        except Exception as e:
            # Handle any exceptions that may occur during the sending process
            
            QMessageBox.warning(self, "Error", "Failed to send message. Error: " + str(e))
            self.close()

class LinkedInApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkedIn Automation Tool")
        self.setGeometry(100, 100, 600, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Tab widget for navigation
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add tabs for different functionalities
        self.login_tab = QWidget()
        self.messaging_tab = QWidget()
        self.connecting_tab = QWidget()
        self.tab_widget.addTab(self.login_tab, "Login")
        self.tab_widget.addTab(self.messaging_tab, "Messaging")
        self.tab_widget.addTab(self.connecting_tab, "Connecting")

        # Setup widgets for each tab
        self.setup_login_tab()
        self.setup_messaging_tab()
        self.setup_connecting_tab()
        
        self.driver = None


    def setup_login_tab(self):
        # Add widgets and functionality for login tab
        layout = QVBoxLayout(self.login_tab)

        self.email_label = QLabel("Email:")
        layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authorize_linkedin)
        layout.addWidget(self.login_button)

    def setup_messaging_tab(self):
        # Add widgets and functionality for messaging tab
        layout = QVBoxLayout(self.messaging_tab)
        
        self.send_message_button = QPushButton("Send Message to Connections")
        self.send_message_button.clicked.connect(self.open_message_gui)
        layout.addWidget(self.send_message_button)

        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        layout.addWidget(self.output_log)

    def setup_connecting_tab(self):
        # Add widgets and functionality for connecting tab
        layout = QVBoxLayout(self.connecting_tab)

        self.keyword_label = QLabel("Keyword:")
        layout.addWidget(self.keyword_label)

        self.keyword_input = QLineEdit()
        layout.addWidget(self.keyword_input)

        self.location_label = QLabel("Location:")
        layout.addWidget(self.location_label)

        self.location_input = QLineEdit()
        layout.addWidget(self.location_input)

        self.search_button = QPushButton("Search and Connect")
        self.search_button.clicked.connect(self.search_and_connect)
        layout.addWidget(self.search_button)

        self.output_log_connecting = QTextEdit()
        self.output_log_connecting.setReadOnly(True)
        layout.addWidget(self.output_log_connecting)

    def open_message_gui(self):
        message_dialog = MessageDialog(self.driver, self)
        message_dialog.exec_()

    def authorize_linkedin(self):
        # Get email and password from input
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            engine.say("Please enter both email and password.")
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()

        # Open LinkedIn login page
        self.driver.get("https://www.linkedin.com/login")

        try:
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            email_input.send_keys(email)

            # Enter password
            password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
            password_input.send_keys(password)

            # Click login button
            login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
            login_button.click()

            # Wait for login process to complete
            WebDriverWait(self.driver, 10).until(EC.url_contains("feed"))

            # Display success message
            engine.say("Login successful.")

            self.output_log.append("Login successful.")
        except Exception as e:
            # Display error message
            engine.say("Login failed.")
            self.output_log.append("Login failed. Error: " + str(e))

    def search_and_connect(self):
        if not self.driver:
            QMessageBox.warning(self, "Error", "Please log in first.")
            return

        # Get keyword from input
        keyword = self.keyword_input.text()

        if not keyword:
            engine.say("Please enter a keyword to search.")
            QMessageBox.warning(self, "Error", "Please enter a keyword to search.")
            return

        try:
            # Navigate to search page
            search_url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords={keyword}'
            print("Searching...")
            self.driver.get(search_url)
            print("Search Found")
            print("Waiting...")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "entity-result__divider")))
            print("Wait Complete")
            # Loop to send connection requests
            # Collect all buttons with the specified class
            print("Collecting Buttons...")
            # Wait for the div containing connect buttons to be present
            try:
                connect_buttons_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".entity-result__actions.entity-result__divider"))
                )
                print(len(connect_buttons_div))
            except TimeoutException:
                print("Timed out waiting for connect buttons to appear.")
                connect_buttons_div = []
            
            # Counter to keep track of connection requests sent
            connect_requests_sent = 0

            for button_div in connect_buttons_div:
                # if connect_requests_sent >5:
                #         break
                try:
                    button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".entity-result__actions.entity-result__divider>div>button.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view"))
                    )
                    button_text = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".entity-result__actions.entity-result__divider>div>button.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view>span.artdeco-button__text"))
                    ).text
                    print(button_text)
                    
                    if button_text == "Connect":
                        print(button_text)
                        button.click()
                        print("Button Clicked")
                        send_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-modal__actionbar.ember-view.text-align-right>button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1"))
                        )
                        send_button_text = send_button.text
                        # print(send_button_text)
                        if send_button_text == "Send":
                            time.sleep(2)
                            send_button.click()
                            self.output_log.append("Connection request sent.")
                            connect_requests_sent += 1
                    else:
                        print("Connect Button Not Found")
                    
                except NoSuchElementException:
                    print("Button not found or text not available")
            
        except Exception as e:
            self.output_log.append("Error: " + str(e))

if __name__ == "__main__":
    app = QApplication([])
    window = LinkedInApp()
    window.show()
    sys.exit(app.exec_())
