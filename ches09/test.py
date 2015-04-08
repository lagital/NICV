import sys
try: from pyPgSQL import PgSQL as db
except:
	try: import pgdb as db
	except:
		print "Neither pyPgSQL nor pgdb is installed. Stopping dead."
		print "Please read the instructions on 'http://www.dpacontest.org/documentation.php'."
		sys.exit(1)
	else: db_name= 'pgdb';  # Choosing "pgdb" as a back-up
else: db_name= 'pyPgSQL'; # Choosing "pyPgSQL.PgSQL"
from parse_binary import parse_binary

__host = "127.0.0.1"
__user = "postgres"
__pass = "postgres"
__db = "scapack"
__conn = None
__curs = None

__conn  = db.connect(
    user     = __user,
    password = __pass,
    host     = __host,
    database = __db
)

__curs  = __conn.cursor()

cmd = "SELECT data FROM trace2 WHERE id = 53"
__curs.execute(cmd)

one = __curs.fetchone()
raw_data = one
res = parse_binary(raw_data)
print len(res)