pipelineJob('Python-Docker-App-Pipeline') {
    description('CI/CD pipeline for a Python Flask Dockerized app')

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/Bongyr/python-app.git')
                        credentials('github-credentials-id')
                    }
                    branch('main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }

    triggers {
    cron('H 4/* 0 0 1-5')
    }

    properties {
        pipelineTriggers {
            triggers {
                githubPush()
            }
        }
    }

    logRotator {
        numToKeep(10)
    }
}
