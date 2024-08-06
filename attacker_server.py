from http.server import HTTPServer, BaseHTTPRequestHandler

class LoggingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the request path
        print(f"Received request: {self.path}")

        # Send a 200 OK response
        self.send_response(200)
        self.end_headers()

# Configure and run the logging server
ATTACKER_PORT = 9000
server_address = ('', ATTACKER_PORT)
httpd = HTTPServer(server_address, LoggingHandler)
print(f"Attacker server running on port {ATTACKER_PORT}")
httpd.serve_forever()
