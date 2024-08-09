"""
API to generate private duck addresses
"""

import json
from http.server import BaseHTTPRequestHandler

import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):

        # Extract the API key from the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data)
            api_key = body['apiKey']
        except (KeyError, json.JSONDecodeError):
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Bad request'}).encode())
            return

        # Define the URL and headers for the request to quack.duckduckgo.com
        url = "https://quack.duckduckgo.com/api/email/addresses"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        # Make the POST request to quack.duckduckgo.com
        response = requests.post(url, headers=headers)

        # Return the response from quack.duckduckgo.com
        self.send_response(response.status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response.text.encode())