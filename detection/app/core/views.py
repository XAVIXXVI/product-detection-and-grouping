from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
import cv2
import numpy as np
from base64 import b64encode
from .detect import detection
import json_numpy

class DetectionView(APIView):
    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return HttpResponseBadRequest("No image uploaded")

        image_file = request.FILES['image']
        image_bytes = image_file.read()

        try:
            image_arr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            processed_image, boxes, scores = detection(image_arr)
            _, processed_image_bytes = cv2.imencode('.jpg', processed_image)
            processed_image_base64 = b64encode(processed_image_bytes.tobytes()).decode('utf-8')

            b_boxes = json_numpy.dumps(boxes)

            response_data = {
                "boxes": b_boxes,
                "processed_image": processed_image_base64
            }

            return JsonResponse(response_data)

        except Exception as e:
            print(f"Error processing image: {e}")
            return HttpResponseBadRequest("Failed to process image")
