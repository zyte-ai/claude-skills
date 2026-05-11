#!/usr/bin/env python3
"""One-shot HTTP server that receives review feedback and writes it to a file."""

__version__ = "0.1.0"

import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    output_path = None

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        with open(self.output_path, "wb") as f:
            f.write(body)
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")
        threading.Thread(target=self.server.shutdown).start()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    Handler.output_path = sys.argv[1]
    srv = HTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    with open(sys.argv[1] + ".port", "w") as f:
        f.write(str(port))
    srv.serve_forever()
