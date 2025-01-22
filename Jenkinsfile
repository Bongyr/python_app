pipeline {
    agent any

    environment {
        IMAGE_NAME = 'python-app'
        DOCKER_REGISTRY = 'Bongyr'
    }

    stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Bongyr/python-app.git',
                        credentialsId: 'github-credentials-id'
                    ]]
                ])
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:latest .'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh 'docker run --rm $DOCKER_REGISTRY/$IMAGE_NAME:latest python -m unittest discover -s tests'
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
                    sh 'docker run -d -p 5000:5000 $DOCKER_REGISTRY/$IMAGE_NAME:latest'
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
