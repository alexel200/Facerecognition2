from flask import (
    Blueprint
)

from src.controllers.generalController import general, verifyUser, uploadPhoto

bp = Blueprint('ai', __name__, url_prefix='/ai')

bp.route('/general', methods=['GET'])(general)
bp.route('/verifyUser', methods=['POST'])(verifyUser)
bp.route('/registerUser', methods=['POST'])(uploadPhoto)