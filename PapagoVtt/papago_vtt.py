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
    percent_each = pyqtSignal(int)
    percent_all = pyqtSignal(int)
    exception_on_request = pyqtSignal(Exception)

    def translate(self):
        """
        do translate
        """
        self.percent_all.emit(0)
        content_count = len(original_files)
        i = 0
        for file_path in original_files:
            original_contents, exported_contents = self.get_content(
                file_path)

            if source == target:
                continue

            try:
                translated_contents = self.send_request(exported_contents)
            except Exception as e:
                self.exception_on_request.emit(e)
                return

            self.write_result(file_path, original_contents,
                              translated_contents)

            self.percent_each.emit(0)
            i += 1
            self.percent_all.emit(self.calculate_percent(i, content_count))

        self.finished.emit()

    def calculate_percent(self, current, all):
        """
        calculate percentage
        """
        return int(current/all*100)

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

        content_length = len(contents)
        i = 0
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
                raise Exception(response.json()['errorMessage'])

            i += 1
            self.percent_each.emit(self.calculate_percent(i, content_length))

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

    widget: QWidget
    list_view: QListWidget
    translate_button: QPushButton
    service_thread: QThread
    service: QObject
    progress_each: QProgressBar
    progress_all: QProgressBar

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

        # add progress bar
        label = self.create_progress_bar_each()
        layout.addWidget(label)
        layout.addWidget(self.progress_each)
        label = self.create_progress_bar_all()
        layout.addWidget(label)
        layout.addWidget(self.progress_all)

        # add translate button
        self.create_translate_button()
        layout.addWidget(self.translate_button)

        # set thread and service
        self.service_thread = QThread()
        self.service = TranslateService()
        self.service.moveToThread(self.service_thread)
        self.service_thread.started.connect(self.service.translate)
        self.service_thread.finished.connect(self.service_thread.deleteLater)
        self.service.percent_each.connect(self.update_progress_each)
        self.service.percent_all.connect(self.update_progress_all)
        self.service.exception_on_request.connect(self.on_fail)
        self.service.finished.connect(self.service_thread.quit)
        self.service.finished.connect(self.service.deleteLater)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)

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

    def create_progress_bar_each(self):
        """
        create progress bar for each file
        """
        label = QLabel()
        label.setText('Progress (Each)')
        self.progress_each = QProgressBar(self)
        return label

    def create_progress_bar_all(self):
        """
        create progress bar for all file
        """
        label = QLabel()
        label.setText('Progress (All)')
        self.progress_all = QProgressBar(self)
        return label

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
        self.service_thread.start()

        self.translate_button.setDisabled(True)
        self.service_thread.finished.connect(
            lambda: self.translate_button.setEnabled(True)
        )

    def update_progress_each(self, value):
        """
        update progress bar for each files
        """
        self.progress_each.setValue(value)

    def update_progress_all(self, value):
        """
        update progress bar for all files
        """
        self.progress_all.setValue(value)

    def on_fail(self, exception: Exception):
        """
        print error message and exit
        """
        msgBox = QMessageBox().critical(
            self,
            'Error',
            str(exception),
            buttons=QMessageBox.StandardButton.Abort
        )
        if msgBox == QMessageBox.StandardButton.Abort:
            sys.exit(255)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
