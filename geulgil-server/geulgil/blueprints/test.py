from flask import Blueprint, jsonify

bp = Blueprint('test', __name__)


@bp.route('/')
def test():
    return jsonify({"status": "ok"})
