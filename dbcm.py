import sqlite3

class DBCM:
  def __init__(self):
    self.conn = sqlite3.connect("weather.sqlite")
    self.cur = self.conn.cursor()
  def __enter__(self):
    return self.cur
  def __exit__(self, exc_type, exc_value, exc_trace):
    self.conn.commit()

    self.cur.close()
    self.conn.close()