from clients import Client
from items import Item

class Order():
    def __init__(self,num: int, client: Client | str, items: list[Item] | None):
        self.num = num
        self.client = client
        self.items = items

    def validate(self):
        return True