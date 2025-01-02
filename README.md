# One Time Secret

## Project Description

This project implements a service for securely storing and sharing one-time secrets. Secrets can be encrypted using a password provided by the user and then retrieved using a unique key. Once a secret is requested and decrypted, it is automatically deleted from the database, ensuring one-time access.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RomanPecheritsa/OneTimeSecretAPI.git
cd OneTimeSecretAPI
```

### 2. Copy the env.example file to .env

Open .env and replace the values of the variables with your own
```bash
cp .env.example .env
```
### 3. Build and Run Docker Containers

Execute the following command to build and starting the Docker images
```bash
make app
```

### 4. Testing the Application

Run the tests and run the tests with coverage
```bash
make tests
make tests-cov
```
### 5. Stop and Down Docker Containers

Execute the following command to stop and down the Docker images
```bash
make app-down
```

### 6. Documentation
The full API documentation is available at: http://127.0.0.1:8000/docs/