from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import cv2
import numpy as np
from .grouping import group
import json_numpy
from base64 import b64encode



class GroupingView(APIView):
    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return HttpResponseBadRequest("No image uploaded")

        image_file = request.FILES['image']
        image_bytes = image_file.read()
        boxes = request.data.get("boxes")
        boxes_string = json_numpy.loads(boxes)

        try:
            image_arr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            cv2.imwrite("test.jpg", image_arr)
            processed_image, group_id = group(image_arr, boxes_string)
            # Encode the processed image back to bytes
            _, processed_image_bytes = cv2.imencode('.jpg', processed_image)
            processed_image_base64 = b64encode(processed_image_bytes.tobytes()).decode('utf-8')

            return JsonResponse(
                {
                    'image': processed_image_base64,
                    "group_id": str(group_id)
                }
                )
        except Exception as e:
            print(f"Error processing image: {e}")
            return HttpResponseBadRequest("Failed to process image")
