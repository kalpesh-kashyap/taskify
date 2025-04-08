from flask import Blueprint, request, jsonify
from .service.file_upload import upload_and_save, start_process
file_routes = Blueprint('file_routes', __name__, url_prefix="/api/image-processing")


@file_routes.route("/upload", methods=["POST"])
def upload_file():
    user_id = request.headers.get("X-User-ID")
    files = [request.files.get(f"file{idx}") for idx in range(len(request.files))]
    
    operations = request.form.get('operations')
    cropsize = request.form.get('cropsize', None)
    filter = request.form.get('filter', None)


    try:
        res = upload_and_save(files, user_id, operations, cropsize, filter)
        return jsonify({"data":res}), 200
    except ValueError as ve:
        return jsonify({"message": "upload error " + str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "upload error " + str(e)}), 500
    

@file_routes.route('process/<int:userId>', methods=["GET"])
def start_image_proces(userId):
    try:
        data = start_process(user_id=userId)
        return jsonify({"message": data}), 200
    except Exception as e:
        return jsonify({"message": "upload error " + str(e)}), 500