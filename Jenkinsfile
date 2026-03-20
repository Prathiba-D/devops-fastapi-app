        // Deploy to Kubernetes using dynamic image → triggers rolling update
 pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'  // Exact name configured in Jenkins -> Configure System -> SonarQube Servers
        IMAGE_NAME = "fastapi-app"  // image name

        AWS_REGION = "ap-south-1"
        ECR_REPO = "205842488113.dkr.ecr.ap-south-1.amazonaws.com/fastapi-app"
    }

    stages {

        stage('Verify Python') {
            steps {
                sh 'python3 --version'  // Ensure Python is installed and version is correct
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'  // Create isolated Python environment
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'  // Install project dependencies
            }
        }

        stage('Syntax Check') {
            steps {
                sh 'venv/bin/python -m py_compile main.py'  // Basic Python syntax check
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export PYTHONPATH=$PWD
                    venv/bin/pytest
                '''
                // Run unit tests
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withEnv(["PATH=/opt/sonar-scanner/bin:$PATH"]) {
                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        sh 'sonar-scanner'  // Perform SonarQube code quality scan
                    }
                }
            }
        }

        stage('Build & Tag Docker Image') {
            steps {
                // Build Docker image with unique build number
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                
                // Tag image with build number
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:${BUILD_NUMBER}"
                
                // Also tag as latest (optional)
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:latest"
            }
        }

        // Trivy scan to check Docker image for vulnerabilities
        stage('Trivy Scan') {
            steps {
                sh '''
                    mkdir -p reports
                    if [ ! -f html.tpl ]; then
                        curl -sSL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl -o html.tpl
                    fi

                    trivy image \
                      --ignore-unfixed \
                      --severity HIGH,CRITICAL \
                      --format template \
                      --template "@html.tpl" \
                      -o reports/trivy_report.html \
                      ${IMAGE_NAME}:${BUILD_NUMBER} || true  
                '''
            }
        }

        // Push Trivy report to GitHub Pages (optional reporting)
        stage('Push Trivy Report to GitHub Pages') {
            steps {
                withCredentials([string(credentialsId: 'github-pat', variable: 'PAT')]) {
                    sh '''
                        git config --global user.name "Jenkins CI"
                        git config --global user.email "ci-bot@mycompany.com"

                        # Clean temporary repo
                        rm -rf /tmp/temp-repo
                        git clone https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git /tmp/temp-repo
                        cd /tmp/temp-repo

                        # Checkout or create gh-pages branch
                        git checkout --orphan gh-pages || git checkout gh-pages
                        git rm -rf . || true

                        # Copy Trivy report
                        cp /var/lib/jenkins/workspace/fastapi-ci/reports/trivy_report.html .

                        # Add index.html to avoid 404
                        echo '<meta http-equiv="refresh" content="0; url=trivy_report.html">' > index.html

                        git add trivy_report.html index.html
                        git commit -m "Update Trivy report - Build ${BUILD_NUMBER}" || echo "No changes to commit"
                        git push https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git gh-pages --force
                    '''
                }
            }
        }

        // Push Docker image to AWS ECR
        stage('Push Image to ECR') {
            steps {
                sh '''
                    echo "Logging in to ECR..."
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECR_REPO

                    echo "Pushing image to ECR..."
                    docker push $ECR_REPO:${BUILD_NUMBER}  
                    docker push $ECR_REPO:latest  
                '''
            }
        }

        // Deploy to Kubernetes using sed → fully declarative approach
        stage('Deploy to Kubernetes (sed + apply)') {
            steps {

                // Print message
                sh 'echo "Updating deployment.yaml with new image tag..."'

                // Replace IMAGE_TAG placeholder with current build number
                sh "sed -i 's|IMAGE_TAG|${BUILD_NUMBER}|g' k8s/deployment.yaml"

                // Apply updated YAML to Kubernetes
                sh "kubectl apply -f k8s/deployment.yaml"

                // Apply service (safe, idempotent)
                sh "kubectl apply -f k8s/service.yaml"

                // Wait for rollout to complete
                sh "kubectl rollout status deployment fastapi-deployment"
            }
        }
    }
}
