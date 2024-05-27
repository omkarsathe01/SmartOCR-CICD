pipeline {
  agent any

  stages {
    stage('Run Docker Container') {
      steps {
        echo 'Running Docker container...'
        sh 'docker compose up --build -d'
      }
    }
  }
}
