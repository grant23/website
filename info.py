import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='info.db'):
  new = not os.path.exists(path)
  db = sqlite3.connect(path)
  if new:
    c = db.cursor()
    c.execute( 'CREATE TABLE information( id INTEGER PRIMARY KEY,'
               'account TEXT, password TEXT, age INTEGER, introduction TEXT )' )
    add_information( db, 'aaa', 'aaa', '20', 'I am aaa.' )
    add_information( db, 'bbb', 'bbb', '25', 'I am bbb.' )
    db.commit()
  return db

def add_information( db, account, password, age, introduction ):
  db.cursor().execute( 'INSERT INTO information ( account, password, age, introduction )'
                       ' VALUES (?, ?, ?, ?)', ( account, password, age, introduction ) )

def get_information( db, account ):
  c = db.cursor()
  c.execute( 'SELECT * FROM information WHERE account = ?', ( account, ) )
  Row = namedtuple( 'Row', [tup[0] for tup in c.description] )
  return [Row(*row) for row in c.fetchall()]

def update_information( db, account, password = '', age = '', introduction = '' ):
  c = db.cursor()

  if password:
    c.execute( 'UPDATE information SET password = ?'
               ' WHERE account = ?', ( password, account ) )

  if age:
    c.execute( 'UPDATE information SET age = ?'
               ' WHERE account = ?', ( age, account ) )

  if introduction:
    c.execute( 'UPDATE information SET introduction = ?'
               ' WHERE account = ?', ( introduction, account ) )


def has_account( db, account, password ):
  c = db.cursor()
  c.execute( 'SELECT * FROM information WHERE account =?'
             ' AND password = ?', ( account, password ) )
  Row = namedtuple( 'Row', [tup[0] for tup in c.description] )
  result = [Row(*row) for row in c.fetchall()]

  if len( result ) == 0:
    return False
  else:
    return True

if __name__ == '__main__':
  db = open_database()
  print( get_information( db, 'aaa' ))
  pprint.pprint(get_information( db, 'aaa' ))
