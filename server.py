import http.server
import socketserver
import os
import urllib.parse
import socket

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def translate_path(self, path):
        clean_path = urllib.parse.unquote(path.split('?')[0])
        if clean_path in ('', '/'):
            clean_path = '/index.html'
            
        full_path = os.path.normpath(os.path.join(DIRECTORY, clean_path.lstrip('/')))
        if os.path.exists(full_path):
            return full_path
            
        public_path = os.path.normpath(os.path.join(DIRECTORY, 'public', clean_path.lstrip('/')))
        if os.path.exists(public_path):
            return public_path
            
        return full_path

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True

candidate_ports = [5500, 5501, 8080, 8085, 4000]
chosen_port = None
httpd = None

for port in candidate_ports:
    try:
        httpd = socketserver.TCPServer(('0.0.0.0', port), CustomHandler)
        chosen_port = port
        break
    except OSError:
        continue

if not httpd:
    httpd = socketserver.TCPServer(('0.0.0.0', 0), CustomHandler)
    chosen_port = httpd.server_address[1]

print(f"\n=======================================================", flush=True)
print(f"  Nicolás Fotografía - Servidor Local Activo", flush=True)
print(f"  ➜ Local:   http://localhost:{chosen_port}/", flush=True)
print(f"  ➜ Network: http://127.0.0.1:{chosen_port}/", flush=True)
print(f"=======================================================\n", flush=True)

httpd.serve_forever()
