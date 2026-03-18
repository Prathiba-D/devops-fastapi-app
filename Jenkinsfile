pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'  // Exact name configured in Jenkins -> Configure System -> SonarQube Servers
        //PATH = "/opt/sonar-scanner/bin:$PATH" // Needed if sonar-scanner installed manually
        //PATH = "/opt/sonar-scanner/bin:${env.PATH}"   // Add the actual sonar-scanner path
        IMAGE_NAME = "fastapi-app"  // image name

        AWS_REGION = "ap-south-1"
        ECR_REPO = "205842488113.dkr.ecr.ap-south-1.amazonaws.com/fastapi-app"

    }
    stages {

        // Optional: Pull latest code from GitHub
        // stage('Pull Code From GitHub') {
        //     steps {
        //         git 'https://github.com/Prathiba-D/devops-fastapi-app.git'
        //     }
        // }

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
                    venv/bin/pytest  // Run unit tests
                '''
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

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .  // Build Docker image with unique build number
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:${BUILD_NUMBER}  // Tag image with build number
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:latest  // Also tag as latest (optional)
                '''
            }
        }

        // Trivy scan to check Docker image for vulnerabilities
        stage('Trivy Scan') {
            steps {
                sh '''
                    mkdir -p reports

                    # Download official HTML template if not present
                    if [ ! -f html.tpl ]; then
                        curl -sSL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl -o html.tpl
                    fi

                    trivy image \
                      --ignore-unfixed \
                      --severity HIGH,CRITICAL \
                      --format template \
                      --template "@html.tpl" \
                      -o reports/trivy_report.html \
                      ${IMAGE_NAME}:${BUILD_NUMBER} || true  // Ignore exit code to not fail the pipeline
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
                    docker push $ECR_REPO:${BUILD_NUMBER}  // Push unique build number
                    docker push $ECR_REPO:latest  // Optional push to latest tag
                '''
            }
        }

        // Deploy to Kubernetes using dynamic image → triggers rolling update
        stage('Deploy to Kubernetes (Automatic Rollout)') {
            steps {
                sh '''
                    echo "Updating Kubernetes Deployment with new image..."

                    # Replace placeholder in deployment.yaml with current build tag
                    kubectl set image deployment/fastapi-deployment \
                        fastapi-container=$ECR_REPO:${BUILD_NUMBER}

                    # Wait until rollout completes successfully
                    kubectl rollout status deployment fastapi-deployment
                '''
            }
        }
    }
}
