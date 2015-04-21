import psycopg2
import constants

class Database(object):

    def __init__(self):

        self.cur = None
        self.conn = None

        print 'Initialize db connection: Start'
        self.conn = psycopg2.connect(
            host = constants.IP,
            database = constants.DB,
            user = constants.USER,
            password = constants.PASSWORD
        )
        self.cur = self.conn.cursor()
        print 'Initialize db connection: Done'