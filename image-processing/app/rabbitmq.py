import pika

def create_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    return connection, channel



def start_file_upload_worker():
    from app.service.file_upload import process_file_upload, process_file_operations


    print("Worker started and waiting for messages...") 
    connection, channel = create_rabbitmq_connection()

    # Declare the queue for file upload and save metadata
    channel.queue_declare(queue='file_upload_queue')

    channel.queue_declare(queue="file_processing_queue")

    # Start consuming messages from the queue
    channel.basic_consume(queue='file_upload_queue', on_message_callback=process_file_upload)

    channel.basic_consume(queue='file_processing_queue', on_message_callback=process_file_operations)

    print('Waiting for file upload messages...')
    channel.start_consuming() 