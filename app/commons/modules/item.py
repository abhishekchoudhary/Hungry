from models.Item import Item
from app.commons.Toolkit import enumerate_table
from copy import deepcopy

def fetch(item_id, incoming):
    requested_item = Item(item_id=item_id)
    response = {'exists' : False, 'status': 'failure'}

    if requested_item._exists == True:
        response['exists'] = True
        response['status'] = 'success'
        response['data'] = requested_item.export()

    return response

def rain(incoming):
    response = {}
    filters = {}
    all_item_ids = enumerate_table('items', filters)

    if len(all_item_ids) == 0:
        response['status'] = 'failed'
        response['message'] = 'No relevant data found!'
    else:
        response['status'] = 'success'
        response['data'] = []

    for an_item_id in all_item_ids:
        an_item = Item(item_id=an_item_id)
        response['data'].append(deepcopy(an_item.export()))

    return response
