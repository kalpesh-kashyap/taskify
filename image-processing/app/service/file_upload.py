from app.rabbitmq import create_rabbitmq_connection
from werkzeug.utils import secure_filename
from app.config import Config
from app.models.file_model import Files
from app.db import db
from app.config import Config
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image, ImageFilter
# from PIL

import json
import os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_and_save(files, user_id, operations, cropsize, filter):
    try:
        if len(files) == 0:
            raise ValueError("Please upload file to process")
        
        for file in files:
            if file and allowed_file(file.filename):
                if file.mimetype not in ['image/jpeg', 'image/png', 'image/gif']:
                    raise ValueError(f"Invalid file type: {file.mimetype}. Only JPG, PNG, GIF are allowed.")
            else:
                raise ValueError(f"Invalid file extension: {file.filename}. Only JPG, PNG, GIF are allowed.")

        connection, channel = create_rabbitmq_connection()    

        channel.queue_declare(queue="file_upload_queue")

        files_metadata = []

        os.makedirs(Config.FILE_UPLOAD_PATH, exist_ok=True)

        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.FILE_UPLOAD_PATH, filename)
            file.save(file_path)
            files_metadata.append({
                'filename': secure_filename(file.filename),
                'user_id': user_id,
                'original_size': file.content_length,
                'status': 'uploading',
                'operations': json.dumps({'operations': operations, 'cropsize': cropsize, 'filter': filter}),
            })

        message = {
            'files': files_metadata,
            'status': 'uploading'
        }

        channel.basic_publish(exchange='',routing_key='file_upload_queue', body=json.dumps(message))
        connection.close()

        
        return f"file uploaded {str(len(files))}"
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))


def process_file_upload(ch, method, properties, body):
    from app import create_app
    try:
        app = create_app()
        with app.app_context():
            message = json.loads(body)
            files_metadata = message["files"]
            user_id = files_metadata[0]['user_id']

            for file_meta in files_metadata:
                filename = file_meta['filename']
                file_path = os.path.join(Config.FILE_UPLOAD_PATH, filename)
                operations = file_meta['operations']

                new_file = Files(
                    filename=filename,
                    user_id=user_id,
                    file_url=file_path,
                    status="uploaded",
                    original_size=file_meta['original_size'],
                    operations=operations,
                )

                db.session.add(new_file)
                db.session.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing file: {str(e)}")



def process_file_operations(ch, method, properties, body):
    from app import create_app
    try:
        app = create_app()
        with app.app_context():
            message = json.loads(body)
            user_id = message['user_id']
            operations = json.loads(message['operations'])

            filename = message['filename']
            file_path = os.path.join(Config.FILE_UPLOAD_PATH, filename)

            image = Image.open(file_path)
            os.makedirs(Config.PROCESSED_FILE_PATH, exist_ok=True)
            if 'crop' in message['operations']:
                crop_details = operations.get('cropsize', '22x22').split('x')
                crop_width = int(crop_details[0])
                crop_height = int(crop_details[1])
                image = image.crop((0, 0, crop_width, crop_height)) 
                
            processed_filename = f"processed_{filename}"
            processed_file_path = os.path.join(Config.PROCESSED_FILE_PATH, processed_filename)
            image.save(processed_file_path)
            new_file = Files.query.filter_by(filename=filename).first()
            new_file.status = 'processed'
            new_file.processed_file_url = processed_file_path
            new_file.processed_size = os.path.getsize(processed_file_path)
            db.session.commit()

            ch.basic_ack(delivery_tag=method.delivery_tag)     

    except Exception as e:
        print("error "+ str(e))

def start_process(user_id):
    try:
        if not user_id:
            raise ValueError("userid requred")
        
        files = Files.query.filter_by(user_id=user_id).all()

        if not files:
            raise ValueError("No uploaded files found for this user")
        
        file_metadata = [file.to_dict() for file in files]

        connection, channel = create_rabbitmq_connection()

        for file in file_metadata:
            channel.basic_publish(exchange='', routing_key='file_processing_queue', body=json.dumps(file))
        channel.close()


        return file_metadata

    except SQLAlchemyError as sqlErr:
        raise Exception("Database error occurred: " + str(sqlErr))
    except Exception as e:
        raise Exception("Database error occurred: " + str(e))

