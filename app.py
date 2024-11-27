import requests
from flask import Flask, request, jsonify
app = Flask(__name__)

def send_simple_message():
  	return requests.post(
  		"https://api.mailgun.net/v3/sandboxf61647df827b41399abcbcbfb39bf811.mailgun.org/messages",
  		auth=("api", "8a513d71a575989541ba1e08bdd99e7b-c02fd0ba-cc0fba04"),
  		data={"from": "devika.c@atriauniversity.edu.in <mailgun@sandboxf61647df827b41399abcbcbfb39bf811.mailgun.org>",
  			"to": ["devika.c008@gmail.com"],
  			"subject": "Hello Devika",
  			"text": "Testing some Mailgun awesomeness!"})
   
@app.route('/', methods=['POST'])
def email():
	send_simple_message()
	return "Email sent!"

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook received!")
    data = request.get_json()
    print(data)
    return jsonify({"message":"OK"})
if __name__ == '__main__':
	app.run(debug=True)