from .run import Run
from .config import Config
from .auth import AuthProvider

__version__ = '1.0.7'

def login():
	auth = AuthProvider()
	if auth.is_logged():
		print('User is already logged in.')
		return
	auth.login()