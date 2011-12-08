import os, argparse

from geoscript.workspace import Directory, PostGIS
from geoscript.layer import Layer

def parse_args():
  """
  Parse the command line arguments
  """

  root_dir = os.path.dirname(os.path.realpath(__file__))
  parser = argparse.ArgumentParser()

  parser.add_argument('db')
  parser.add_argument('table')
  parser.add_argument('--host', default='localhost', help='defaults to "localhost"')
  parser.add_argument('--port', type=int, default=5432, help='defaults to "5432"')
  parser.add_argument('--schema', default='public', help='defaults to "public"')
  parser.add_argument('--user', default='postgres', help='defaults to "postgres')
  parser.add_argument('--passwd', default='', help='defaults to ""')
  parser.add_argument('--shp_dir', default="%s/../data" % (root_dir, ), help='defaults to "censustools/data"')

  return parser.parse_args()

if __name__ == '__main__':
  # Parse the command line arguments
  args = parse_args()

  # Create a workspace for all of the shp files in the directory
  shps = Directory(args.shp_dir)

  # Create a workspace for our PostGIS database
  pg = PostGIS(args.db, host=args.host, port=args.port, schema=args.schema, user=args.user, passwd=args.passwd)
  
  # Define our table variable
  pg_table = None

  for name in shps:
    # Init the table/layer using the the schema from the shp file on the first pass
    if pg_table == None : pg_table = pg.create(name=args.table, schema=shps[name].schema)

    # Add the features from the shp file into the database
    print "Adding features from [%s] to database [%s] on table [%s].[%s]" % (name, args.db, args.schema, args.table)
    pg_table.add(shps[name])