import os
from uuid import uuid4
from subprocess import TimeoutExpired
from flask import Flask, request, jsonify, send_from_directory
from config import config
from common.files import save_to, uploads_url
from common.errors import InternalServerErrorError, PageNotFound, RestAPIError
from common.docx2pdf import convert_to, LibreOfficeError

app = Flask(__name__, static_url_path='')


@app.route('/upload', methods=['POST'])
def upload_file():
    upload_id = str(uuid4())
    source = save_to(os.path.join(config['uploads_dir'], 'source', upload_id), request.files['file'])

    try:
        result = convert_to(os.path.join(config['uploads_dir'], 'pdf', upload_id), source, timeout=15)
    except LibreOfficeError:
        raise InternalServerErrorError({'message': 'Error when converting file to PDF'})
    except TimeoutExpired:
        raise InternalServerErrorError({'message': 'Timeout when converting file to PDF'})

    return jsonify({'result': {'source': uploads_url(source), 'pdf': uploads_url(result)}})


@app.route('/uploads/<path:path>', methods=['GET'])
def serve_uploads(path):
    return send_from_directory(config['uploads_dir'], path)


@app.errorhandler(404)
def page_not_found(error):
    return PageNotFound().to_response()


@app.errorhandler(500)
def handle_500_error():
    return InternalServerErrorError().to_response()


@app.errorhandler(RestAPIError)
def handle_rest_api_error(error):
    return error.to_response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
