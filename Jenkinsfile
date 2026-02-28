pipeline {
    agent any

    environment {
        EC2_PUBLIC_IP   = '13.127.3.216'
        COMPOSE_FILE    = 'docker-compose.yaml'
        BACKEND_URL     = "http://${EC2_PUBLIC_IP}:8000/api/health"
        FRONTEND_URL    = "http://${EC2_PUBLIC_IP}:3000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '=== Checking out source code ==='
                checkout scm
            }
        }

        stage('Test Backend') {
            steps {
                echo '=== Running Backend Tests ==='
                dir('backend') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --quiet -r requirements.txt
                        pip install --quiet pytest httpx
                        pytest app/test_main.py -v --tb=short || true
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '=== Building Docker Images ==='
                sh """
                    docker compose -f ${COMPOSE_FILE} build \
                        --build-arg NEXT_PUBLIC_API_URL=http://${EC2_PUBLIC_IP}:8000
                """
            }
        }

        stage('Deploy') {
            steps {
                echo '=== Deploying Containers ==='
                sh """
                    docker compose -f ${COMPOSE_FILE} up -d --force-recreate --remove-orphans
                """
                // Give services time to start up
                sh 'sleep 15'
            }
        }

        stage('Health Check') {
            steps {
                echo '=== Running Health Checks ==='
                retry(5) {
                    sh """
                        echo 'Checking backend...'
                        curl -f --silent --max-time 10 ${BACKEND_URL} | python3 -c \
                            "import sys, json; d=json.load(sys.stdin); print('Backend OK:', d); assert d.get('status') == 'healthy'"

                        echo 'Checking frontend...'
                        curl -f --silent --max-time 10 -o /dev/null -w '%{http_code}' ${FRONTEND_URL} | grep -q '200'

                        echo 'All health checks passed!'
                    """
                }
            }
        }

        stage('Show Running Containers') {
            steps {
                sh 'docker compose ps'
            }
        }
    }

    post {
        success {
            echo """
            ================================================
            DEPLOYMENT SUCCESSFUL
            ------------------------------------------------
            Frontend : http://${EC2_PUBLIC_IP}:3000
            Backend  : http://${EC2_PUBLIC_IP}:8000
            Jenkins  : http://${EC2_PUBLIC_IP}:8080
            ================================================
            """
        }
        failure {
            echo '=== Deployment FAILED. Showing container logs for debugging ==='
            sh 'docker compose logs --tail=50 || true'
        }
        always {
            echo "Build #${BUILD_NUMBER} finished with status: ${currentBuild.currentResult}"
        }
    }
}
