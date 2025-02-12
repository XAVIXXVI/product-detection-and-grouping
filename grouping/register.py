import requests
import os

CONSUL_HOST = os.environ.get('CONSUL_HOST', 'consul')
CONSUL_PORT = os.environ.get('CONSUL_PORT', '8500')
SERVICE_NAME = os.environ.get('SERVICE_NAME')
SERVICE_PORT = os.environ.get('SERVICE_PORT')


def register_service():
    consul_url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    service_data = {
        "Name": SERVICE_NAME,
        "Port": int(SERVICE_PORT)
        # Add other required fields here, such as Address, Tags, Check, etc.
    }
    response = requests.put(consul_url, json=service_data)
    if response.status_code == 200:
        print(f"Service '{SERVICE_NAME}' registered successfully with Consul.")
    else:
        print(f"Failed to register service '{SERVICE_NAME}' with Consul. Status code: {response.status_code}")

if __name__ == "__main__":
    register_service()