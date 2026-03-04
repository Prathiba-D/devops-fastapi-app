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

                stage('Trivy Scan') {
            steps {
                sh '''
                    mkdir -p reports
                    trivy image --ignore-unfixed --format template \
                    --template "@contrib/html.tpl" \
                    --output reports/trivy_report.html \
                    ${IMAGE_NAME}:${BUILD_NUMBER} || true
                '''
                // archiveArtifacts artifacts: 'reports/trivy_report.html', fingerprint: true
            }
        }
        stage('Push Trivy Report to GitHub') {
            steps {
                withCredentials([string(credentialsId: 'github-pat', variable: 'PAT')]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "ci-bot@mycompany.com"

                        git clone https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git temp-repo
                        cd temp-repo
                        cp ../reports/trivy_report.html .

                        git add trivy_report.html
                        git commit -m "Update Trivy vulnerability report - ${BUILD_NUMBER}" || echo "No changes to commit"
                        git push https://$PAT@github.com/Prathiba-D/devops-fastapi-app.git main
                    '''
                }
            }
        }
      
    }
}
