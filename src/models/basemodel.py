import rethinkdb as r
class BaseModel(r.RqlQuery):
    def init(self, conn):
        try:
            yield r.table_create(cls.__name__).run(conn)
        except:
            print "tables already exist"

    def table()
        r.table(cls.__name__)
