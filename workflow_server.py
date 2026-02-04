#!/usr/bin/env python3
import http.server
import socketserver
import os

class WorkflowHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.path = '/workflow.html'
        return super().do_GET()

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')
    PORT = 8084
    with ReuseAddrTCPServer(("", PORT), WorkflowHandler) as httpd:
        print(f"Serving workflow dashboard at port {PORT}")
        httpd.serve_forever()