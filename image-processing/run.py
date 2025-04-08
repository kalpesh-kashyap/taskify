import threading
from app import create_app
from app.rabbitmq import start_file_upload_worker

app = create_app()

def run_worker():
    start_file_upload_worker()

if __name__ == '__main__':
    worker_thread = threading.Thread(target=run_worker)
    worker_thread.daemon = True
    worker_thread.start()
    app.run(debug=True, use_reloader=True, port=app.config["PORT"])
