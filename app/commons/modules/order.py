from models.Order import Order
from app.commons.Toolkit import enumerate_table
from copy import deepcopy

def fetch(order_id, incoming):
    requested_order = Order(order_id=order_id)
    response = {'exists' : False, 'status': 'failure'}

    if requested_order._exists == True:
        response['exists'] = True
        response['status'] = 'success'
        response['data'] = requested_order.export()

    return response

def keep(order_id, incoming):
    response = {}

    an_order = Order(order_id=order_id)
    an_order.consume(incoming)
    saved_id = an_order.save()

    if saved_id is None:
        response['status'] = 'failed'
        response['message'] = 'There was a problem with saving this record. Please check your request!'
        response['http_status'] = 412
    else:
        response['status'] = 'success'
        response['message'] = 'Record saved!'
        response['storage_id'] = saved_id

    return response

def rain(incoming):
    response = {}
    filters = {}
    if 'status' in incoming:
        filters['status']  = incoming['status']
    all_order_ids = enumerate_table('orders', filters)

    if len(all_order_ids) == 0:
        response['status'] = 'failed'
        response['message'] = 'No relevant data found!'
    else:
        response['status'] = 'success'
        response['data'] = []

    for an_order_id in all_order_ids:
        an_order = Order(order_id=an_order_id)
        response['data'].append(deepcopy(an_order.export()))

    return response
