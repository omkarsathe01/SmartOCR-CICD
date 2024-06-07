from TextfromDoc import app as application
from prometheus_client import start_http_server

if __name__ == "__main__":
    start_http_server(8000)
    application.run(port=5000)
