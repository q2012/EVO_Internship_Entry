from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('home/index.html')
