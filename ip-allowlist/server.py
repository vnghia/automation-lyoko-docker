#! /usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json
import argparse


class IpAllowlistHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(content_length).decode())
        subprocess.check_call(["ip-allowlist", "add", body["ip"], body["tag"]])
        self.send_response(200)
        self.end_headers()

    def do_DELETE(self):
        content_length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(content_length).decode())
        subprocess.check_call(["ip-allowlist", "rm", body.get("ip", body.get("tag"))])
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    args = parser.parse_args()

    httpd = HTTPServer(("localhost", args.port), IpAllowlistHandler)
    httpd.serve_forever()
