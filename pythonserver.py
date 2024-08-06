from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.cookies
import uuid

class CookieHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Generate a unique session ID for each browser that loads the page
        unique_id = str(uuid.uuid4())  # Create a UUID for the session

        # Create a cookie with the unique session ID
        cookie = http.cookies.SimpleCookie()
        cookie["session_id"] = unique_id
        cookie["session_id"]["path"] = "/"  # Ensure the cookie is accessible site-wide

        # Send the response header with the cookie
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Set-Cookie", cookie.output(header='', sep=''))
        self.end_headers()

        # Read and send the HTML content
        with open("index.html", "rb") as file:  # Replace with your HTML file
            self.wfile.write(file.read())

# Configure and run the server
PORT = 8000
server_address = ('', PORT)
httpd = HTTPServer(server_address, CookieHandler)
print(f"Serving on port {PORT}")
httpd.serve_forever()