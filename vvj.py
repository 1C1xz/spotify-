import requests
from urllib.parse import urlencode, urlparse, parse_qs
import base64
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler


CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/callback'


def get_authorization_code():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read user-read-recently-played user-follow-read user-follow-modify"
    }
    webbrowser.open(auth_url + '?' + urlencode(params))
    

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/callback"):
                query = urlparse(self.path).query
                params = parse_qs(query)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authorization successful. You can close this window.")
                self.server.auth_code = params['code'][0]
    
    httpd = HTTPServer(('localhost', 8888), RequestHandler)
    httpd.handle_request()
    return httpd.auth_code


def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
    auth_code = get_authorization_code()
    token_info = get_access_token(auth_code)
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")


    refresh_token = token_info.get('refresh_token')
    if refresh_token:
        print(f"Refresh Token: {refresh_token}")
    

    input("Press Enter to close the script...")
