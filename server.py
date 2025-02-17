from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import smtplib
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

EMAIL_ADDRESS = "dskazuto@gmail.com"  # Change this
EMAIL_PASSWORD = "esqhaibpzrwtjdvx"    # Use an App Password if using Gmail

class EmailHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight request (OPTIONS)."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/send_email":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            email = data.get("email", "")

            if not email:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid Email")
                return

            try:
                # Send email
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                message = f"Subject: Antivirus Alert\n\nYour device contains junk files. Please scan using our tool."
                server.sendmail(EMAIL_ADDRESS, email, message)
                server.quit()

                logging.info(f"Email sent to {email}")

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Email sent successfully!")

            except Exception as e:
                logging.error(f"Error sending email: {e}")
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode("utf-8"))

# Start the server
server_address = ("", 8080)
httpd = HTTPServer(server_address, EmailHandler)
logging.info("Server running on port 8080...")
httpd.serve_forever()
