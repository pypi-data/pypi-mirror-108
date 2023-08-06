from flask_marshmallow import Marshmallow as _Marshmallow, Schema as _Schema


class Marshmallow(_Marshmallow):

    def __init__(self):
        super(Marshmallow, self).__init__()
        self.Schema = Schema


class Schema(_Schema):

    def handle_error(self, exc, data, **kwargs):
        for key in exc.messages.keys():
            exc.messages[key] = exc.messages[key][0]
        raise exc
