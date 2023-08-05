import os
import pandas as pd
import psycopg2
from .customdecorators import trycatch

class DB():
  def __init__(self, conndata):
    self.setconn(conndata)

  def setconn(self, conndata):
    self.conn = psycopg2.connect(host=conndata['host'], database=conndata['database'], user=conndata['user'], password=conndata['password'])
    self.cur = self.conn.cursor()

  def query(self, *args):
    self.cur.execute(*args)

  def rollback(self):
    self.conn.rollback()

  @trycatch(exceptionfunc=rollback, log=True)
  def commit(self):
    self.conn.commit()

  def copy_expert(self, *args):
    self.cur.copy_expert(*args)

  def fetchall(self):
    return self.cur.fetchall()

  def printquery(self, *args):
    print(self.cur.mogrify(*args))

  def getcolumns(self, table):
    self.query(f"""
      SELECT column_name
      FROM information_schema.columns
      WHERE table_schema = 'public'
      AND table_name = '{table}';
    """)
    _columns = [e for i in self.fetchall() for e in i]
    return _columns

  def select(self, columns, table, query=None, orderby='id'):
    _query = f"select {','.join(columns)} from {table} order by {orderby}"
    if query != None:
      _query = query
    if columns[0] == '*': columns = self.getcolumns(table)
    self.query(_query)
    _tableDF = pd.DataFrame(self.fetchall(), columns=columns)
    _tableDF = _tableDF.convert_dtypes()
    return _tableDF
  
  def update(self, table, id, field, value):
    _query = f"""
      UPDATE {table}
      SET {field}='{value}'
      WHERE id={id}
      """
    self.query(_query)
    return _query

  def altersequence(self, table, start, commit=True):
    _query = f"""
      ALTER SEQUENCE {table}_id_seq
      RESTART with {start}
      """
    self.query(_query)
    if commit: self.commit()

  def truncate(self, table, commit=True):
    _query = f"""
      TRUNCATE TABLE {table} CASCADE;
    """
    self.query(_query)
    if commit: self.commit()

  def copy(self, tableName, tableDF, columns):
    self.delete(f"tmp_{tableName}.csv")

    tableDF.to_csv(f'tmp_{tableName}.csv', index=False, header=False)
    
    if columns[0] == '*': columns = self.getcolumns(tableName)
    columns.remove('id')

    copy_sql = f"""
          COPY {tableName}({','.join(columns)})
          FROM STDIN WITH CSV 
          DELIMITER as ','"""
          
    with open(f'tmp_{tableName}.csv', 'r') as f:
        self.copy_expert(copy_sql, f)
    self.commit()

    self.delete(f"tmp_{tableName}.csv")

  @trycatch(exceptionfunc=lambda:print("The file does not exist"))
  def delete(self, file):
    os.remove(file)

  def importfromdb(self, table, fromdb, todb):

    ## Get table from source database
    self.setconn(fromdb)

    _columns = self.getcolumns(table=table)
    print('get columns OK')
    _tableDF = self.select(columns=_columns, table=table, orderby='id')
    _tableDF.drop(columns=['id'], inplace=True)
    print('select table OK')

    self.close()

    ## Clean destination table and restart sequenceid
    self.setconn(todb)

    self.truncate(table=table, commit=False)
    print('get truncate OK')
    self.altersequence(table=table, start=1)
    print('get altersequence OK')

    ## Insert data from source to destination
    self.copy(tableName=table, tableDF=_tableDF, columns=_columns)
    print('get copy OK')

    self.close()

  def close(self):
    self.cur.close()
    self.conn.close()