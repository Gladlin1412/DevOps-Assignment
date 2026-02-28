pipeline {
    agent { label 'ubuntu' }

    environment {
        GIT_URL    = 'https://github.com/Gladlin1412/DevOps-Assignment.git'
        GIT_BRANCH = 'main'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GIT_URL}"
            }
        }

        stage('Docker Compose Down') {
            steps {
                sh 'docker compose down || true'
            }
        }

        stage('Docker Compose Build & Up') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
    }

    post {
        success {
            echo 'Application deployed successfully using Docker Compose 🚀'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
    }
}