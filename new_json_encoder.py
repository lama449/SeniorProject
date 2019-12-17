from flask.json import JSONEncoder
from bson import ObjectId, Timestamp
from datetime import datetime

class New_JSON_Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)
