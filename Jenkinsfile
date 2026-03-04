pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'  // Exact name configured in Jenkins -> Configure System -> SonarQube Servers
        //PATH = "/opt/sonar-scanner/bin:$PATH" // Needed if sonar-scanner installed manually
        //PATH = "/opt/sonar-scanner/bin:${env.PATH}"   // Add the actual sonar-scanner path
        IMAGE_NAME = "fastapi-app"  // image name

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

        // stage('SonarQube Analysis') {
        //     steps {
        //         withEnv(["PATH=/opt/sonar-scanner/bin:$PATH"]) {
        //             withSonarQubeEnv("${SONARQUBE_SERVER}") {
        //                 sh 'sonar-scanner'
        //             }
        //         }
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                sh "docker build -t ${IMAGE_NAME}:${env.BUILD_NUMBER} ."
            }
        }

        stage('Scan Docker Image') {
            steps {
                echo "Scanning Docker image ${IMAGE_NAME}:${env.BUILD_NUMBER} for vulnerabilities..."
                // Scan and fail build if critical/high vulnerabilities are found
                sh "trivy image --exit-code 1 --severity CRITICAL,HIGH ${IMAGE_NAME}:${env.BUILD_NUMBER} > trivy_report.txt"
                // Optional: display first few lines of the report in console
                sh "head -n 20 trivy_report.txt"
            }
        }
      
    }
}
