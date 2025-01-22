pipeline {
    agent any

    environment {
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
                    sh 'docker run -d -p 5000:5000 $DOCKER_REGISTRY/$IMAGE_NAME:latest'
                }
            }
        }
         stage('Test') {
            steps {
                script {
                    // Docker run command to test
                    sh 'docker run --rm bongyr/python_app:latest python -m unittest discover -s tests'
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
