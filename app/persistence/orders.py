from domain.orders import Order
from db import DbConnection,Row

def makeOrder(row: Row):
   return Order(row.num,None,[])

class OrdersSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,clientCpf: str, itemCods: list[int]):
      self.cursor.execute("INSERT INTO orders (cli_cpf) VALUES (?)",clientCpf)
      orderCod = self.cursor.fetchOne().cod
      # Relacionamentos:
      orderItemsSql = "INSERT INTO orders_items (ord_num, itm_cod) VALUES "
      orderItemsParams = []
      for cod in itemCods:
        orderItemsSql += "(?,?) "
        orderItemsParams.append(orderCod)
        orderItemsParams.append(cod)

      self.cursor.execute(orderItemsSql,tuple(orderItemsParams))
      self.cursor.commit()

    def list_all(self)-> list[Order]:
        self.cursor.execute("SELECT * FROM orders")
        return map(makeOrder,self.cursor.fetchall())
    def get_by_pk(self, cod: int) -> list[Order]:
        self.cursor.execute("""--sql
          SELECT * 
          FROM orders o 
          WHERE o.cod = %d 
          JOIN clients c ON o.cli_cpf = c.cpf
        """, cod)
        return list(map(makeOrder,self.cursor.fetchall()))
    def list_by_client(self, cpf: str)-> list[Order]:
        self.cursor.execute("SELECT * FROM orders o WHERE o.cli_cpf = %s", cpf)
        return list(map(makeOrder,self.cursor.fetchall()))
    
    def update(self, cod: int, clientCpf: str = None, itemCods: list[int] = None):
       pass
    
    def delete(self, cod: int):
       pass
    
        
      