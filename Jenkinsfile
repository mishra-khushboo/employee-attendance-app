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

        stage('Run Tests') {
            steps {
                bat '''
                echo Running Dummy Tests...

                echo Test 1: Checking workspace
                IF EXIST Jenkinsfile (echo PASS) ELSE (echo FAIL & exit /b 1)

                echo Test 2: Checking Docker installed
                docker --version >nul 2>&1
                IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

                echo Test 3: Simple command test
                echo Hello Jenkins > test_output.txt
                IF EXIST test_output.txt (echo PASS) ELSE (echo FAIL & exit /b 1)

                echo All Dummy Tests Passed!
                '''
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
                bat "kubectl apply -f k8s/deployment.yaml --validate=false"
                bat "kubectl apply -f k8s/service.yaml --validate=false"
            }
        }
    }

    post {
        success { echo 'Pipeline Success! Attendance App Deployed.' }
        failure { echo 'Pipeline Failed. Fix issues before deployment.' }
    }
}