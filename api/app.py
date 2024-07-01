import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
import requests

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route('/')
def home():
    return 'Hiiiii'



@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name')
    client_ip = request.remote_addr
    api_key = os.getenv('API_KEY')

    location = requests.get(f'http://api.weatherapi.com/v1/ip.json?key={api_key}&q={client_ip}').json()['city']

    temperature = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}').json()['current']['temp_c']

    response_data = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
