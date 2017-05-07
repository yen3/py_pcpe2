pipeline {
    agent { docker 'ubuntu:16.04' }
    stages {
        stage('build') {
            steps {
                sh '''
                ./run_ci.sh
                '''
            }
        }
    }
}
