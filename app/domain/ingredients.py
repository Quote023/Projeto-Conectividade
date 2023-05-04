class Ingredient():
  def __init__(self, cod: int,name: str, qty: int):
    self.cod = cod
    self.name = name
    self.qty = qty

  def validate(self):
    return True if self.qty >= 0 else False