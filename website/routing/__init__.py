from .. import APP
from packing import Package

from flask import redirect, render_template
from pathlib import Path

ROUTES = Package(Path(__file__).parent)


def back_home():
    return redirect('/')


@APP.route('/<path:path>')
def not_found(path):
    return render_template("404.html")
