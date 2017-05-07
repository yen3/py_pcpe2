pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh '''
                apt-get update
                apt-get install git -y
                git submodule init
                git submodule update
                python setup.py develop
                '''
            }
        }
    }
}
