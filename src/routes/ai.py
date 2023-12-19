from flask import (
    Blueprint
)
import sys

sys.path.append('../src')
from src.controllers.generalController import general, verifyUser, uploadPhoto

bp = Blueprint('ai', __name__, url_prefix='/ai')

bp.route('/general', methods=['GET'])(general)
bp.route('/verifyUser', methods=['POST'])(verifyUser)
bp.route('/registerUser', methods=['POST'])(uploadPhoto)