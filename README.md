General Commands

**1. Clone the Repository**
git clone <repository-url>
cd <project-directory>

**2. Install Dependencies**
**For CDK dependencies:**
npm install
For Python dependencies (if using a Python Lambda function):
pip install -r requirements.txt

**3. Authenticate Docker to AWS ECR**
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com

**4. Build and Push Docker Image**e
docker build -t my-lambda-image .

**Tag the image with your ECR repository:**
docker tag my-lambda-image:latest <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository-name>:latest

**Push the image to your ECR repository:**
docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<ecr-repository-name>:latest

**5. Deploy the CDK Stack**
**Bootstrap the CDK environment:**
cdk bootstrap
**Deploy the stack to AWS:**
cdk deploy

**6. Test the Lambda Function via API Gateway (cURL)**
Send a POST request to the API Gateway to test the Lambda function:
curl -X POST https://<api-id>.execute-api.<aws-region>.amazonaws.com/prod/messages \
    -H "Content-Type: application/json" \
    -d '{"messageUUID":"123e4567-e89b-12d3-a456-426614174000","messageText":"Hello, world!","messageDatetime":"2024-02-01 10:00:00"}'
