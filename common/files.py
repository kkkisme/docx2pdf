import os
from config import config
from werkzeug.utils import secure_filename
from flask import request


def uploads_url(path):
    return request.host_url + path.replace(config['uploads_dir'], 'uploads')


def save_to(folder, file):
    os.makedirs(folder, exist_ok=True)
    save_path = os.path.join(folder, secure_filename(file.filename))
    file.save(save_path)
    return save_path
