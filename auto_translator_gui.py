import sys
import json
import os
import requests
from deep_translator import GoogleTranslator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QScrollArea, QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QCheckBox, QLineEdit, QLabel, QTextEdit
)

from PyQt5.QtWidgets import QMessageBox

# Global variables to store the selected file paths
appname_file_path = None
storepage_file_path = None

example_store_page_json = {"language":"english","appid":2976180,"name":"A difficult game about spelunking"}

# app_id_override = ""
# app_name_override = ""
# example_store_page_json.language="english"
# example_store_page_json.appid = 2976180
# example_store_page_json.name = "A difficult game about spelunking"

# JSON keys to filter out
jsonKeyNamesToFilterOut = ["language", "appid", "itemid"]

my_steam_app_ids = ["2360880","2530060","2496790","2476040","2328280","1445370"]

def sanitize_translated_value(rawValue):
    replacement_string = rawValue
    replacement_string = replacement_string.replace("{steam_app_image} ", "{STEAM_APP_IMAGE}")
    replacement_string = replacement_string.replace("{steam_app_image}", "{STEAM_APP_IMAGE}")
    replacement_string = replacement_string.replace("[img] ", "[img]")
    replacement_string = replacement_string.replace(" [/img]", "[/img]")
    return replacement_string


def process_appname_json(app_id_override, app_name_override, in_text_area):
    example_store_page_json["appid"] = app_id_override
    example_store_page_json["name"] = app_name_override
    
    baseTranslationFile = example_store_page_json    
    appidOverride = baseTranslationFile.get('appid', -1)

    translationEntriesJsonFileName = "includes/appname_translations_file"
    with open(f"{translationEntriesJsonFileName}.json", "r") as translation_file:
        data = json.load(translation_file)

    for entry in data["entries"]:
        google_language_id = entry["language"]
        google_language_display_name = google_language_id

        if appidOverride != -1:
            entry["appid"] = appidOverride

        google_language_id = map_language_id(google_language_id)
        translated_val = translate_and_save(entry, baseTranslationFile, google_language_id, "appid")
        text_entry = in_text_area.toPlainText()
        text_entry = f"{text_entry}\n{google_language_display_name}:{translated_val}"
        in_text_area.setPlainText(text_entry)

def process_appname_json_old(file_path, in_text_area):
    with open(file_path, "r") as file:
        baseTranslationFile = json.load(file)
        appidOverride = baseTranslationFile.get('appid', -1)

        translationEntriesJsonFileName = "includes/appname_translations_file"
        with open(f"{translationEntriesJsonFileName}.json", "r") as translation_file:
            data = json.load(translation_file)

        for entry in data["entries"]:
            google_language_id = entry["language"]
            google_language_display_name = google_language_id

            if appidOverride != -1:
                entry["appid"] = appidOverride

            google_language_id = map_language_id(google_language_id)
            translated_val = translate_and_save(entry, baseTranslationFile, google_language_id, "appid")
            text_entry = in_text_area.toPlainText()
            text_entry = f"{text_entry}\n{google_language_display_name}:{translated_val}"
            in_text_area.setPlainText(text_entry)


def process_storepage_json(file_path):
    with open(file_path, "r") as file:
        baseTranslationFile = json.load(file)
        itemidOverride = baseTranslationFile.get('itemid', -1)

        translationEntriesJsonFileName = "includes/storepage_translations_file"
        with open(f"{translationEntriesJsonFileName}.json", "r") as translation_file:
            data = json.load(translation_file)

        for entry in data["entries"]:
            google_language_id = entry["language"]

            if itemidOverride != -1:
                entry["itemid"] = itemidOverride

            google_language_id = map_language_id(google_language_id)
            translate_and_save(entry, baseTranslationFile, google_language_id, "itemid")

def map_language_id(google_language_id):
    language_map = {
        "brazilian": "pt",
        "latam": "es",
        "sc_schinese": "zh-TW",
        "tchinese": "zh-TW",
        "schinese": "zh-CN",
        "koreana": "ko"
    }
    return language_map.get(google_language_id, google_language_id)

def translate_and_save(entry, baseTranslationFile, google_language_id, id_key):
    return_val = ""
    for fieldName, fieldValue in baseTranslationFile.items():
        if fieldName in jsonKeyNamesToFilterOut:
            continue
        if len(fieldValue) > 1:
            print(f"translating {fieldValue} to {google_language_id}")
            #translatedFieldValue = translator.translate(fieldValue, src='en', dest=google_language_id).text            
            translatedFieldValue = GoogleTranslator(source='en', target=google_language_id).translate(fieldValue)
            translatedFieldValue = translatedFieldValue.lower()
            entry[fieldName] = translatedFieldValue
            if fieldName == "name":
                return_val = translatedFieldValue
    

    output_directory = f'./exports/{id_key}/export_{entry[id_key]}'
    os.makedirs(output_directory, exist_ok=True)

    json_string = json.dumps(entry).lower()
    sanitized_json_string = sanitize_translated_value(json_string)

    output_file_dir = f'{output_directory}/{id_key}_{entry[id_key]}_{entry["language"]}.json'
    with open(output_file_dir, "w") as output_file:
        output_file.write(sanitized_json_string)
        print(f"Translation complete. Exported {output_file_dir}.")
        
    return return_val
        
def make_image_clickable(image_label, steam_url):
    try:
        def open_steam_url(event):
            QDesktopServices.openUrl(QUrl(steam_url))
        
        image_label.mousePressEvent = open_steam_url
    except Exception as e:
        print(f"Error setting up mouse event: {e}")


        
def load_steam_images(steam_app_ids, grid_layout):
    for i, app_id in enumerate(steam_app_ids):
        image_url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg?t=1723472552"
        steam_url = f"https://store.steampowered.com/app/{app_id}"

        # Load image using requests
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # Create label and set the pixmap
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio))

            # Make image clickable
            make_image_clickable(image_label, steam_url)

            # Add image to grid layout
            row = i // 3
            col = i % 3
            grid_layout.addWidget(image_label, row, col)
        else:
            print(f"Failed to load image for app ID {app_id}")


        
class TranslationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.game_name_input_label = QLabel("app name:")
        layout.addWidget(self.game_name_input_label)
        
        # # Add array input field for Steam App IDs
        self.game_name_input = QLineEdit(self)
        self.game_name_input.setPlaceholderText("Enter game name here:")    
        self.game_name_input.setText("Improbability Control Bureau")
        layout.addWidget(self.game_name_input)
        
        self.app_id_input_label = QLabel("app id:")
        layout.addWidget(self.app_id_input_label)

        self.app_id_input = QLineEdit(self)
        self.app_id_input.setPlaceholderText("Enter app id :")        
        self.app_id_input.setText("2530060")
        layout.addWidget(self.app_id_input)        
        
        self.dynamic_link_label = QLabel(self)
        self.dynamic_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.dynamic_link_label.setOpenExternalLinks(True)
        layout.addWidget(self.dynamic_link_label)
        
        
        # # Connect the app_id_input to a function that updates the link
        # self.app_id_input.textChanged.connect(self.update_dynamic_link)

        # self.appname_label = QLabel("Select appname JSON file:")
        # layout.addWidget(self.appname_label)

        # appname_button = QPushButton("Select appname JSON")
        # appname_button.clicked.connect(self.select_appname_file)
        # layout.addWidget(appname_button)

        self.storepage_label = QLabel("Select storepage JSON file:")
        layout.addWidget(self.storepage_label)

        storepage_button = QPushButton("Select storepage JSON")
        storepage_button.clicked.connect(self.select_storepage_file)
        layout.addWidget(storepage_button)

        process_button = QPushButton("Process Files")
        process_button.clicked.connect(self.process_files)
        layout.addWidget(process_button)

        self.app_translation_label = QLabel("translated app names. If you published your steam store page already, give this to steam support to update your translated game titles: ")
        layout.addWidget(self.app_translation_label)
        
        self.text_area = QTextEdit()
        self.text_area.setFontPointSize(14)
        self.text_area.setMinimumHeight(100)
        layout.addWidget(self.text_area)
        
        self.app_translation_label = QLabel("Help a brother out. Wishlist my games!!! :) ")
        layout.addWidget(self.app_translation_label)
        
        

        # Scroll area to display images in a grid layout
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        image_widget = QWidget(scroll_area)
        self.grid_layout = QGridLayout(image_widget)
        scroll_area.setWidget(image_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setWindowTitle("Scott HF Dunbar's Translation App")
        self.setGeometry(300, 300, 700, 660)
        
        # try:
            # Load Steam app images into grid
        steam_app_ids = [app_id.strip() for app_id in my_steam_app_ids if app_id.strip().isdigit()]
        load_steam_images(steam_app_ids, self.grid_layout)
        # except Exception as e:
        #     print(f"Caught an unexpected exception: {e}")
            # Handle other exceptions if needed

    def update_dynamic_link(self):
        app_id = self.app_id_input.text().strip()
        if app_id.isdigit():
            url = f"https://partner.steamgames.com/admin/game/edit/{app_id}?activetab=tab_localization"
            print(f"clicked url: {url}")
            self.dynamic_link_label.setText(f'<a href="{url}">Edit Game Localization in Steamworks</a>')
        else:
            self.dynamic_link_label.setText("")
            
    def select_appname_file(self):
        global appname_file_path
        appname_file_path, _ = QFileDialog.getOpenFileName(self, "Select appname JSON", "", "JSON Files (*.json)")
        if appname_file_path:
            self.appname_label.setText(f"Selected: {os.path.basename(appname_file_path)}")

    def select_storepage_file(self):
        global storepage_file_path
        storepage_file_path, _ = QFileDialog.getOpenFileName(self, "Select storepage JSON", "", "JSON Files (*.json)")
        if storepage_file_path:
            self.storepage_label.setText(f"Selected: {os.path.basename(storepage_file_path)}")

    def process_files(self):
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Processing in progress...")
        msg.setWindowTitle("Processing")
        msg.setStandardButtons(QMessageBox.NoButton)  # Disable close button while processing
        msg.show()
        
        app_name_override = self.game_name_input.text().strip()
        app_id_override = int(self.app_id_input.text().strip())

        process_appname_json(app_id_override, app_name_override, self.text_area)
        # Process files
        #if appname_file_path:
            #process_appname_json(appname_file_path, self.text_area)
            
        if storepage_file_path:
            process_storepage_json(storepage_file_path)
        
        # Update the status when processing is complete
        msg.setText("Processing complete!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()  # Wait for the user to close the message box
        

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = TranslationApp()
        ex.show()
    except Exception as e:
        print(f"Caught an unexpected exception: {e}")
        # Handle other exceptions if needed
    sys.exit(app.exec_())
