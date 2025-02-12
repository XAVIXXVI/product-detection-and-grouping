from sklearn.preprocessing import StandardScaler
import cv2
import numpy as np
from PIL import Image
import random
import cv2
import numpy as np
import skfuzzy as fuzz
from sklearn.preprocessing import StandardScaler
from skimage.feature import local_binary_pattern

class GroupingModule:
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def group(self, bounding_boxes, img4):
        image = img4.copy()
        features = self.extract_features(bounding_boxes, image)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
            features_scaled.T,
            c=50,
            m=5,
            error=0.005,
            maxiter=1000,
            init=None
        )
        cluster_labels = np.argmax(u, axis=0)
        unique_cluster_ids = np.unique(cluster_labels)

        clustered_boxes = {}
        for i, label in enumerate(cluster_labels):
            if label not in clustered_boxes:
                clustered_boxes[label] = []
            clustered_boxes[label].append(bounding_boxes[i])

        return {
            "cluster_ids": unique_cluster_ids.tolist(),
            "clustered_boxes": clustered_boxes
        }

    def extract_features(self, bounding_boxes, image):
        features = []
        for box in bounding_boxes:
            x1, y1, x2, y2 = box
            roi = image[y1:y1+y2, x1:x1+x2]
            roi = np.array(roi)
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            color_hist = cv2.calcHist([roi], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            color_mean = cv2.mean(roi)

            lbp = local_binary_pattern(roi_gray, 8, 1, method='uniform')
            lbp_hist, _ = np.histogram(lbp.ravel(), bins=256)

            features.append(np.concatenate((color_hist.flatten(), color_mean, lbp_hist.flatten())))

        return np.array(features)


def visualize_clusters(image, clusters):
    image_copy = image.copy()
    colors = set()

    def generate_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while len(colors) < len(clusters):
        color = generate_color()
        colors.add(color)

    colors = list(colors)
    print(len(colors))
    next_color = 0
    for cluster_id, bounding_boxes in clusters.items():
        color = colors[next_color]

        for box in bounding_boxes:
            cv2.rectangle(image_copy, (box[0], box[1]), (box[0]+ box[2], box[1]+box[3]), color, 4)
        next_color += 1
    cv2.imwrite("test2.jpg", image_copy)
    return image_copy


def group(img3, b_boxes):
    grouping_module = GroupingModule(threshold=0.5)
    results = grouping_module.group(b_boxes, img3)
    image_with_boxes = visualize_clusters(img3, results["clustered_boxes"])

    # Convert image to PIL format
    pil_image = Image.fromarray(image_with_boxes)

    # Save the image with boxes
    pil_image.save('res.jpg')
    return image_with_boxes, results["clustered_boxes"]

