IMAGE_NAME = "production/dictmixin"

node {
    withCredentials([
        [$class: 'StringBinding', credentialsId: 'PYPI_PASSWORD', variable: 'PYPI_PASSWORD']
    ]) {
        stage('Checkout') { checkout scm }

        try {
            stage('Build') {
                sh "sudo docker build -t $IMAGE_NAME ."
            }

            stage('Packaging and upload') {
                sh """
                   sudo docker run -e VERSION=${VERSION} \
                                   -e PASSWORD=${env.PYPI_PASSWORD} \
                                   --rm $IMAGE_NAME
                """
            }

            slackSend color: 'good', message: "${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        } catch (e) {
            currentBuild.result = 'FAILURE'
            slackSend color: 'danger', message: "${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }

    }
}
