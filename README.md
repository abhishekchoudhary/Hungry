#Hungry
=======

Demo server. Meant to mimic a food service backend. Python + SQLite FTW!

##APIs
 - Order
 - Food Items

####The Order API
######Fetch
`__SERVER__/order/fetch/<order_id>`
Meant to fetch the complete details of an order.

######Rain
`__SERVER__/order/rain`
Gets a list of all orders present. Can be filtered by status using 'status' in a URL parameter (logically, 0 is 'placed', 1 is 'in transit', 2 is 'delivered', 3 is 'cancelled')

######Keep
 - `__SERVER__/order/keep`
 - `__SERVER__/order/keep/<order_id>`
Invoke without order ID to save a new order, with order ID to update existing. Only need supply the changed parameters in the API if updating existing records. Takes `customer_id`, `items`, `status_track` as parameters. `customer_id` should exist beforehand (foreign key with `customers` table), `items` is a comma-separated list of item IDs in the menu, and `status_track` is the status of the order.

####The Food Item API
######Fetch
`__SERVER__/item/fetch/<item_id>`
Meant to fetch the complete details of an item.

######Rain
`__SERVER__/order/rain`
Gets a list of all items on the menu.


##Setup
 - Install dependencies from `requirements.txt`
 - Run `bootstrap.py` to seed the database
 - Run server with `run.py`

