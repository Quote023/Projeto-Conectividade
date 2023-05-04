import json

DEFAULT_PATH = "./config.json"
DRIVER = "/usr/local/mysql-connector-odbc-8.0.33-macos13-arm64/lib/libmyodbc8a.so"
class ConfigFile():
  def __init__(self,address: str,port: str,user: str,pwd: str,database: str):
    self.address = address
    self.port = port
    self.user = user
    self.pwd = pwd
    self.database = database

  def makeConnString(self):
    return f"DRIVER={{{DRIVER}}};Server={self.address};Port={self.port};Uid={self.user};Pwd={self.pwd};DATABASE={self.database}"


def load_config(path: str = DEFAULT_PATH) -> ConfigFile | None:
  # try:
    file = open(path,"r")
    return json.load(file, object_hook = lambda x: ConfigFile(x["address"],x["port"],x["user"],x["pwd"],x["database"]))
  # except:
    # return None

def save_config(config: ConfigFile, path: str = DEFAULT_PATH):
  file = open(path,"w")
  json.dump(config.__dict__,file)