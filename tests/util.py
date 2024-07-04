import http.server
import io
import socketserver
import threading
import zipfile
from contextlib import contextmanager


@contextmanager
def http_server(port, files):
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            filename = self.path[1:]
            if filename in files:
                if isinstance(files[filename], dict):
                    self.send_zip_file(files[filename], filename)
                else:
                    self.send_txt_file(files[filename])
            else:
                self.send_error(404, "File Not Found")

        def send_zip_file(self, files, filename):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in files:
                    zf.writestr(file, files[file])

            zip_data = zip_buffer.getvalue()

            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(zip_data)))
            self.end_headers()

            self.wfile.write(zip_data)
        
        def send_txt_file(self, files):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(files)))
            self.end_headers()

            self.wfile.write(files.encode())

    httpd = None
    server_thread = None
    try:
        httpd = socketserver.TCPServer(("", port), RequestHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()

        yield
    finally:
        if httpd is not None:
            httpd.shutdown()
        if server_thread is not None:
            server_thread.join()

if __name__ == "__main__":
    with http_server(8000, {
        'submission.zip': {
            'submission.py': 'print("Hello, World!")'
        }
    }):
        import requests
        res = requests.get('http://localhost:8000/submission.zip')
        with open('test.zip', 'wb') as f:
            f.write(res.content)
