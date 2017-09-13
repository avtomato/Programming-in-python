import socket
import time
from collections import defaultdict


class ClientError(socket.error):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

    def put(self, metric_name, metric_value, timestamp=int(time.time())):
        with socket.create_connection((self._host, self._port), self._timeout) as s:
            data = 'put %s %f %d\n' % (metric_name, metric_value, timestamp)
            try:
                s.send(data.encode('utf-8'))
            except socket.error:
                raise ClientError

    def get(self, message):
        data = defaultdict(list)
        with socket.create_connection((self._host, self._port), self._timeout) as s:
            msg = 'get %s\n' % message
            try:
                s.send(msg.encode('utf-8'))
            except socket.error:
                raise ClientError
            raw_data = s.recv(1024)
            raw_data = raw_data.decode('utf-8')
            raw_data = [i.split() for i in raw_data.split('\n')[1:] if len(i) > 1]
            [data[i[0]].append((int(i[2]), float(i[1]))) for i in raw_data]
        if message == '*':
            return data
        else:
            data = {message: data.get(message)}
            return data
