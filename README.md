
# **API Rate Limiter with Docker and Kubernetes**

## **Project Overview**

This project implements an **API rate limiter** using **Flask** and **Redis**, deployed with **Docker** and **Kubernetes** for scalability and high availability. The rate limiter restricts the number of requests a client (identified by IP address) can make to the API. Clients are allowed a maximum of 10 requests per minute. Once the limit is exceeded, clients receive a `429 Too Many Requests` error. The project showcases expertise in building scalable applications using containerization and orchestration tools like Docker and Kubernetes.

## **Key Features**

- **Rate Limiting**: Limits API requests to 10 per minute per client IP.
- **Redis Integration**: Redis is used to track client requests and enforce the rate limit.
- **Dockerized Application**: The entire application is containerized using Docker for easy deployment and consistency across environments.
- **Kubernetes Deployment**: The application is deployed in a Kubernetes cluster, with auto-scaling and load balancing to ensure reliability and scalability.
- **API Endpoint**: `/api` - Allows users to interact with the API, where rate-limiting is enforced.

## **Technologies Used**

- **Flask**: Python web framework for creating the API.
- **Redis**: In-memory data store used for tracking request counts and rate limiting.
- **Docker**: Containerization technology to package the application and its dependencies.
- **Kubernetes**: Orchestration platform to manage the deployment, scaling, and operation of the application.

## **Installation and Setup**

### **Prerequisites**

- Docker
- Kubernetes (installed and configured locally or through a cloud provider)
- Redis (handled within the project via Docker)
- Python 3.x

### **Step 1: Clone the Repository**

Clone this repository to your local machine:

```bash
git clone https://github.com/Digvijay-pawar/api-rate-limiter.git
cd api-rate-limiter
```

### **Step 2: Build and Run with Docker**

To build and run the application locally using Docker and Docker Compose:

1. **Build Docker Images**:
   ```bash
   docker-compose build
   ```

2. **Run the Application**:
   ```bash
   docker-compose up
   ```

This will start the Flask app and Redis service in containers.

3. **Test the Application**:
   Visit `http://localhost:5000/api` in your browser or use a tool like **Postman** or **curl** to test the API.

### **Step 3: Deploy with Kubernetes**

1. **Apply Redis Deployment**:
   Deploy Redis to Kubernetes using the following command:
   ```bash
   kubectl apply -f redis-deployment.yaml
   ```

2. **Apply Flask App Deployment**:
   Deploy the Flask app to Kubernetes using the following command:
   ```bash
   kubectl apply -f flask-app-deployment.yaml
   ```

3. **Apply Services**:
   Expose the Flask app and Redis services using:
   ```bash
   kubectl apply -f service.yaml
   ```

4. **Verify the Deployments**:
   Ensure the pods are running and services are exposed:
   ```bash
   kubectl get pods
   kubectl get services
   ```

5. **Access the Application**:
   - If using `LoadBalancer` or `NodePort` for Kubernetes service, access the app via the provided external IP or node IP and port.

   Example (using `LoadBalancer` service):
   ```bash
   http://localhost/api
   ```

### **Step 4: Scaling the Application with Kubernetes**

You can scale the Flask app pods based on traffic by updating the number of replicas in the `flask-app-deployment.yaml` file:

1. **Scale Flask App Pods**:
   ```bash
   kubectl scale deployment flask-app --replicas=5
   ```

   Kubernetes will automatically create the new pods and load balance traffic between them.

## **Project Structure**

```plaintext
api-rate-limiter/
│
├── docker-compose.yml          # Docker Compose file for local setup
├── Dockerfile                  # Dockerfile for Flask app
├── flask-app-deployment.yaml   # Kubernetes deployment for Flask app
├── redis-deployment.yaml      # Kubernetes deployment for Redis
├── service.yaml               # Kubernetes service to expose the app and Redis
├── requirements.txt           # Python dependencies
├── app.py                      # Flask application with rate limiting logic
└── README.md                   # This file
```

## **Rate Limiting Logic**

1. **Request Count-Based Rate Limiting**:
   - The application allows a maximum of **10 requests per minute** per client IP.
   - Redis is used to store and manage request counts for each client IP. The count is reset every minute.

2. **Rate Limiting Middleware**:
   - Every incoming request is checked against Redis to determine if the client has exceeded the rate limit.
   - If the limit is exceeded, the client receives a `429 Too Many Requests` response.

3. **Redis Commands**:
   - `SETEX`: Initializes the request count with a TTL of 60 seconds for each client.
   - `INCRBY`: Increments the request count for each subsequent request within the time window.

## **Scaling and Deployment with Kubernetes**

- **Auto-scaling**: Kubernetes can automatically scale the number of Flask app pods based on traffic by adjusting the deployment configuration.
- **Load Balancing**: Kubernetes ensures that incoming requests are evenly distributed across the available Flask app pods.
- **Fault Tolerance**: Kubernetes will restart failed pods and maintain application availability.
