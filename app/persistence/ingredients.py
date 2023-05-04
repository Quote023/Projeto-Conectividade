from db import DbConnection, Row
from domain.ingredients import Ingredient

def makeIngredient(row: Row):
   return Ingredient(row.cod,row.name,row.qty)

class IngredientsSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,name: str, qty: int = 0):
      self.cursor.execute("INSERT INTO ingredients (name,qty) VALUES (%s)",(name,qty))
      ingredientCod = self.cursor.fetchOne().cod
      self.cursor.commit()
      return ingredientCod

    def list_all(self) -> list[Ingredient]:
        self.cursor.execute("SELECT * FROM ingredients")
        return list(map(makeIngredient,self.cursor.fetchall()))

    def list_by_pk(self, cod: int) -> list[Ingredient]:
        self.cursor.execute("SELECT * FROM ingredients o WHERE o.cod = %d", cod)
        return list(map(makeIngredient,self.cursor.fetchall()))
    def list_by_name(self, name: str) -> list[Ingredient]:
        self.cursor.execute("SELECT * FROM ingredients o WHERE o.name = %s", name)
        return list(map(makeIngredient,self.cursor.fetchall()))
    def list_by_qty_ordered(self, desc: bool = False)-> list[Ingredient]:
        self.cursor.execute(f"""--sql
          SELECT * 
          FROM ingredients i
          ORDER BY i.qty {"DESC" if desc else "ASC"}
        """)
        return list(map(makeIngredient,self.cursor.fetchall()))
        
    def update(self, cod: int, clientCpf: str = None, itemCods: list[int] = None):
       pass
    
    def delete(self, cod: int):
       pass
    
        
      