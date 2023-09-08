$env:API_HOST = 0.0.0.0
$env:API_PORT = 5000
$env:AUTH_TYPE = 'session_auth'
$env:SESSION_NAME = '_my_session_id'
python -m api.v1.app
# python main_3.py