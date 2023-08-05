
class _MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(_MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class DBHelper(object):

    def __init__(self):
        self.db = None

    def init_app(self, app, db):
        self.db = db

    def flush(self):
        return _Flush(db=self.db)

    def commit(self):
        return _Commit(db=self.db)


class _Flush(metaclass=_MetaSingleton):
    def __init__(self, db):
        self._db = db

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.session.flush()


class _Commit(metaclass=_MetaSingleton):
    def __init__(self, db):
        self._db = db

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.session.commit()