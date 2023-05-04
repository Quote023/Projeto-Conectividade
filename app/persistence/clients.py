from .db import DbConnection, Row
from domain.clients import Client

def makeClient(row: Row):
    return Client(row.cpf,row.name)

class ClientsSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,cpf: str, name: str = ""):
      print("inserting"  + cpf)
      self.cursor.execute(f"INSERT INTO clients (cpf,name) VALUES ('{cpf}', '{name}')").commit()
      return cpf

    def list_all(self)-> list[Client]:
        self.cursor.execute("SELECT * FROM clients")
        return list(map(makeClient,self.cursor.fetchall()))
    
    def list_by_pk(self, cpf: str) -> list[Client]:
        self.conn.execute("SELECT * FROM clients o WHERE o.cpf = %d", cpf)
        return list(map(makeClient,self.cursor.fetchall()))
    
    def delete(self, cpf: str):
      try:
        self.cursor.execute(f"DELETE FROM gdi.clients WHERE cpf = '{cpf}'").commit()
        return self.cursor.rowcount > 0
      except:
        return False
        
      