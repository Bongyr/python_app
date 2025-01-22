pipeline {
    agent any

    environment {
        IMAGE_NAME = 'python-app'
        DOCKER_REGISTRY = 'Bongyr'
        GIT_SSH_KEY = credentials('github-ssh-credentials-id')
    }

     stages {
        stage('Checkout') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'github-ssh-credentials-id', keyFileVariable: 'GIT_SSH_KEY')]) {
                        sh '''
                        git config core.sshCommand "ssh -i $GIT_SSH_KEY"
                        git clone git@github.com:Bongyr/python-app.git
                        '''
                        }
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

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
