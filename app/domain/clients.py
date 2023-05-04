
class Client():
  def __init__(self, cpf: str, name: str = ""):
    self.cpf = cpf
    self.name = name

  def validate(self):
    return True if len(self.cpf) == 11 and self.cpf.isnumeric() else False
    
