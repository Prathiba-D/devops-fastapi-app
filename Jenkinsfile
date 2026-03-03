pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQubeServer'  // Exact name configured in Jenkins -> Configure System -> SonarQube Servers
        //PATH = "/opt/sonar-scanner/bin:$PATH" // Needed if sonar-scanner installed manually
    }

    stages {

        stage('Pull Code From GitHub') {
            steps {
                git 'https://github.com/Prathiba-D/devops-fastapi-app.git'

            }
        }

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
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh 'sonar-scanner'
                }
            }
        }
    }
}
