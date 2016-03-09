import wrappers

class Order:
    _exists = False
    __TRACKED_FIELDS = ["customer_id", "status"]
    __IMMUTABLE_FIELDS = ["created_at", "updated_at"]

    def __init__(self, order_id):
        db = wrappers.SQLite.init()
        cursor = db.cursor()
        fields = ', '.join(self.__TRACKED_FIELDS + self.__IMMUTABLE_FIELDS)
        row_id = order_id
        self.id = int(order_id)
        a_query = "SELECT " + fields + " FROM orders WHERE id = :row_id"
        cursor.execute(a_query, {"row_id": row_id})
        result = cursor.fetchone()
        if result == None:
            db.close()
            return

        self._exists = True
        index = 0
        for a_field in self.__TRACKED_FIELDS + self.__IMMUTABLE_FIELDS:
            value = result[index]
            setattr(self, a_field, value)
            index += 1
        items_query = "SELECT item_id FROM orders_items WHERE order_id = :order_id"
        cursor.execute(items_query, {"order_id": row_id})
        result = cursor.fetchall()
        self.items = map(lambda x: x[0], result)
        db.close()

    def consume(self, data):
        for a_field in self.__TRACKED_FIELDS:
            if a_field not in data:
                try:
                    value = getattr(self, a_field)
                except AttributeError:
                    value = None
            else:
                value = data[a_field]
            setattr(self, a_field, value)

        if 'items' in data:
            self.items = map(int, data['items'].split(','))

    def export(self, to_database=False):
        data_dict = {}
        attributes = [a for a in dir(self) if not a.startswith('_') and not callable(getattr(self,a))]
        for an_attribute in attributes:
            data_dict[an_attribute] = getattr(self, an_attribute)

        if self._exists:
            del data_dict['id']
            data_dict['order_id'] = self.id

        data_dict['items'] = ','.join(map(str, self.items))

        return data_dict

    def save(self, create_new=False):
        if self._exists == False:
            create_new = True

        db = wrappers.SQLite.init()
        cursor = db.cursor()

        if create_new == True:
            a_query = """
                INSERT INTO orders
                (""" + ', '.join(self.__TRACKED_FIELDS) +  """)
                VALUES ( :""" + ', :'.join(self.__TRACKED_FIELDS) + """ )
            """
        else:
            update_params = wrappers.SQLite.get_update_params(self.__TRACKED_FIELDS)
            a_query = " UPDATE orders SET " + update_params + " WHERE id=:id"
            storage_id = self.id

        try:
            cursor.execute(a_query, self.export(to_database=True))
            storage_id = cursor.lastrowid
            if not create_new:
                storage_id = self.id
                cursor.execute("DELETE FROM orders_items WHERE order_id = :order_id", {'order_id': item_id})

            order_item_query = "INSERT INTO orders_items (order_id, item_id) VALUES (:order_id, :item_id)"
            items = map(int, self.items.split(','))

            for an_item in items:
                cursor.execute(order_item_query, {'order_id': self.id, 'item_id': an_item})
        except Exception, e:
            print e
            storage_id = None

        db.commit()
        db.close()
        return storage_id
