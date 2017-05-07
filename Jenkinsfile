pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('Checkout'){
           checkout scm
           sh '''
           git submodule init
           git submodule update
           '''
        }
        stage('build') {
            steps {
                sh 'python setup.py develop'
            }
        }
    }
}
