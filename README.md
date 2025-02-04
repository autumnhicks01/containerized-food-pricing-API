**Containerized Food Cost API**
===============================

This project provides a scalable Flask API to estimate recipe costs using the **Spoonacular API**. The application is containerized with Docker and deployed on AWS ECS (Fargate), with an Application Load Balancer (ALB) and optional API Gateway integration.

* * * * *
![Untitled diagram-2025-01-31-174922](https://github.com/user-attachments/assets/97c45f22-7c56-4a1c-9f63-04ffa62b9517)


**Features**
------------

-   Receives a list of ingredients and servings.
-   Queries Spoonacular's Price Estimator endpoint.
-   Returns a formatted HTML response with ingredient costs.
-   Scalable infrastructure using Docker and AWS services.

<img width="701" alt="w9oriwoeri" src="https://github.com/user-attachments/assets/04a0fe69-fab3-4de5-babe-37b4a59d7275" />

* * * * *

**Project Structure**
---------------------

-   **app.py**: Main Flask application handling API requests.
-   **Dockerfile**: Instructions to containerize the application.
-   **test_form.html**: Simple form for testing API requests.
-   **requirements.txt**: Python dependencies.

* * * * *

**Getting Started**
-------------------

### **Prerequisites**

-   Python 3.x installed locally.
-   Docker installed on your machine.
-   AWS CLI installed and configured.

### **Environment Variable**

The application requires a **SPOONACULAR_API_KEY** for API access. Set this before running the app:


`export SPOONACULAR_API_KEY="your_api_key_here"`

* * * * *

### **Local Development**

1.  Install dependencies:

    `pip install -r requirements.txt`

2.  Run the Flask app locally:

    `python app.py`

3.  Test using `curl`:

    `curl -X POST -F "ingredientList=3 oz chicken breast" http://127.0.0.1:5000/price-estimator`

* * * * *

### **Docker Setup**

1.  Build the Docker image:

    `docker build -t food-cost-api .`

2.  Run the Docker container:

    `docker run -p 8080:8080 -e SPOONACULAR_API_KEY=your_api_key food-cost-api`

* * * * *

### **AWS Deployment**

1.  **Push Docker Image to AWS ECR**:

    -   Create an ECR repository:

        `aws ecr create-repository --repository-name food-cost-api`

    -   Authenticate Docker to AWS:

        `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com`

    -   Tag and push the image:

        `docker tag food-cost-api:latest <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/food-cost-api:latest
        docker push <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/food-cost-api:latest`

2.  **Deploy on AWS ECS**:

    -   Create a Fargate cluster.
    -   Register a task definition using the ECR image and configure port `8080`.
    -   Add the **SPOONACULAR_API_KEY** as an environment variable.
    -   Create a service and attach an Application Load Balancer (ALB) for traffic distribution.
3.  **(Optional) API Gateway Integration**:

    -   Create a new HTTP API in AWS API Gateway.
    -   Link the ALB's DNS name and `/price-estimator` path.
    -   Deploy the API and obtain the public endpoint URL.

* * * * *

### **Testing**

1.  Use the HTML form (**test_form.html**) to test the API:

2.  Alternatively, test with `curl`:

    `curl -X POST -F "ingredientList=3 oz chicken breast" https://<api-gateway-id>.execute-api.<region>.amazonaws.com/price-estimator`

* * * * *

**Future Enhancements**
-----------------------

-   Add nutrition or allergen tracking via Spoonacular endpoints.
-   Secure API keys with AWS Secrets Manager.
-   Create a frontend to display detailed cost data.

* * * * *

**Contributors**
----------------

Contributions are welcome! Feel free to submit a pull request or open an issue.
