from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from surf24 import db
from surf24.models import Advert, Picture, Category
from surf24.ads.forms import AdForm, PicForm, CategoryForm
from surf24.ads.picture_handler import add_ad_pic, del_pic

ads = Blueprint('ads', __name__)

@ads.route('/create', methods=['GET', 'POST'])
@login_required
def create_ad():
    form = AdForm()
    picForm = PicForm()
    choices = ["one", "two", "three"]
    #hoices = Category.query.filter_by(parent=1)
    choices1 = Category.query.filter_by(parent=1)

    for element in choices1:
            choices.append(element.name)
    #print(choices)
    categoryForm = CategoryForm()
    #with_entities(SomeModel.col1, SomeModel.col2)
    categoryForm.category.choices = choices

    if form.validate_on_submit():

        advert = Advert(title=form.title.data,
                            text = form.text.data,
                            user_id = current_user.id,
                            price = form.price.data)
        db.session.add(advert)
        db.session.commit()
        db.session.flush()

        if picForm.validate_on_submit():
            if picForm.picture1.data:
                filename = add_ad_pic(picForm.picture1.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture2.data:
                filename = add_ad_pic(picForm.picture2.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture3.data:
                filename = add_ad_pic(picForm.picture3.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture4.data:
                filename = add_ad_pic(picForm.picture4.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture5.data:
                filename = add_ad_pic(picForm.picture5.data, advert.id)
                picture = Picture(advert_id=advert.id, image=filename)
                db.session.add(picture)
                db.session.commit()

        return redirect(url_for('core.index'))
    return render_template('create_ad.html', form=form, picForm=picForm, categoryForm = categoryForm)

@ads.route('/<int:ad_id>')
def advert(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    return render_template('ad.html', ad=ad)


@ads.route("/<int:ad_id>/update", methods=['GET','POST'])
@login_required
def update(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(403)

    form = AdForm()
    picForm = PicForm()
    if form.validate_on_submit():
        ad.title = form.title.data
        ad.text = form.text.data
        ad.price = form.price.data
        db.session.add(ad)
        db.session.commit()
        db.session.flush()

        if picForm.validate_on_submit():
            if picForm.picture1.data:
                filename = add_ad_pic(picForm.picture1.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture2.data:
                filename = add_ad_pic(picForm.picture2.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture3.data:
                filename = add_ad_pic(picForm.picture3.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture4.data:
                filename = add_ad_pic(picForm.picture4.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
            if picForm.picture5.data:
                filename = add_ad_pic(picForm.picture5.data, ad_id)
                picture = Picture(advert_id=ad_id, image=filename)
                db.session.add(picture)
                db.session.commit()
        return redirect(url_for('ads.advert', ad_id = ad_id))
    elif request.method == 'GET':
        form.title.data = ad.title
        form.text.data = ad.text
        form.price.data = ad.price

    return render_template('create_ad.html', title='Updating', form=form, picForm=PicForm(), ad=ad)
@ads.route('/<int:ad_id>/delete', methods=['GET','POST'])
@login_required
def delete(ad_id):
    ad=Advert.query.get_or_404(ad_id)

    pics=Picture.query.filter_by(advert_id=ad_id)
    if ad.author != current_user:
        abort(403)
    for picfile in pics:
        del_pic(picfile.image)
        db.session.delete(picfile)
        db.session.commit()

    db.session.delete(ad)
    db.session.commit()

    flash('Kuulutus kustutatud!')
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
    return redirect(url_for('ads.advert', ad_id = ad.id))
    #return render_template('create_ad.html', title='Updating', form=AdForm(), picForm=PicForm(), ad=ad.id)
