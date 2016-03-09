import wrappers

class Item:
    _exists = False
    __TRACKED_FIELDS = ["price", "name"]

    def __init__(self, item_id):
        # Can't fetch from DB
        if item_id is None:
            return
        db = wrappers.SQLite.init()
        cursor = db.cursor()
        fields = ', '.join(self.__TRACKED_FIELDS)
        row_id = item_id
        self.id = int(item_id)
        # Selecting necessary fields from the databsae for object initialization
        a_query = "SELECT " + fields + " FROM items WHERE id = :row_id"
        cursor.execute(a_query, {"row_id": row_id})
        result = cursor.fetchone()

        db.close()

        # If no result is found for the relevant ID
        if result == None:
            return

        # Otherwise, populate the object with values from the database
        self._exists = True
        index = 0
        for a_field in self.__TRACKED_FIELDS:
            value = result[index]
            setattr(self, a_field, value)
            index += 1

    # Utility function to export an object's data to a dict
    def export(self):
        data_dict = {}
        attributes = [a for a in dir(self) if not a.startswith('_') and not callable(getattr(self,a))]
        for an_attribute in attributes:
            data_dict[an_attribute] = getattr(self, an_attribute)

        if self._exists:
            del data_dict['id']
            data_dict['item_id'] = self.id

        return data_dict
