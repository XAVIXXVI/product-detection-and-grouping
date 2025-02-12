from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
import requests
import os
from consul import Consul
import socket

def get_container_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


# Create a Consul client instance (assuming Consul is on the same network)
consul = Consul(host='consul')


# Function to fetch service details by name
def get_service_details(service_name):
    services = consul.agent.services()
    for service_id, service_info in services.items():
        if service_info['Service'] == service_name:
            return service_info
    return None


# Get the IP address of the "detection-service" container
detection_service_ip = get_container_ip('django-server-detection-1')
grouping_service_ip = get_container_ip("django-server-grouping-1")
image_processing_ip = get_container_ip("django-server-main_service-1")
# Get information about detection service
detection_service = get_service_details('detection-service')  # Replace with actual service name
detection_url = None
if detection_service:
    detection_url = f"http://{detection_service_ip}:{detection_service['Port']}/detection/"


# Get information about grouping service
grouping_service = get_service_details('grouping-service')  # Replace with actual service name
grouping_url = None
if grouping_service:
    grouping_url = f"http://{grouping_service_ip}:{grouping_service['Port']}/grouping/"


class ImageProcessView(APIView):
    def post(self, request, format=None):
        print(request.FILES)
        if 'image' not in request.FILES:
            return HttpResponseBadRequest("No image uploaded")

        image_file = request.FILES['image']

        try:
            # Read image file content
            image_bytes = image_file.read()

            # Prepare data for detection
            detection_response = requests.post(detection_url, files={'image': (image_file.name, image_bytes)})

            # Check if detection was successful
            if detection_response.status_code != 200:
                return HttpResponseBadRequest("Detection failed")

            detection_data = detection_response.json()
            # Prepare data for grouping
            grouping_response = requests.post(grouping_url, files={'image': (image_file.name, image_bytes)}, data=  {'boxes': detection_data['boxes']})

            # Check if grouping was successful
            if grouping_response.status_code != 200:
                return HttpResponseBadRequest("Grouping failed")

            grouping_data = grouping_response.json()
            processed_image_bytes_grouping = grouping_data.get('image', None)
            response_data = {
                "image": processed_image_bytes_grouping
            }

            return JsonResponse(response_data)
        except Exception as e:
            print(f"Error processing image: {e}")
            return HttpResponseBadRequest("Failed to process image")


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Process the image and call the backend API
        # Replace 'backend_endpoint' with the actual URL of your backend API
        backend_endpoint = f'http://{image_processing_ip}:8000/image_process/'
        response = requests.post(backend_endpoint, files={'image': uploaded_image})

        if response.status_code == 200:
            processed_image_data = response.json()
            return render(request, 'upload_image.html', {'processed_image': processed_image_data})
        else:
            error_message = f"Error processing image: {response.status_code}"
            return render(request, 'upload_image.html', {'error': error_message})

    return render(request, 'upload_image.html')
