# **🛒 Product Detection & Grouping System**

## **📌 Project Overview**
This project is designed for **product detection and grouping** on supermarket shelves. It helps in identifying which products are **out of stock** and need a refill. The system is built for **real-time inventory management**, ensuring shelves are always stocked efficiently.

## **⚙️ Technologies Used**
- **Consul** – Service discovery and health checking.
- **Docker** – Containerized deployment for microservices.
- **Django** – Backend framework for API handling.
- **Detection Model** – Used for detecting products in images.
- **Fuzzy C-Means Clustering** – For grouping detected products.
- **YOLO-NAS ONNX (Pre-trained Model)** – Optimized object detection model.

## **🛠 How It Works**
1. **Product Detection** – The detection microservice scans images from supermarket shelves.
2. **Bounding Box Creation** – It identifies and marks each product with a bounding box.
3. **Product Grouping** – Using **Fuzzy C-Means clustering**, it groups similar products (e.g., all Coke bottles as a single group).
4. **Fast Processing** – The system operates in **seconds**, ensuring minimal delay.
5. **Accuracy Improvement** – Currently, working on enhancing detection accuracy using **YOLO-NAS ONNX**.

## **🚀 Future Improvements**
- Further optimization of the **YOLO-NAS ONNX** model for better accuracy.
- Integration with **real-time store inventory management systems**.
- Deployment on **edge devices** for in-store monitoring.

This project is a step toward **AI-powered retail automation** with efficient stock management and real-time alerts! 🛍️📊




# **🚀 Product Detection & Grouping Service**

This project provides a **Product detection and grouping service** using Django and Docker. It processes uploaded images, detects products, and groups similar products using microservices.

---

## **📌 Prerequisites**
- **Docker Desktop** installed. ([Download Docker](https://www.docker.com/products/docker-desktop))
- **Git** installed (if cloning the repo). ([Download Git](https://git-scm.com/))

---

## **📂 Project Setup Instructions**

### **1️⃣ Install Docker Desktop**
1. Download Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).
2. Install Docker following the on-screen instructions.
3. Ensure Docker is running before proceeding.

### **2️⃣ Clone the Repository** (Skip if using a ZIP file)
1. Open **Terminal** (Mac/Linux) or **Command Prompt/Powershell** (Windows).
2. Navigate to the directory where you want to clone the project.
3. Run the following command:
   ```sh
   git clone git@github.com:XAVIXXVI/product-detection-and-grouping.git
   ```
4. Change into the project directory:
   ```sh
   cd product-detection-and-grouping
   ```

### **3️⃣ Extract ZIP File (If Applicable)**
If you received the project as a ZIP file:
1. Extract the ZIP file to a location of your choice.

### **4️⃣ Build the Docker Containers**
1. Open a terminal in the project directory.
2. Run the following command:
   ```sh
   docker-compose build
   ```
3. This command will take some time to execute as it builds all required Docker images.

### **5️⃣ Run the Django Server**
Once the build is complete, run:
```sh
docker-compose up
```
This command will start the Django server along with the required microservices.

---

## **🌐 Running the Application**

### **Access the Application in Your Browser**
Once the server is running, open your browser and go to:
```
http://127.0.0.1:8000/upload/
```

### **Upload an Image**
- Select an image file and upload it.
- The system will process the image using **detection and grouping services**.
- The processed image will be displayed on the same page.

### **Download the Processed Image**
After processing, you will have an option to **download the processed image**.

---

## **📌 Troubleshooting**
- If Docker is not running, restart Docker and try again.
- If the application does not start, run:
  ```sh
  docker-compose down
  docker-compose up --build
  ```

---

✅ **That's it! You're all set to use the application.** 🎉
**Thank you! 🚀**

