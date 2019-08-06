import socket

class WebApp():
    http_response_template = (
        'HTTP/1.1 {2} {3}\r\n'
        'Content-Type: text/html; charset=utf-8\r\n'
        'Content-Length: {1}\r\n'
        'Connection: close\r\n\r\n{0}')

    def __init__(self, address, port, handlers):
        self.binding_address = socket.getaddrinfo(address, port)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(self.binding_address)
        self.handlers = handlers

    def start(self):
        self.socket.listen(1)
        print('Listening on {0}:{1}'.format(self.binding_address[0], self.binding_address[1]))
        while True:
            socket, address = self.socket.accept()
            headers, body = self.parse_request(socket.recv(1024))
            method, path = self.get_method_path(headers)
            print('{0}:{1} {2} {3}'.format(address[0], address[1], method, path))
            if method != 'GET' and body is not None:
                print(body + '\r\n')
            status_code, content_length, response = self.get_response(method, path, body)
            print('{0} {1}, {2} bytes'.format(
                status_code, self.get_status_code_reason(status_code), content_length))
            socket.send(response.encode('utf-8'))
            socket.close()

    def get_response(self, method, path, body):
        if (path, method) in self.handlers:
            status_code, response_content = self.handlers[path, method](method, path, body)
        else:
            status_code, response_content = self.default_handler(method, path, body)
        content_length = len(response_content)
        return status_code, content_length, self.http_response_template.format(
            response_content, content_length, status_code, self.get_status_code_reason(status_code))

    def default_handler(self, method, path, body):
        return 404, '<h3>{0} {1} has no handler</h3>'.format(method, path)

    def get_status_code_reason(self, status_code):
        if status_code == 200:
            return 'OK'
        if status_code == 404:
            return 'Not Found'
        return ''

    def get_method_path(self, headers):
        starting_line_parts = headers[0].split()
        method = starting_line_parts[0]
        path = starting_line_parts[1]
        return method, path

    def parse_request(self, request_bytes):
        request_str = request_bytes.decode('utf-8')
        request_parts = request_str.split('\r\n\r\n')
        headers = request_parts[0].split('\r\n')
        if len(request_parts) == 2:
            body = request_parts[1]
        else:
            body = None
        return headers, body
