pipeline {
  agent any

  stages {
    stage('Run Docker Container') {
      steps {
        echo 'Running Docker container...'
        bat 'docker compose up --build -d'
      }
    }
  }
}
