from flask.json import JSONEncoder
from bson import ObjectId, Timestamp

class New_JSON_Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Timestamp):
            return str(o)
        return JSONEncoder.default(self, o)
