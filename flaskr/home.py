from flask import (
    Blueprint, g, render_template, request, make_response, jsonify
)
from datetime import datetime
from werkzeug.exceptions import abort

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
    end_files = []
    if g.user is not None:
        u_files = (db.mongo.db.users.find_one({"_id": ObjectId(g.user["_id"])}))["files"]
        for file in u_files:
            expires_at = datetime.strptime(file["filename"].split("__", 3)[2], '%Y-%m-%dT%H:%M')
            datetime_now = datetime.utcnow()
            if expires_at <= datetime_now:
                grid_fs = get_grid_fs()
                grid_fs.delete({'filename': file["filename"]})
                db.mongo.db.users.update_one({"_id": ObjectId(g.user["_id"])},
                                             {"$pull": {"files": {"filename": file["filename"]}}})
            else:
                end_files.append(file)
    return render_template('home/index.html', files=end_files)


@login_required
@bp.route('/upload', methods=["POST"])
def upload():
    grid_fs = get_grid_fs()
    expires_at = datetime.strptime(request.form["expires"], '%Y-%m-%dT%H:%M')
    if expires_at <= datetime.utcnow():
        return jsonify(error="Invalid expire date")
    filename = str(g.user["_id"]) + "__" + str(datetime.utcnow()) + "__" + \
               request.form["expires"] + "__" + request.files["file"].filename

    with grid_fs.new_file(filename=filename) as fp:
        fp.write(request.files["file"])
        file_id = fp._id

    if grid_fs.find_one(file_id) is not None:
        db.mongo.db.users.update_one({"_id": ObjectId(g.user["_id"])},
                                     {"$push": {"files": {"filename": filename, "file_id": file_id}}})
        return jsonify(fileurl=filename, filename=filename.split("__", 3)[3])
    else:
        return jsonify(error="Upload failed for absolutely no reason")


@bp.route('/download/<string:filename>')
def download(filename):
    grid_fs = get_grid_fs()
    grid_fs_file = grid_fs.find_one({'filename': filename})

    if grid_fs_file is not None:
        expires_at = datetime.strptime(filename.split("__", 3)[2], '%Y-%m-%dT%H:%M')
        datetime_now = datetime.utcnow()
        if expires_at >= datetime_now:
            response = make_response(grid_fs_file.read())
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.split("__", 3)[3])
            return response
        grid_fs.delete({'filename': filename})
        db.mongo.db.users.update_one({"_id": ObjectId(filename.split("__", 1)[0])},
                                     {"$pull": {"files": {"filename": filename}}})
    abort(404, "File with name {0} doesn't exist.".format(filename))


@bp.route('/<string:filename>')
def file_page(filename):
    grid_fs = get_grid_fs()
    if grid_fs.find_one({'filename': filename}) is not None:
        expires_at = datetime.strptime(filename.split("__", 3)[2], '%Y-%m-%dT%H:%M')
        datetime_now = datetime.utcnow()
        if expires_at >= datetime_now:
            return render_template('home/file.html', filename=filename.split("__", 3)[3], fileurl=filename)
        grid_fs.delete({'filename': filename})
        db.mongo.db.users.update_one({"_id": ObjectId(filename.split("__", 1)[0])},
                                     {"$pull": {"files": {"filename": filename}}})
    abort(404, "File with name {0} doesn't exist.".format(filename))

