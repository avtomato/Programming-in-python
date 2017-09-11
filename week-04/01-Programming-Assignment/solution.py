import os
import tempfile


class File:

    def __init__(self, filename):
        self.filename = filename

    def __add__(self, other):
        with open(self.filename, 'r') as file_object_first, open(other.filename, 'r') as file_object_second:
            data = file_object_first.read() + file_object_second.read()
            new_object = File(os.path.join(tempfile.gettempdir(), 'new'))
            new_object.write(data)
            return new_object

    def __getitem__(self, item):
        with open(self.filename, 'r') as file_object:
            data = file_object.readlines()
            return data[item].strip()

    def __repr__(self):
        return '%s' % self.filename

    def write(self, s):
        with open(self.filename, 'w') as file_object:
            file_object.write(s)
