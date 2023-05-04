from db import DbConnection,Row
from domain.items import Item

Qty = int
IngredientCod = int
ItemIngredients = (IngredientCod,Qty)


def makeItem(row: Row):
   return Item(row.cod, row.category,row.name, [])

class ItemsSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,name: str, category: str, itemIngredients: list[ItemIngredients]):
      self.cursor.execute("INSERT INTO items (name,category) VALUES (%s, %s)",(name,category))
      itemCod = self.cursor.fetchOne().cod
      #Relacionamentos
      itemItemsSql = "INSERT INTO items_ingredients (itm_cod,ing_cod,qty) VALUES "
      itemItemsParams = []
      for cod,qty in itemIngredients:
        itemItemsSql += "(%s,%s,%s) "
        itemItemsParams.append(itemCod)
        itemItemsParams.append(cod)
        itemItemsParams.append(qty)

      self.cursor.execute(itemItemsSql,tuple(itemItemsParams))
      self.cursor.commit()

    def list_all(self)-> list[Item]:
        self.cursor.execute("SELECT * FROM items")
        return list(map(makeItem,self.cursor.fetchall()))
    def list_by_pk(self, cod: int) -> list[Item]:
        self.cursor.execute("SELECT * FROM items o WHERE o.cod = %d", cod)
        return list(map(makeItem,self.cursor.fetchall()))
    def list_by_client(self, cpf: str)-> list[Item]:
        self.cursor.execute("SELECT * FROM items o WHERE o.cli_cpf = %s", cpf)
        return list(map(makeItem,self.cursor.fetchall()))
    
    def update(self, cod: int, clientCpf: str = None, itemCods: list[int] = None):
       pass
    
    def delete(self, cod: int):
       pass
    
        
      