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
        

        echo Test 1: Jenkinsfile exists
        IF EXIST Jenkinsfile (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 2: Workspace accessible
        cd >nul
        IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 3: Git available
        git --version >nul 2>&1
        IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 4: Docker available
        docker --version >nul 2>&1
        IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 5: File write test
        echo Hello Jenkins > test1.txt
        IF EXIST test1.txt (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 6: File read test
        type test1.txt >nul
        IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 7: Directory creation
        mkdir test_folder
        IF EXIST test_folder (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 8: Environment variable check
        IF DEFINED IMAGE_NAME (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 9: Basic arithmetic
        set /a num=2+2
        IF %num%==4 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 10: Echo command
        echo Jenkins CI/CD running...
        IF %ERRORLEVEL%==0 (echo PASS) ELSE (echo FAIL & exit /b 1)

        echo Test 11: Cleanup test files
        del test1.txt >nul 2>&1
        rmdir /s /q test_folder >nul 2>&1
        echo PASS

        echo ===============================
        echo ALL 11 TESTS PASSED
        echo ===============================
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