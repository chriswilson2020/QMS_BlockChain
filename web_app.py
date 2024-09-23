from flask import Flask, render_template
import os
import requests
import json
import binascii
from dotenv import load_dotenv

app = Flask(__name__)

# Function to connect to a Multichain node
def connect_to_multichain(method, params=None):
    # Load environment variables from .env file
    load_dotenv('blockchain.env')
    rpc_user = os.getenv('RPC_USER')
    rpc_password = os.getenv('RPC_PASSWORD')
    rpc_host = os.getenv('RPC_HOST')
    rpc_port = os.getenv('RPC_PORT')

    # Construct the URL for the RPC connection
    url = f'http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}'
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params if params else [],
        "jsonrpc": "2.0",
        "id": 1
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Retrieve all unique batches with their latest version
def get_all_batches():
    result = connect_to_multichain('liststreamitems', ['root'])
    latest_batches = {}

    if result and 'result' in result:
        for item in result['result']:
            json_hex = item['data']
            json_string = binascii.unhexlify(json_hex).decode('utf-8')
            batch_record = json.loads(json_string)

            if 'batch_number' in batch_record:
                batch_number = batch_record['batch_number']
                # Always overwrite the batch entry to keep the latest version
                latest_batches[batch_number] = batch_record

    # Return only the latest version of each batch
    return list(latest_batches.values())

# Flask route for the homepage
@app.route('/')
def index():
    batches = get_all_batches()
    return render_template('index.html', batches=batches)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
