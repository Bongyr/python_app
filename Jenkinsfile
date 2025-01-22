pipeline {
    agent any

    environment {
        NETWORK_NAME = 'monitoring-network'
        IMAGE_NAME = 'python_app'
        DOCKER_REGISTRY = 'bongyr'
        GIT_SSH_KEY = credentials('github-ssh-credentials-id')
    }

     stages {
        stage('Checkout') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'github-ssh-credentials-id', keyFileVariable: 'GIT_SSH_KEY')]) {
                        sh '''
                        if [ -d "python_app/.git" ]; then
                            cd python_app && git pull origin main
                        else
                            git clone git@github.com:Bongyr/python_app.git
                        fi
                        '''
                        }
                    }    
                }
            }  
        
        stage('Build') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:latest .'
                }
            }
        }

        stage('Push to Registry') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_REGISTRY --password-stdin'
                    sh 'docker push $DOCKER_REGISTRY/$IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "docker network create ${NETWORK_NAME} || echo 'Network ${NETWORK_NAME} already exists'"
                    sh """
                     docker run -d --name flask_app \\
                        --network ${NETWORK_NAME} \\
                        -p 5000:5000 \\
                        $DOCKER_REGISTRY/$IMAGE_NAME:latest
                    """
                    
                }
            }
        }
         stage('Test') {
            steps {
                script {
                    def retryCount = 0
                    def maxRetries = 5
                    def appAvailable = false
        
                    // Retry logic to check if Flask app is up
                    while (retryCount < maxRetries && !appAvailable) {
                        try {
                            sh 'curl http://localhost:5000'
                            appAvailable = true
                        } catch (Exception e) {
                            retryCount++
                            echo "Flask app not ready, retrying... (${retryCount}/${maxRetries})"
                            sleep(5)  // Wait for 5 seconds before retrying
                        }
                    }
        
                    // If Flask app is ready, run tests
                    if (appAvailable) {
                        sh 'docker run --rm --network host bongyr/python_app:latest python -m unittest discover -s tests'
                    } else {
                        error "Flask app is not available after ${maxRetries} retries"
                    }
                }
            }
        }
     }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
