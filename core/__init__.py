from flask import Blueprint

bp = Blueprint('core', __name__)

from core import routes
