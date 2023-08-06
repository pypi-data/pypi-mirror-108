from flask_marshmallow import Marshmallow

ma = Marshmallow()


class Schema(ma.Schema):

    def handle_error(self, exc, data, **kwargs):
        for key in exc.messages.keys():
            exc.messages[key] = exc.messages[key][0]
        raise exc
