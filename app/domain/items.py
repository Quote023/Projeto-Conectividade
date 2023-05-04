from ingredients import Ingredient

qty = int


class Item():
  def __init__(self,cod: int,category: str,name: str,ingredients: list[tuple[Ingredient, qty]]):
    self.cod = cod
    self.category = category
    self.name = name
    self.ingredients = ingredients

  def validate(self):
    return True if (all([qty >= 0 for _,qty in self.ingredients])) else False
