import os
import json
import jwt
import datetime as dt
import pyhectiqlab.ops as ops

from http.server import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open_new
from pathlib import Path
import urllib.parse as urlparse
from urllib.parse import parse_qs

import pyhectiqlab.settings as settings

class HTTPServerHandler(BaseHTTPRequestHandler):
    """
    HTTP Server callbacks to handle OAuth redirects
    """
    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if ("access_token" in self.path):
            parsed = urlparse.urlparse(self.path)
            s = parse_qs(parsed.query)
            self.server.access_token = s["access_token"]
            self.server.refresh_token = s["refresh_token"]
            self.server.expiration = s["expiration"]
            self.wfile.write(bytes('<html><h1>You may now close this window.'+ '</h1></html>', 'utf-8'))
        else:
            self.wfile.write(bytes('<html><h1>Hum. Cannot find the token...'+ '</h1></html>', 'utf-8'))

    def log_message(self, format, *args):
        # Mute
        return

class AuthProvider:
    """
    Class used to handle oAuth
    """
    def __init__(self, port=8082):
        self.port = str(port)
        self._load_tokens()

        # Refresh token if access_token is expired
        if self.tokens:
            if "access_token" in self.tokens:
                if self._is_expired(self.tokens["access_token"])==True:
                    self._refresh_token()

        return
    
    def is_logged(self):
        if self.tokens is None:
            return False
        
        if "access_token" in self.tokens:
            if self._is_expired(self.tokens["access_token"])==False:
                return True
            else:
                self._refresh_token()
                return self.is_logged()
        return False
    
    def login(self):
        if self.is_logged():
            return 
        self._refresh_token()
    
    def logout(self):
        self.tokens = None
        self._save_local_tokens({})

    def login_with_password(self, username:str, password:str):
        tokens = ops.login(username, password)
        if tokens.get('status_code')==401:
            return False
        self._save_local_tokens(tokens)
        self.tokens = tokens
        return True

    @property
    def token(self):
        self.login()
        return self.tokens["access_token"]
    
    def _get_expiration_date(self, token):
        if token is None:
            return None
            
        return jwt.decode(token, verify=False)['exp']
    
    def _is_expired(self, token):
        d = self._get_expiration_date(token)
        if d is None:
            return True
        return dt.datetime.now().timestamp() > d
    
    def _get_access_token(self):
        """
        Get access token from server
        """
        httpServer = HTTPServer(('localhost', int(self.port)),
                lambda request, address, server: HTTPServerHandler(request, address, server))
       
        access_uri = f"{settings.app_url}/api-login?redirectURL=http://0.0.0.0:{self.port}/"
        open_new(access_uri)
        # This function will block until it receives a request
        httpServer.handle_request()
        tokens = {"access_token": httpServer.access_token[0], 
         "refresh_token": httpServer.refresh_token[0], 
         "expiration" :httpServer.expiration[0]}
    
        self._save_local_tokens(tokens)
        self.tokens = tokens
        
        # Close socket (server will be shutdown at return)
        httpServer.socket.close()
        print("Login completed.")
        return 

    def _refresh_token(self):
        if self.tokens is None or self.tokens=={}:
            self._get_access_token()
            return

        if "refresh_token" in self.tokens:
            tokens = ops.refresh_token(self.tokens["refresh_token"])
            self._save_local_tokens(tokens)
            self.tokens = tokens
            return
        
        return

    def _load_tokens(self):
        self.tokens = None
        if os.path.isfile(self.tokens_path):
            file = open(self.tokens_path, "rb")
            self.tokens = json.load(file)
            file.close()
        return

    def _save_local_tokens(self, tokens):
        """
        Save the tokens locally
        """
        if not os.path.exists(self.tokens_folder):
            os.mkdir(self.tokens_folder)

        f = open(self.tokens_path, 'w')
        f.write(json.dumps(tokens))
        f.close()

    @property
    def tokens_path(self):
        home = str(Path.home())
        config_folder = os.path.join(home, '.hectiqlab')
        return os.path.join(config_folder, 'creds.json')
    
    @property
    def tokens_folder(self):
        home = str(Path.home())
        config_folder = os.path.join(home, '.hectiqlab')
        return config_folder
