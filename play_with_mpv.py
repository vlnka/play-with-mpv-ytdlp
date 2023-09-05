#!/usr/bin/env python
# Plays MPV when instructed to by a chrome extension =]

import sys
import argparse
import subprocess

if sys.version_info[0] < 3:  # python 2
    import BaseHTTPServer
    import urlparse
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(msg+'\n')
            self.wfile.close()

else:  # python 3
    import http.server as BaseHTTPServer
    import urllib.parse as urlparse
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(bytes(msg+'\n', 'utf-8'))

class Handler(BaseHTTPServer.BaseHTTPRequestHandler, CompatibilityMixin):
    def respond(self, code, body=None):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if body:
            self.send_body(body)

    def do_GET(self):
        try:
            url = urlparse.urlparse(self.path)
            query = urlparse.parse_qs(url.query)
        except:
            query = {}
        if query.get('mpv_args'):
            print("MPV ARGS:", query.get('mpv_args'))
        if "play_url" in query:
            urls = str(query["play_url"][0])         
            #pipe = subprocess.Popen(['mpv', urls] +
            #             query.get("mpv_args", []))
            ps_command = [
            'powershell', 
            '-ExecutionPolicy', 'Bypass',
            '-File', 'D:/Scripts/playwithmpv/launchmpv.ps1',
            urls
            ]
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW                    
            pipe = subprocess.Popen(ps_command, startupinfo=startup_info)
            self.respond(200, "playing...")
        else:
            self.respond(400)

def start():
    parser = argparse.ArgumentParser(description='Plays MPV when instructed to by a browser extension.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port',   type=int,  default=7531, help='The port to listen on.')
    parser.add_argument('--public', action='store_true',     help='Accept traffic from other comuters.')
    args = parser.parse_args()
    hostname = '0.0.0.0' if args.public else 'localhost'
    httpd = BaseHTTPServer.HTTPServer((hostname, args.port), Handler)
    print("serving on {}:{}".format(hostname, args.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" shutting down...")
        httpd.shutdown()

if __name__ == '__main__':
    start()

