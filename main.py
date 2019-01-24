"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py runmigrations
"""
from docopt import docopt

from alayatodo import (
    app,
    init_db,
    run_migrations
)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        init_db()
    elif args['runmigrations']:
        run_migrations()
    else:
        app.run(use_reloader=True)
