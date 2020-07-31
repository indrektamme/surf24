from flask import Blueprint, render_template, request, session
from flask_login import login_user, current_user, logout_user, login_required
from surf24.models import Advert, AdvertCategory, Category
from surf24.core.forms import FilterForm
from surf24.categories.views import makeCategoryForm
from flask_login import current_user, login_required
from surf24 import db
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from pprint import pprint

core = Blueprint('core',__name__)
@core.route('/', methods=['GET', 'POST'])
def index():
    filterForm = FilterForm()
    categoryForm = makeCategoryForm(filterForm.category1.data , filterForm.category2.data, filterForm.category3.data, 0, "", filterForm)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    # sellise päringu teen juppideks:
    # adverts = db.session.query(Advert, AdvertCategory).join(AdvertCategory).filter_by(category1=23).filter_by(category2=26).order_by(Advert.date.desc()).paginate(page=page,per_page=per_page)

    if filterForm.brand.data == None: print("brand on tyhi")
    else: print("brand ei ole tyhi")


    # filtrid sessiooni
    if filterForm.hidden_if_form_sent.data != None:
        session['filter_size'] = filterForm.size.data
        session['filter_sizeMax'] = filterForm.sizeMax.data
        session['filter_brand'] = filterForm.brand.data
        session['filter_price'] = filterForm.price.data
        session['filter_priceMax'] = filterForm.priceMax.data
        session['filter_searchKeyword'] = filterForm.searchKeyword.data
        session['filter_category1'] = filterForm.category1.data
        session['filter_category2'] = filterForm.category2.data
        session['filter_category3'] = filterForm.category3.data
    else:
        filterForm.size.data = session.get('filter_size', '')
        filterForm.sizeMax.data = session.get('filter_sizeMax', '')
        filterForm.brand.data = session.get('filter_brand', '')
        filterForm.price.data = session.get('filter_price', '')
        filterForm.priceMax.data = session.get('filter_priceMax', '')
        filterForm.searchKeyword.data = session.get('filter_searchKeyword', '')
        filterForm.category1.data = session.get('filter_category1', '')
        filterForm.category2.data = session.get('filter_category2', '')
        filterForm.category3.data = session.get('filter_category3', '')


    adverts = db.session.query(Advert, AdvertCategory, Category).join(AdvertCategory)
    if filterForm.category1.data != None and filterForm.category1.data > 20 :
        adverts = adverts.filter_by(category1=filterForm.category1.data)

    if filterForm.category2.data != None and filterForm.category2.data > 20 :
        adverts = adverts.filter_by(category2=filterForm.category2.data)

    if filterForm.category3.data != None and filterForm.category3.data > 20 :
        adverts = adverts.filter_by(category3=filterForm.category3.data)

    if filterForm.size.data != None and filterForm.size.data > 0 :
        adverts = adverts.filter(AdvertCategory.size >= float(filterForm.size.data))

    if filterForm.sizeMax.data != None and filterForm.sizeMax.data > 0 :
        adverts = adverts.filter(AdvertCategory.size <= float(filterForm.sizeMax.data))

    if filterForm.brand.data != None and filterForm.brand.data != "":
        adverts = adverts.filter(AdvertCategory.brand.like('%'+filterForm.brand.data+'%'))


#    print(f"sessioon t66tab: {session.get('ok', '')}")
    if filterForm.price.data != None:
        filterForm.price.data = filterForm.price.data

        if filterForm.price.data == 0:
            adverts = adverts.filter(or_(AdvertCategory.price >= float(0), AdvertCategory.price == None))
            filterForm.price.data = filterForm.price.data
        else:
            k=filterForm.price.data
            print(f"see on {filterForm.price.data}")
            adverts = adverts.filter(AdvertCategory.price >= float(filterForm.price.data))
            filterForm.price.data = k
    if filterForm.priceMax.data != None:
        page=1
        if filterForm.priceMax.data == 0:
            adverts = adverts.filter(or_(AdvertCategory.price <= float(0), AdvertCategory.price == None))
        else:
            adverts = adverts.filter(or_(AdvertCategory.price <= float(filterForm.priceMax.data), AdvertCategory.price == None))
    if filterForm.searchKeyword.data != None and filterForm.searchKeyword.data != "":
        adverts = adverts.filter(Advert.text.like('%'+filterForm.searchKeyword.data+'%'))
        page=1

    adverts = adverts.join(Category, AdvertCategory.category1==Category.id)
    adverts = adverts.order_by(Advert.date.desc()).paginate(page=page,per_page=per_page)

    # nii saab printida muutujad
    # pprint(vars(adverts))



    return render_template('index.html' , current_user=current_user, adverts=adverts, filterForm=filterForm)

@core.route('/my', methods=['GET', 'POST'])
def myAdverts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    adverts = Advert.query.filter_by(author=current_user).order_by(Advert.date.desc()).paginate(page=page,per_page=per_page)
    # et saaks kasutada sama template: siis on keerukam sql, nagu / routes
    adverts = db.session.query(Advert, AdvertCategory).filter_by(author=current_user).join(AdvertCategory).order_by(Advert.date.desc()).paginate(page=page,per_page=per_page)

    return render_template('index.html' , current_user=current_user, adverts=adverts)
