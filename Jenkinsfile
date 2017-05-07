pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh '''
                python setup.py develop --user
                '''
            }
        }
    }
}
