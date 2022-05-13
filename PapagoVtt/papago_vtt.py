from time import sleep
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.QtWidgets import *
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


class TranslateService(QObject):
    """
    translate service
    """

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def translate(self):
        for file_path in original_files:
            original_contents, exported_contents = self.get_content(file_path)
            if source == target:
                continue
            translated_contents = self.send_request(exported_contents)
            self.write_result(file_path, original_contents,
                              translated_contents)

    def get_content(self, file_path: str):
        """
        get original contents from vtt file
        """
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

    def send_request(self, contents: dict[int, str]):
        """
        send translate request to papago and get translated message
        """
        translated_contents: dict[int, str] = {}

        headers = {
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        for index, content in contents.items():

            next_line = contents.get(index+1)
            if next_line is not None:
                content = "{}{}{}".format(content, line_separator, next_line)

            previous_line = contents.get(index-1)
            if previous_line is not None:
                continue

            payload = {
                'text': content,
                'source': source,
                'target': target
            }

            response = requests.post(api_url, headers=headers, data=payload)

            if response.status_code == 200:
                body = response.json()
                translated_text: str = body['message']['result']['translatedText']

                if line_separator in translated_text:
                    multi_line_text = translated_text.split(line_separator)
                    translated_contents[index] = multi_line_text[0]
                    translated_contents[index+1] = multi_line_text[1]
                else:
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

    def write_result(self, file_path: str, original_contents: list[str], translated_contents: dict[int, str]):
        """
        write translated contents to file
        """
        contents = original_contents.copy()

        for index, content in translated_contents.items():
            contents[index] = content + line_separator

        for index, content in enumerate(contents):
            if 'Language:' in content:
                contents[index] = content.replace(
                    source, target) + line_separator
                break

        root = os.path.dirname(file_path)

        original_file_name = os.path.basename(file_path)
        file_name = original_file_name.replace(source, target)
        if file_name == original_file_name:
            file_name = "{}_{}".format(target, file_name)

        target_file_path = os.path.join(root, file_name)

        with open(target_file_path, 'w') as file:
            file.writelines(contents)


class FileListView(QListWidget):
    """
    drop down file list
    """

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


class MainWindow(QMainWindow):
    """
    main view
    """

    list_view: QListWidget
    translate_button: QPushButton
    service: TranslateService
    thread: QThread

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

    def create_file_list(self):
        """
        create file list
        """
        label = QLabel()
        label.setText('Drag and drop file')
        self.list_view = FileListView()
        return label

    def create_remove_button(self):
        """
        create remove button
        """
        button = QPushButton()
        button.setText('Remove file')
        button.clicked.connect(self.remove_file)
        return button

    def remove_file(self):
        """
        remove file from file list
        """
        global original_files
        for selected_item in self.list_view.selectedIndexes():
            index = selected_item.row()
            self.list_view.takeItem(index)
            original_files.pop(index)

    def create_target_language_selector(self):
        """
        create drop down menu
        """
        label = QLabel()
        label.setText('Select target language')
        selector = QComboBox()
        selector.addItems(supported_language_code.keys())
        selector.textActivated.connect(self.set_target_language)
        return label, selector

    def set_target_language(self, selectd: str):
        """
        set translate target language when dropdown menu selected
        """
        global supported_language_code
        global target
        target = supported_language_code[selectd]

    def create_translate_button(self):
        """
        create translate button
        """
        self.translate_button = QPushButton()
        self.translate_button.setText('Translate')
        self.translate_button.clicked.connect(self.translate_files)
        self.translate_button.setDisabled(False)

    def translate_files(self):
        """
        read vtt file and do translate
        """
        self.thread = QThread()
        self.service = TranslateService()
        self.service.moveToThread(self.thread)
        self.thread.started.connect(self.service.translate)
        self.service.finished.connect(self.thread.quit)
        self.service.finished.connect(self.service.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.translate_button.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.translate_button.setDisabled(True)
        )


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
