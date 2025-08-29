from debugger import log, start_session

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from types import FrameType
import warnings, os, signal

warnings.filterwarnings("ignore", message="Using the in-memory storage for tracking rate limits")

APP = Flask(__name__)
APP.subdomain_matching = True
APP.wsgi_app = ProxyFix(APP.wsgi_app, x_for=1, x_proto=1, x_host=1)
LIMITER = Limiter(get_remote_address, default_limits=["500 per day", "100 per hour"])


DEBUG = False


def _on_shutdown(signum: int, frame: FrameType | None):
    log('info', f"""Handling signal {
    'SIGTERM' if signum == signal.SIGTERM else 'SIGINT'
    }, shutting down...""")

    # TODO: Implement shutdown routine


def init_app(db_manage: bool = False):
    from packing import ROOT_PATH
    load_dotenv(os.path.join(ROOT_PATH, '.env'))

    APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

    from .data import DB, BCRYPT, MIGRATE

    DB.init_app(APP)
    BCRYPT.init_app(APP)
    MIGRATE.init_app(APP, DB)

    if db_manage:
        return

    global DEBUG
    DEBUG = os.getenv("INSTANCE") == 'debug'

    APP.config['SERVER_NAME'] = os.getenv("SERVER_NAME")
    APP.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    APP.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    APP.config["MAX_FORM_MEMORY_SIZE"] = 16 * 1024 * 1024

    APP.config['RATELIMIT_STORAGE_URL'] = os.getenv("REDIS_URI")
    LIMITER.init_app(APP)

    start_session()

    from .routing import ROUTES
    ROUTES.initialize()

    signal.signal(signal.SIGINT, _on_shutdown)
    signal.signal(signal.SIGTERM, _on_shutdown)
