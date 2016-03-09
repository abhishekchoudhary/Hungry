"""
    Controller to dictate working of __URL__/items/ and all associated APIs.
"""
from flask import Blueprint, request, g
from app.commons.CORS import crossdomain
from app.commons.Toolkit import respond, get_timestamp
import models
import app.commons.modules as modules
from werkzeug.datastructures import CombinedMultiDict, MultiDict

# Setting up access to this controller under '<OUR_AWESOME_DOMAIN>/items/*'
api = Blueprint('items', __name__, url_prefix='/items')

@api.route('/', methods=['POST', 'GET'])
@crossdomain(origin='*')
def base():
    """
        The base method for this controller does not need to do anything.
        A list of methods is possible, but might make us vulnerable.
        So we just do something fun for the time being.
    """
    request_timestamp = get_timestamp()
    response = {
        'message': "We don't make coffee. How about an XKCD instead?",
        'alternative': 'https://c.xkcd.com/random/comic/',
        'status': "It's complicated",
        'http_status': 418
    }

    # Returning with the joke 418 status code, because why not
    return respond(response)

@api.route('/fetch/<item_id>', methods=['GET'])
@crossdomain(origin='*')
def fetch(item_id):
    response = modules.item.fetch(item_id, g.incoming)
    return respond(response)

@api.route('/rain',methods=['GET'])
@crossdomain(origin='*')
def rain():
    response=modules.item.rain(g.incoming)
    return respond(response)
