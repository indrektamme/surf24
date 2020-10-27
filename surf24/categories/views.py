from surf24 import db
from flask import Blueprint, render_template, redirect, url_for, session
from surf24.models import Category, User
from surf24.categories.forms import CategoryForm, EditCategoryForm
from flask_login import login_user, current_user, logout_user, login_required
from surf24.users.roles import Roles

categories = Blueprint('categories', __name__)

def makeCategoryForm(choice1, choice2, choice3, size=0, brand="", form = None):
    if size == None: size = 0
    if form == None: form = CategoryForm()
    form.category1.choices = createCategoryChoices(0)
    form.category2.choices = createCategoryChoices(choice1)
    if ifCategoryHasParent(choice2, choice1): form.category3.choices = createCategoryChoices(choice2)

    if float(size) > 0: form.size.data = size
    if brand: form.brand.data = brand
    form.category1.default = choice1
    form.category2.default = choice2
    form.category3.default = choice3

    return form

def createCategoryChoices(parent):
    choices = []
    if parent == None: parent = 1000
    choices1 = Category.query.filter_by(parent=parent).all()
    for element in choices1:
        sequence = (element.id, element.en)
        if (session['lang'] == 'et'):
            sequence = (element.id, element.et)
        if (session['lang'] == 'es'):
            sequence = (element.id, element.es)
        if (session['lang'] == 'ru'):
            sequence = (element.id, element.ru)

        choices.append(sequence)
    return choices

def ifCategoryHasParent(categoryId, parentId):
    if categoryId:
        category = Category.query.get(categoryId)
        if category != None:
            if category.parent == parentId:
                return True
    return False


@categories.route("/admin_categories")
@login_required
def admin_categories():
    if current_user.role == Roles.ADMIN:
        categories = Category.query.all()
        return render_template('admin_categories.html', categories=categories, Roles=Roles)
    else:
        return redirect(url_for('core.index'))


@categories.route("/admin_add_category")
@login_required
def admin_add_category():
    if current_user.role == Roles.ADMIN:
        category = db.session.query(Category).filter_by(en = None, order = None, parent = None).first()
        if category:
            return redirect(url_for('categories.admin_edit_category', cat_id=category.id))
        else:
            category = Category()
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('categories.admin_edit_category', cat_id=category.id))
    return redirect(url_for('categories.admin_edit_category', cat_id=cat.id))




@categories.route("/<int:cat_id>/admin_edit_category", methods=['GET','POST'])
@login_required
def admin_edit_category(cat_id):
    form = EditCategoryForm()
    if current_user.role == Roles.ADMIN:
        category = Category.query.get(cat_id)
        if form.validate_on_submit():
            category.en = form.en.data
            if form.en.data == "":
                category.en = None
            category.parent = form.parent.data
            category.order = form.order.data

            category.et = form.et.data
            category.ru = form.ru.data
            category.es = form.es.data

            db.session.commit()
            db.session.flush()
            return redirect(url_for('categories.admin_categories'))
        else:
            form.parent.data = category.parent
            form.en.data = category.en
            form.order.data = category.order
            form.order.et = category.et
            form.order.ru = category.ru
            form.order.es = category.es
            return render_template('admin_edit_category.html', category=category, Roles=Roles, form = form)
    else:
        return redirect(url_for('core.index'))
