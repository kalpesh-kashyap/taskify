
# Taskify - Microservices Project

This project is designed to showcase a **file processing tool** with microservices architecture using **Flask** and **RabbitMQ**. The project has the following microservices:

- **User Service**: Handles user authentication and management.
- **API Gateway**: Acts as a reverse proxy to forward requests to other microservices.
- **Image Processing Service**: Handles file uploads and processes images (crop, filter, etc.).

## Microservices Overview

### 1. **User Service**
- **Port**: 3001
- **Responsibilities**: 
  - Handles user registration and login functionality.
  - Interacts with the database to save and retrieve user data.

### 2. **API Gateway**
- **Port**: 3000
- **Responsibilities**:
  - The entry point for all requests.
  - Forwards requests to the appropriate microservices (User Service or Image Processing Service).
  - Handles JWT authentication for secure access to services.

### 3. **Image Processing Service**
- **Port**: 3002
- **Responsibilities**:
  - Handles file uploads and saves metadata.
  - Processes uploaded images based on operations requested (e.g., crop, filter, etc.).
  - Saves processed images to the server and updates the database with processed file information.

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8+
- RabbitMQ
- PostgreSQL

### Python Libraries

To install the required Python libraries for all services, run:

```bash
pip install -r requirements.txt
```

### Setup the Environment

Make sure to create a `.env` file with the following variables set for each microservice:

```text
PORT=3000  # Port for API Gateway
DATABASE_URI=postgresql://username:password@localhost/taskify
IMAGE_PROCESS_SERVICE=http://localhost:3002
JWT_SECRET_KEY=your_jwt_secret_key
```

### RabbitMQ

Make sure RabbitMQ is running and accessible on the default port (`5672`).

## Running the Project

### 1. **Start the RabbitMQ Server**:

Ensure that RabbitMQ is running on your machine. You can use Docker or a local installation to start RabbitMQ.

```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:management
```

### 2. **Start the Microservices**

Each service runs on its own port. You need to start each microservice in separate terminals.

#### **User Service**:

```bash
cd user-service
python run.py
```

#### **API Gateway**:

```bash
cd api-gateway
python run.py
```

#### **Image Processing Service**:

```bash
cd image-processing
python run.py
```

## API Endpoints

### **User Service** (Port 3001)

- **POST /register**: Register a new user.
- **POST /login**: Login and receive a JWT token.

### **API Gateway** (Port 3000)

- **POST /upload**: Upload files for processing.
  - Forward the request to the **Image Processing Service** for processing.

### **Image Processing Service** (Port 3002)

- **POST /upload**: Upload files and process them. The service will save files and apply requested operations (e.g., crop, filter).

## File Processing Workflow

1. **File Upload**: Users upload files through the **API Gateway**.
2. **Message to RabbitMQ**: Metadata about the uploaded files is sent to **RabbitMQ**.
3. **Processing Files**: The **Image Processing Service** consumes the message, processes the files (crop, filter, etc.), and updates the database.
4. **Database Update**: After processing, the service updates the metadata in the database.

## Directory Structure

```
/user-service
    /app
        /models
        /routes
        /services
        /config.py
        run.py
/api-gateway
    /app
        /config.py
        run.py
        /routes
/image-processing
    /app
        /models
        /services
        /config.py
        run.py
    /uploads
    /processed_files
```

## Notes

- Each service can be run independently or together for a full end-to-end demo.
- RabbitMQ handles task queuing for file processing, making the system asynchronous and scalable.
