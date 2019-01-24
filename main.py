"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py runmigrations
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app
from alayatodo import db
from alayatodo.models import User


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


def add_default_users():
    for user, password in [('user{}'.format(i),
                            'user{}'.format(i)) for i in range(1, 4)]:
        new_user = User(user, password)
        db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        add_default_users()
        print("AlayaTodo: Database initialized.")
    elif args['runmigrations']:
        _run_sql('resources/1to2.sql')
    else:
        app.run(use_reloader=True)
