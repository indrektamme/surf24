from flask import Blueprint, render_template, request
from flask_login import login_user, current_user, logout_user, login_required
from surf24.models import Advert
core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    adverts = Advert.query.order_by(Advert.date.desc()).paginate(page=page,per_page=per_page)
    return render_template('index.html' , current_user=current_user, adverts=adverts)
