"""Create an application instance."""

from flask.helpers import get_debug_flag

from src.main import create_app
from src.settings import DevelopConfig, ProductionConfig

CONFIG = DevelopConfig if get_debug_flag() else ProductionConfig

app = create_app(CONFIG)
