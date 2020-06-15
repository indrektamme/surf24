from flask import Blueprint, render_template
from flask_login import login_user, current_user, logout_user, login_required

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html' , current_user=current_user)
