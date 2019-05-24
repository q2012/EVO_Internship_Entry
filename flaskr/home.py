from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
import datetime

from flaskr.auth import login_required
from . import db
from flask_pymongo import GridFS
from bson import ObjectId

bp = Blueprint('home', __name__)


def get_grid_fs():
    if db.mongo is not None and db.grid_fs is None:
        db.grid_fs = GridFS(db.mongo.db)
    return db.grid_fs


@bp.route('/')
def index():
    u_files = None
    if g.user is not None:
        u_files = (db.mongo.db.users.find_one({"_id": ObjectId(g.user["_id"])}))["files"]
    return render_template('home/index.html', files=u_files)


@login_required
@bp.route('/upload', methods=["POST"])
def upload():
    grid_fs = get_grid_fs()
    file_url = str(datetime.datetime.now())
    with grid_fs.new_file(filename=file_url) as fp:
        fp.write(request.files["file"])
        file_id = fp._id

    if grid_fs.find_one(file_id) is not None:
        print("Success")
        db.mongo.db.users.update_one({"_id": ObjectId(g.user["_id"])}, {"$push": {"files": {"fileurl": file_url, "file_id": file_id} }})
        return redirect(url_for("index"))
    else:
        print("Fail")
        return render_template('home/upload_failed')

@bp.route('/download/<string:filename>')
def download(filename):
    grid_fs = get_grid_fs()
    grid_fs_file = grid_fs.find_one({'filename': filename})

    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response
