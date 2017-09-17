import sys
import asyncio

storage = {}


def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def process_data(data):
    command, payload = data.split(' ', 1)
    if command == 'put':
        s = put(payload)
        return s
    elif command == 'get':
        s = get(payload)
        return s
    else:
        return 'error\nwrong command\n\n'


def put(data):
    metric_name, metric_value, timestamp = data.split()
    if metric_name not in storage:
        storage[metric_name] = {}
        storage[metric_name].update({timestamp: metric_value})
    else:
        storage[metric_name].update({timestamp: metric_value})
    return 'ok\n\n'


def get(data):
    key = data.strip()
    if key == '*':
        response = 'ok\n'
        for key, value in storage.items():
            for v in sorted(value):
                response += '%s %s %s\n' % (key, value[v], v)
        response += '\n'
        return response
    else:
        values = storage.get(key)
        if values:
            response = 'ok\n'
            for v in sorted(values):
                response += '%s %s %s\n' % (key, values[v], v)
            response += '\n'
            return response
        else:
            return 'ok\n\n'


if __name__ == "__main__":
    host, port = sys.argv[1:]
    run_server(host, port)
