from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path

HOST = "192.168.100.123" # My Private IP Address, No location leakage here!
PORT = 57790
ROOT = Path("./root").resolve()

Status = {
    "Status": "ok",
    "services": [
        { "Service": "AI-webscripts", "ok": True }
    ]
}

class Server(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)


    def send_error(self, code, message=None, explain=None):
        file_map = {
            404: os.path.join("hidden", "errors", "404.html"),
            403: os.path.join("hidden", "errors", "403.html"),
            400: os.path.join("hidden", "errors", "400.html"),
            503: os.path.join("hidden", "errors", "503.html")
        }
        
        target_file = file_map.get(code)

        if target_file:
            self.send_response(code)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            try:
                with open(target_file, "r") as f:
                    content = f.read()
                self.wfile.write(content.format(PORT=PORT).encode("utf-8"))
                return
            except Exception as e:
                print(f"Error serving {code} page: {e}")
            
        
        super().send_error(code, message, explain)
    
    def log_message(self, format, *args):
        import sys
        prefix = "[SERVER]"
        message = format % args
        sys.stderr.write(f"{prefix} {self.address_string()} - {message}\n")

    def do_POST(self):
        super().do_POST()

    def do_GET(self):
        super().do_GET()


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Server)
    print(f"Starting AI-Webscripts on http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
