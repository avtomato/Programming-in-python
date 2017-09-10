class FileReader:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            return open(self.file_name).read()
        except IOError:
            return ""
