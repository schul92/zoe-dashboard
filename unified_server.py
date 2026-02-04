#!/usr/bin/env python3
import http.server
import socketserver
import os

class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve unified.html as default for root
        if self.path == '/' or self.path == '/index.html':
            self.path = '/unified.html'
        elif self.path.startswith('/workflow') and not self.path.endswith('.png'):
            self.path = '/workflow.html'
        elif self.path.startswith('/aws') and not self.path.endswith('.png'):
            self.path = '/index.html'
        # All other paths (including .png files) served as-is
        return super().do_GET()
    
    def end_headers(self):
        # Add CORS headers for mobile access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')
    PORT = 8090
    print(f"Serving unified dashboard at port {PORT}")
    with ReuseAddrTCPServer(("", PORT), UnifiedHandler) as httpd:
        httpd.serve_forever()
