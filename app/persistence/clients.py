from .db import DbConnection,RowType
from domain.clients import Client

def makeClient(row: RowType):
    return Client(row[0],row[1])

class ClientsSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,cpf: str, name: str = ""):
      print("inserting"  + cpf)
      self.cursor.execute("INSERT INTO clients (cpf,name) VALUES (%s, %s)",(cpf,name))
      self.db.commit()
      return cpf

    def list_all(self)-> list[Client]:
        self.cursor.execute("SELECT cpf,name FROM clients")
        return list(map(makeClient,self.cursor.fetchall()))
    
    def list_by_pk(self, cpf: str) -> list[Client]:
        self.conn.execute("SELECT * FROM clients c WHERE c.cpf = %s", [cpf])
        return list(map(makeClient,self.cursor.fetchall()))
    
    def delete(self, cpf: str):
      self.cursor.execute("DELETE FROM clients WHERE cpf = %s",[cpf])
      self.db.commit()
      return self.cursor.rowcount > 0
        
      