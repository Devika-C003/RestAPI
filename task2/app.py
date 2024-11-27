from flask import Flask, jsonify, request, redirect
import requests
app = Flask(__name__)
# GitHub OAuth configuration
CLIENT_ID = "Ov23li3cEab6ACjQTizt"
CLIENT_SECRET = "9d2a497128565b2c32a16fc91baae203f3ca7e68"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
API_BASE_URL = "https://api.github.com/user"

USERNAME = "admin"
PASSWORD = "password123"
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Constellations API!"}), 200

# Basic Auth

@app.route('/basic-auth', methods=['GET'])
def basic_auth():
    # Retrieve Basic Auth credentials
    auth = request.authorization
    
    # Check if credentials are provided and valid
    if auth and auth.username == USERNAME and auth.password == PASSWORD:
        return jsonify({"message": "Access granted! Welcome to the protected resource."}), 200
    else:
        # Return 401 if credentials are missing or invalid
        return jsonify({"error": "Unauthorized access. Please provide valid credentials."}), 401
    
# Bearer Token Auth
# Predefined Bearer Token
VALID_TOKEN = "devika123"

@app.route('/bearer-auth', methods=['GET'])
def bearer_auth():
    # Get the Authorization header
    auth_header = request.headers.get("Authorization")
    
    # Validate the token
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]  # Extract the token part
        if token == VALID_TOKEN:
            return jsonify({"message": "Access granted! Welcome to the Bearer protected resource."}), 200
        else:
            return jsonify({"error": "Invalid Bearer Token."}), 401
    else:
        return jsonify({"error": "Bearer Token missing or invalid."}), 401
    
#OAuth
# OAuth route to redirect to GitHub's authorization page
@app.route('/oauth')
def oauth():
    authorization_url = f"{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}&scope=user"
    return redirect(authorization_url)

# Login route to initiate the OAuth flow
@app.route('/login')
def login():
    return redirect(url_for('oauth'))

# Callback route to handle GitHub's response
@app.route('/callback')
def callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    if not code:
        return "Authorization failed.", 400

    # Exchange the authorization code for an access token
    token_response = requests.post(
        TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
        }
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return "Failed to obtain access token.", 400

    # Use the access token to fetch the user's information
    user_response = requests.get(
        API_BASE_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
    )

    user_data = user_response.json()
    return f"Logged in as: {user_data.get('login')}"
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
