from flask import Flask, render_template, jsonify, g, request
from werkzeug.datastructures import CombinedMultiDict, MultiDict
import sys
import commons

# Define the WSGI application object
app = Flask(__name__)

# trying to config parameters
try:
    app.config.from_object('config')
except Exception as e:
    print 'environment config not found'
    sys.exit(1)

if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('flask_error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

@app.before_request
def pre():
    g.incoming = CombinedMultiDict([request.args, request.form])
    g.request_start_time = commons.Toolkit.get_timestamp()
    g.processing_time = lambda: int(g.request_end_time - g.request_start_time)
    g.incoming_files = request.files.keys()

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status' : 'error', 'message' : "Page found, but we'll not show you."}), 404

@app.errorhandler(405)
def not_found(error):
    return jsonify({'status' : 'error', 'message' : 'Is this the right HTTP method?'}), 405

@app.errorhandler(500)
def internal_error(exception):
  app.logger.exception(exception)
  return render_template('500.html'), 500

# set up static file serving endpoint in debug mode
if app.debug is True:
    @app.route('/<path:path>')
    def static_proxy(path):
        # send_static_file will guess the correct MIME type
        return app.send_static_file(path)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.orders.controllers import api as order_api
from app.items.controllers import api as item_api

# Register blueprint(s)
app.register_blueprint(order_api)
app.register_blueprint(item_api)
