from flask import Flask
from webhook import WebhookHandler

app = Flask(__name__)

@app.route("/webhook/", methods=["POST", "GET"])
def webhook():
    handler = WebhookHandler(verify_token="DavidMVToken")
    return handler.handle_request()

if __name__ == "__main__":
    app.run(debug=True)
