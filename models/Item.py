import wrappers

class Item:
    _exists = False
    __TRACKED_FIELDS = ["price", "name"]

    def __init__(self, item_id):
        db = wrappers.SQLite.init()
        cursor = db.cursor()
        fields = ', '.join(self.__TRACKED_FIELDS)
        row_id = item_id
        self.id = int(item_id)
        a_query = "SELECT " + fields + " FROM items WHERE id = :row_id"
        cursor.execute(a_query, {"row_id": row_id})
        result = cursor.fetchone()

        db.close()
        if result == None:
            return

        self._exists = True
        index = 0
        for a_field in self.__TRACKED_FIELDS:
            value = result[index]
            setattr(self, a_field, value)
            index += 1

    def export(self, to_database=False):
        data_dict = {}
        attributes = [a for a in dir(self) if not a.startswith('_') and not callable(getattr(self,a))]
        for an_attribute in attributes:
            data_dict[an_attribute] = getattr(self, an_attribute)

        if self._exists:
            del data_dict['id']
            data_dict['item_id'] = self.id

        return data_dict
