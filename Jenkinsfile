pipeline {
    agent any
    environment {
        IMAGE_NAME = "devops27093/employee-attendance-app"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/mishra-khushboo/employee-attendance-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    bat "docker login -u %USER% -p %PASS%"
                    bat "docker push %IMAGE_NAME%:latest"
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat "kubectl apply -f k8s/deployment.yaml"
                bat "kubectl apply -f k8s/service.yaml"
            }
        }
    }
    post {
        success { echo 'Pipeline Success! Attendance App Deployed.' }
        failure { echo 'Pipeline Failed. Check logs.' }
    }
}