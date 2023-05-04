from .db import DbConnection,RowType
from domain.items import Item



def makeItem(row: RowType):
   return Item(row[0], row[1])

class ItemsSqlRepo():
    def __init__(self,db: DbConnection):
      self.db = db
      self.cursor = db.makeCursor()

    def create(self,name: str, category: str):
      self.cursor.execute("INSERT INTO items (name,category) VALUES (%s, %s)",[name,category])
      self.db.commit()
      return name

    def list_all(self)-> list[Item]:
        self.cursor.execute("SELECT name,category FROM items")
        return list(map(makeItem,self.cursor.fetchall()))
    
    def list_by_pk(self, name: str) -> list[Item]:
        self.cursor.execute("SELECT name,category FROM items i WHERE i.name = %s", [name])
        return list(map(makeItem,self.cursor.fetchall()))
    
    def list_by_category(self, category: str)-> list[Item]:
        self.cursor.execute("SELECT name,category FROM items i WHERE i.category = %s", [category])
        return list(map(makeItem,self.cursor.fetchall()))
    
    def get_by_order(self, ord_num: int) -> list[Item]:
      self.cursor.execute("""-- sql
        SELECT i.name,i.category
        FROM orders_items oi
        JOIN items i ON i.name = oi.itm_nam
        WHERE oi.ord_num = %s 
      """, [ord_num])
      return list(map(makeItem,self.cursor.fetchall()))
    
    def list_with_sales(self):
      self.cursor.execute("""-- sql
        SELECT i.name, count(i.name)
        FROM orders_items oi
        JOIN items i ON i.name = oi.itm_nam
        GROUP BY i.name
      """)
      return self.cursor.fetchall()
    
    def update_category(self, name: str, new_cat: str):
        self.cursor.execute("UPDATE items SET category = %s WHERE name = %s", (new_cat,name))
        self.db.commit()
        return self.cursor.rowcount > 0
    
    def delete(self, name: str):
      self.cursor.execute("DELETE FROM items WHERE name = %s", [name])
      self.db.commit()
      return self.cursor.rowcount > 0
    
        
      