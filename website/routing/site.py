from . import ROUTES

from flask import Blueprint, render_template

site = Blueprint('site', __name__)


@site.route('/')
def index():
    return render_template("site/index.html")


@site.route('/privacy')
def privacy():
    return render_template("site/privacy.html")


@site.route('/impressum')
def impressum():
    return render_template("site/impressum.html")


@ROUTES.init_task
def init():
    from .. import APP
    APP.register_blueprint(site)
