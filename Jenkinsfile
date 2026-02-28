pipeline {
agent any

```
environment {
    GIT_URL = 'https://github.com/Gladlin1412/DevOps-Assignment.git'
    GIT_BRANCH = 'main'
}

stages {

    stage('Checkout Code') {
        steps {
            git branch: "${GIT_BRANCH}", url: "${GIT_URL}"
        }
    }

    stage('Clean Docker Environment') {
        steps {
            sh '''
            docker system prune -a -f
            '''
        }
    }

    stage('Docker Compose Down') {
        steps {
            sh 'docker-compose down || true'
        }
    }

    stage('Docker Compose Build (No Cache)') {
        steps {
            sh 'docker-compose build --no-cache'
        }
    }

    stage('Docker Compose Up') {
        steps {
            sh 'docker-compose up -d'
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
```

}
