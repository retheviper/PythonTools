from time import sleep
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *
from random import randint
import os
import sys
import requests


# languages
supported_language_code: dict[str, str] = {
    'Korean': 'ko',
    'English': 'en',
    'Japanese': 'ja',
    'Chinese(China)': 'zh-CN',
    'Chinese(Taiwan)': 'zh-TW',
    'Vietnamese': 'vi',
    'Indonesian': 'id',
    'Thailand': 'th',
    'German': 'de',
    'Russian': 'ru',
    'Spanish': 'es',
    'French': 'fr'
}


# api properties for papago
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
api_url = 'https://openapi.naver.com/v1/papago/n2mt'


# variables
source: str = ''
target: str = 'ko'
line_separator: str = '\n'
original_files: list[str] = []
processing: bool = False


# drop down file list
class FileListView(QListWidget):
    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith('.vtt') and str(file_path) not in original_files:
                    # add file path to list
                    original_files.append(str(file_path))
                    # add file name to file list view
                    self.addItem(file_path.split('/')[-1])
        else:
            event.ignore()


# main view
class MainWindow(QMainWindow):

    list_view: QListWidget
    translate_button: QPushButton

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Papago vtt translator v1.0.0')
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        layout = QVBoxLayout()

        # add drop down file list
        label = self.create_file_list()
        layout.addWidget(label)
        layout.addWidget(self.list_view)

        # add remove button for file
        remove_button = self.create_remove_button()
        layout.addWidget(remove_button)

        # add language select drop box
        label, translate_language = self.create_target_language_selector()
        layout.addWidget(label)
        layout.addWidget(translate_language)

        # add translate button
        self.create_translate_button()
        layout.addWidget(self.translate_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


    # create file list
    def create_file_list(self):
        label = QLabel()
        label.setText('Drag and drop file')
        self.list_view = FileListView()
        return label


    # create remove button
    def create_remove_button(self):
        button = QPushButton()
        button.setText('Remove file')
        button.clicked.connect(self.remove_file)
        return button


    # remove file from file list
    def remove_file(self):
        global original_files
        for selected_item in self.list_view.selectedIndexes():
            index = selected_item.row()
            self.list_view.takeItem(index)
            original_files.pop(index)


    # create drop down menu
    def create_target_language_selector(self):
        label = QLabel()
        label.setText('Select target language')
        selector = QComboBox()
        selector.addItems(supported_language_code.keys())
        selector.textActivated.connect(self.set_target_language)
        return label, selector


    # set translate target language when dropdown menu selected
    def set_target_language(self, selectd: str):
        global supported_language_code
        global target
        target = supported_language_code[selectd]


    # create translate button
    def create_translate_button(self):
        self.translate_button = QPushButton()
        self.translate_button.setText('Translate')
        self.translate_button.clicked.connect(self.translate_files)
        self.translate_button.setDisabled(False)


    # read vtt file and do translate
    def translate_files(self):
        self.translate_button.setDisabled(True)
        for file_path in original_files:
            original_contents, exported_contents = self.get_content(file_path)
            if source == target:
                continue
            translated_contents = self.send_request(exported_contents)
            self.write_result(file_path, original_contents, translated_contents)
        self.translate_button.setDisabled(False)


    # get original contents from vtt file
    def get_content(self, file_path: str):
        exported_contents: dict[int, str] = {}
        global source
        with open(file_path, 'r') as file:
            original_contents: list[str] = file.readlines()
            for index, line in enumerate(original_contents):
                content = line.strip()
                if source == '' and 'Language:' in content:
                    source = content.split(':')[1].strip()
                if '-->' not in content and content != '':
                    exported_contents[index] = content
        return original_contents, exported_contents


    # send translate request to papago and get translated message
    def send_request(self, contents: dict[int, str]):
        translated_contents: dict[int, str] = {}

        headers = {
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        for index, content in contents.items():

            payload = {
                'text': content,
                'source': source,
                'target': target
            }

            response = requests.post(api_url, headers=headers, data=payload)

            if response.status_code == 200:
                body = response.json()
                translated_text: str = body['message']['result']['translatedText']
                translated_contents[index] = translated_text

                # wait for API's limitation(only 10 request per second allowed)
                sleep(0.12)
            else:
                msgBox = QMessageBox().critical(
                    self,
                    'Error',
                    response.json()['errorMessage'],
                    buttons=QMessageBox.StandardButton.Abort
                )
                if msgBox == QMessageBox.StandardButton.Abort:
                    sys.exit(255)

        return translated_contents


    # write translated contents to file
    def write_result(self, file_path: str, original_contents: list[str], translated_contents: dict[int, str]):
        contents = original_contents.copy()

        for index, content in translated_contents.items():
            if 'Language:' in content:
                contents[index] = content.replace(source, target) + line_separator
            else:
                contents[index] = content + line_separator

        root = os.path.dirname(file_path)
        file_name = os.path.basename(file_path).replace(source, target)
        target_file_path = os.path.join(root, file_name)

        with open(target_file_path, 'w') as file:
            file.writelines(contents)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()