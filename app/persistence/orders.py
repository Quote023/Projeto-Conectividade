from domain.orders import Order
from domain.clients import Client
from .db import DbConnection

def makeOrder(row):
   return Order(row[0],Client(row[1],row[2]),[])

class OrdersSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,clientCpf: str, itemNames: list[str]):
      self.cursor.execute("INSERT INTO orders (cli_cpf) VALUES (%s)",[clientCpf])
      orderCod = self.cursor.lastrowid
      # Relacionamentos:
      orderItemsSql = "INSERT INTO orders_items (ord_num, itm_nam) VALUES "
      orderItemsParams = []
      for i,itmName in enumerate(itemNames):
        if (i > 0): orderItemsSql += ","
        orderItemsSql += "(%s,%s) "
        orderItemsParams.append(orderCod)
        orderItemsParams.append(itmName)

      self.cursor.execute(orderItemsSql,orderItemsParams)
      self.db.commit()
      return orderCod


    def list_all(self)-> list[Order]:
        self.cursor.execute("SELECT o.num,o.cli_cpf, c.name FROM orders o JOIN clients c ON c.cpf = o.cli_cpf")
        return map(makeOrder,self.cursor.fetchall())

    def get_by_pk(self, cod: int) -> list[Order]:
        self.cursor.execute("""-- sql
          SELECT o.num,o.cli_cpf, c.name
          FROM orders o 
          WHERE o.cod = %d 
          JOIN clients c ON o.cli_cpf = c.cpf
        """, cod)
        return list(map(makeOrder,self.cursor.fetchall()))
    
    def list_by_client(self, cpf: str)-> list[Order]:
        self.cursor.execute("SELECT o.num,o.cli_cpf, c.name FROM orders o JOIN clients c ON c.cpf = o.cli_cpf WHERE o.cli_cpf = %s", [cpf])
        return list(map(makeOrder,self.cursor.fetchall()))
    
    
        
      