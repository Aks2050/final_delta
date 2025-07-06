from flask import Flask, request, jsonify
from delta_rest_client import DeltaRestClient

app = Flask(__name__)

# Replace with your real Delta API credentials
API_KEY = "XqJ3zyECb98GVtHqUVA2BwPeCGcHeR"
API_SECRET = "H6Mq86oOnrdXJavaVY0roR1ON460STPyGLCTvwq8eWOQvcqgTOiHd1fVE5mS"

# ✅ Corrected: Added base_url
client = DeltaRestClient(
    base_url="https://api.delta.exchange",
    api_key=API_KEY,
    api_secret=API_SECRET
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    if data:
        direction = data.get("direction")
        size = int(data.get("size", 1))

        if direction == "buy":
            order = client.create_order(
                product_id=1,  # Replace this with actual product_id for BTCUSD.P
                side='buy',
                order_type='market',
                size=size
            )
        elif direction == "sell":
            order = client.create_order(
                product_id=1,
                side='sell',
                order_type='market',
                size=size
            )
        else:
            return jsonify({"error": "Invalid direction"}), 400

        return jsonify({"status": "Order placed", "order": order}), 200

    return jsonify({"error": "No data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
