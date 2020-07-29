from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from surf24 import db
from surf24.models import Advert, Picture, Category, AdvertCategory
from surf24.ads.forms import AdForm, PicForm, CategoryForm
from surf24.ads.picture_handler import add_ad_pic, del_pic
from surf24.categories.views import makeCategoryForm
from surf24.categories.forms import CategoryForm

ads = Blueprint('ads', __name__)

@ads.route('/create', methods=['GET', 'POST'])
@login_required
def create_ad():
    form = AdForm()
    picForm = PicForm()

    categoryForm = makeCategoryForm(0, 0, 0)
    categoryForm = makeCategoryForm(categoryForm.category1.data , categoryForm.category2.data, categoryForm.category3.data)

    if form.validate_on_submit():
        advert = Advert(title=form.title.data,
                            text = form.text.data,
                            user_id = current_user.id,
                            price = form.price.data)
        db.session.add(advert)
        db.session.commit()
        db.session.flush()

        if categoryForm.validate_on_submit():
            advertcategory = AdvertCategory(category1=categoryForm.category1.data, category2=categoryForm.category2.data, category3=categoryForm.category3.data, advert_id=advert.id, size = categoryForm.size.data, brand = categoryForm.brand.data)
            db.session.add(advertcategory)
            db.session.commit()
        else:
            print(categoryForm.errors)
            print(categoryForm.category.data)

        if picForm.validate_on_submit():
            if picForm.picture.data:
                filename = add_ad_pic(picForm.picture.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()
                #return render_template('create_ad.html', title='Lisa kuulutus', form=form, picForm=PicForm(), ad=advert, categoryForm=categoryForm)
    if form.submitbutton.data: return redirect(url_for('ads.update', ad_id=advert.id))
    return render_template('create_ad.html', title='add question',  form=form, picForm=picForm, categoryForm = categoryForm)




@ads.route('/<int:ad_id>')
def advert(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    # categories = db.session.query(AdvertCategory, Category).join(Category, AdvertCategory.category1==Category.id)
    categories = db.session.query(AdvertCategory, Category).filter_by(advert_id=40).join(Category, AdvertCategory.category1==Category.id)
    #categories = db.session.query(Advert, AdvertCategory).filter_by(id=ad_id)\
    #    .outerjoin(Advert, AdvertCategory.advert_id==Advert.id)\
    #    .outerjoin(AdvertCategory, Category.id==AdvertCategory.category1)

    #join(Category, AdvertCategory.category1==Category.id)
    #.filter_by(id=2)
    return render_template('ad.html', ad=ad, categories=categories)

@ads.route("/<int:ad_id>/update", methods=['GET','POST'])
@login_required
def update(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(403)
    form = AdForm()
    picForm = PicForm()

    categories = AdvertCategory.query.filter_by(advert_id=ad_id).first()
    categoryForm = CategoryForm()
    # send values to makeCategoryForm
    if categoryForm.category1.data == None: categoryForm.category1.data = categories.category1
    if categoryForm.category2.data == None: categoryForm.category2.data = categories.category2
    if categoryForm.category3.data == None: categoryForm.category3.data = categories.category3
    categoryForm = makeCategoryForm(categoryForm.category1.data, categoryForm.category2.data, categoryForm.category3.data, categoryForm.size.data, brand = categoryForm.brand.data)
    # make default values visable!
    if categoryForm.category1.data == None: categoryForm.category1.data = categories.category1
    if categoryForm.category2.data == None: categoryForm.category2.data = categories.category2
    if categoryForm.category3.data == None: categoryForm.category3.data = categories.category3
    if categoryForm.size.data == None: categoryForm.size.data = categories.size
    if categoryForm.brand.data == None: categoryForm.brand.data = categories.brand


    if form.validate_on_submit():
        ad.title = form.title.data
        ad.text = form.text.data
        ad.price = form.price.data
        db.session.commit()
        db.session.flush()

        if categoryForm.validate_on_submit():
            categories.brand = categoryForm.brand.data
            categories.category1 = categoryForm.category1.data
            categories.category2 = categoryForm.category2.data
            categories.category3 = categoryForm.category3.data
            categories.size = categoryForm.size.data
            db.session.commit()
        if picForm.validate_on_submit():
            if picForm.picture.data:
                print("hakka pilti salvestama")
                filename = add_ad_pic(picForm.picture.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
        if form.submitbutton.data:
            return redirect(url_for('ads.advert', ad_id = ad_id))
    elif request.method == 'GET':
        form.title.data = ad.title
        form.text.data = ad.text
        form.price.data = ad.price
    return render_template('create_ad.html', title='Updating', form=form, picForm=PicForm(), ad=ad, categoryForm=categoryForm)




@ads.route('/<int:ad_id>/delete', methods=['GET','POST'])
@login_required
def delete(ad_id):
    ad=Advert.query.get_or_404(ad_id)
    pics=Picture.query.filter_by(advert_id=ad_id)
    ad_categories = AdvertCategory.query.filter_by(advert_id=ad_id)

    if ad.author != current_user:
        abort(403)
    for cat in ad_categories:
        db.session.delete(cat)
        db.session.commit()
    for picfile in pics:
        del_pic(picfile.image)
        db.session.delete(picfile)
        db.session.commit()
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('core.index'))

@ads.route('/<int:pic_id>/delete_image', methods=['GET','POST'])
@login_required
def delete_image(pic_id):
    pic=Picture.query.get_or_404(pic_id)
    ad=Advert.query.get_or_404(pic.advert_id)
    if ad.author != current_user:
        abort(403)
    del_pic(pic.image)
    db.session.delete(pic)
    db.session.commit()
    return redirect(url_for('ads.update', ad_id = ad.id))
