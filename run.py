"""
    Application entry point
"""

from app import app
import config

app.run(host='127.0.0.1', port=config.PORT, debug=config.DEBUG)
