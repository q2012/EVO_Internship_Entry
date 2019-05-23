from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import datetime
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db
from flask_pymongo import GridFS

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('home/index.html')


@bp.route('/upload', methods=["POST"])
def upload():
    grid_fs = GridFS(db.mongo.db)
    with grid_fs.new_file(filename=str(datetime.datetime.now())) as fp:
        fp.write(request.files["file"])
        file_id = fp._id

    if grid_fs.find_one(file_id) is not None:
        print("Success")
        return redirect(url_for('index'))
    else:
        print("Fail")
        return render_template('home/upload_failed')
