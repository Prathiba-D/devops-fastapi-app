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

        // stage('Pull Code From GitHub') {
        //     steps {
        //         git 'https://github.com/Prathiba-D/devops-fastapi-app.git'

        //     }
        // }

        stage('Verify Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Syntax Check') {
            steps {
                sh 'venv/bin/python -m py_compile main.py'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export PYTHONPATH=$PWD
                    venv/bin/pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withEnv(["PATH=/opt/sonar-scanner/bin:$PATH"]) {
                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        sh 'sonar-scanner'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                sh "docker build -t ${IMAGE_NAME}:${env.BUILD_NUMBER} ."
            }
        }

        //         stage('Trivy Scan') {
        //     steps {
        //         sh '''
        //             mkdir -p reports
        //             trivy image --ignore-unfixed --severity HIGH,CRITICAL --format html \
        //             --output reports/trivy_report.html ${IMAGE_NAME}:${BUILD_NUMBER} || true
        //         '''
        //         // archiveArtifacts artifacts: 'reports/trivy_report.html', fingerprint: true
        //     }
        // }


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
                      ${IMAGE_NAME}:${BUILD_NUMBER} || true
                '''
            }
        }
        
         stage('Push Trivy Report to GitHub Pages') {
            steps {
                withCredentials([string(credentialsId: 'github-pat', variable: 'PAT')]) {
                    sh '''
                        git config --global user.name "Jenkins CI"
                        git config --global user.email "ci-bot@mycompany.com"
        
                        # Clean temp directory
                        rm -rf /tmp/temp-repo
        
                        # Clone repository
                        git clone https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git /tmp/temp-repo
                        cd /tmp/temp-repo
        
                        # Create clean gh-pages branch
                        git checkout --orphan gh-pages || git checkout gh-pages
                        git rm -rf . || true
        
                        # Copy Trivy report
                        cp /var/lib/jenkins/workspace/fastapi-ci/reports/trivy_report.html .
        
                        # Create index.html to avoid 404
                        echo '<meta http-equiv="refresh" content="0; url=trivy_report.html">' > index.html
        
                        git add trivy_report.html index.html
                        git commit -m "Update Trivy report - Build ${BUILD_NUMBER}" || echo "No changes to commit"
        
                        # Force push to gh-pages
                        git push https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git gh-pages --force
                    '''
                }
            }
        }
        
        stage('Push Image to ECR') {
            steps {
                sh '''
                    echo "Logging in to ECR..."
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECR_REPO

                    echo "Tagging image for ECR..."
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:${BUILD_NUMBER}
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} $ECR_REPO:latest

                    echo "Pushing image to ECR..."
                    docker push $ECR_REPO:${BUILD_NUMBER}
                    docker push $ECR_REPO:latest
                '''
            }
        }
      
    }
}
