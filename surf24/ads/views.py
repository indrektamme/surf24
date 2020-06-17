from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from surf24 import db
from surf24.models import Advert
from surf24.ads.forms import AdForm

ads = Blueprint('ads', __name__)


@ads.route('/create', methods=['GET', 'POST'])
@login_required
def create_ad():
    form = AdForm()

    if form.validate_on_submit():
        advert = Advert(title=form.title.data,
                            text = form.text.data,
                            user_id = current_user.id)

        db.session.add(advert)
        db.session.commit()
        flash('Kuulutus lisatud')
        return redirect(url_for('core.index'))

    return render_template('create_ad.html', form=form)


@ads.route('/<int:ad_id>')
def advert(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    # return render_template('ad.html', title=ad.title, date = ad.date, post = ad.text)
    return render_template('ad.html', ad=ad)

#update

@ads.route("/<int:ad_id>/update", methods=['GET','POST'])
@login_required
def update(ad_id):
    ad = Advert.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(403)

    form = AdForm()

    if form.validate_on_submit():
        ad.title = form.title.data
        ad.text = form.text.data

        db.session.add(ad)
        db.session.commit()
        flash('Kuulutus on uuendatud')
        return redirect(url_for('ads.ad', ad_id = ad.id))

    elif request.method == 'GET':
        form.title.data = ad.title
        form.text.data = ad.text

    return render_template('create_ad.html', title='Updating', form=form)
@ads.route('/<int:ad_id>/delete', methods=['GET','POST'])
@login_required
def delete(ad_id):
    ad=Advert.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(403)

    db.session.delete(ad)
    db.session.commit()
    flash('Kuulutus kustutatud!')
    return redirect(url_for('core.index'))
