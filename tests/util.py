import http.server
import io
import socketserver
import threading
import zipfile
from contextlib import contextmanager


@contextmanager
def http_server(port, files):
    """
    A context manager that starts a simple HTTP server that serves the given files.

    The files are provided in dictionary format. The keys are the file names and the values are the file contents.

    If the file content is a dictionary, the file is treated as a zip file. The keys are the file names inside the zip file and the values are the file contents.

    However, if the file content is a string, the file is treated as a text file.
    """
    # First, define the request handler
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            """
            Handle GET requests.
            """
            filename = self.path[1:]
            if filename in files:
                if isinstance(files[filename], dict):
                    self.send_zip_file(files[filename], filename)
                else:
                    self.send_txt_file(files[filename])
            else:
                self.send_error(404, "File Not Found")

        def send_zip_file(self, files, filename):
            """
            Respond with a zip file of the given name containing the given files.
            """
            # Create the zip file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in files:
                    zf.writestr(file, files[file])

            zip_data = zip_buffer.getvalue()

            # Send the HTTP headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(zip_data)))
            self.end_headers()

            # Send the zip file data
            self.wfile.write(zip_data)
        
        def send_txt_file(self, files):
            """
            Respond with a text file containing the given content.
            """
            # Send the HTTP headers
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(files)))
            self.end_headers()

            # Send the file data
            self.wfile.write(files.encode())

    # Start an HTTP server, and start serving on another thread
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
