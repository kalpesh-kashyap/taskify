from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from app.auth import token_required
from app.config import Config
import requests

file_upload = Blueprint('file_upload', __name__)

@file_upload.route("/upload", methods=["POST"])
@token_required
def upload_file(user_id):
    try:
        files = request.files.getlist('images')
        
        if len(files) == 0:
            raise ValueError("Please upload file to process")
        
        files_to_send = {}

        for idx, file in enumerate(files):
            filename = secure_filename(file.filename)  # Ensure safe filenames
            files_to_send[f'file{idx}'] = (filename, file.stream, file.content_type)

        operations = request.form.get('operations', None)
        cropsize = request.form.get('cropsize', None)
        filter = request.form.get('filter', None)
        data = {
            "user_id": user_id,
            "operations": operations,
            "cropsize": cropsize,
            "filter":filter
        }    
        
        image_process_service = f"{Config.IMAGE_PROCESS_SERVICE}/api/image-processing/upload"
        response = requests.post(image_process_service, files=files_to_send,data=data, headers={"X-User-ID": user_id})
        return jsonify({"message": "Files uploaded and processed successfully", "data": response.json()}), response.status_code
            
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@file_upload.route("/process/<int:userId>", methods=['GET'])
def start_process(userId):
    try:
        image_process_service = f"{Config.IMAGE_PROCESS_SERVICE}/api/image-processing/process/{userId}"
        print(image_process_service)
        response = requests.get(image_process_service)
        return jsonify({"message": "Files uploaded and processed successfully", "data": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500