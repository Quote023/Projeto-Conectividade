import pyodbc 
from pyodbc import Row
from .config import ConfigFile


class DbConnection():
    def __init__(self, config: ConfigFile):
        self.config = config
        self.conn = pyodbc.connect(self.config.makeConnString())
        
    def makeCursor(self):
        return self.conn.cursor()

    def create_initial_tables(self):
        print("[create_initial_tables] Criando Tabelas no Banco de Dados")
        cursor = self.makeCursor()
        cursor\
        .execute("""-- sql
          CREATE TABLE IF NOT EXISTS clients(
            cpf VARCHAR(14) PRIMARY KEY,
            name VARCHAR(50)
          )
          """)\
        .execute("""-- sql
          CREATE TABLE IF NOT EXISTS ingredients(
              cod INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(50) NOT NULL,
              qty INT NOT NULL DEFAULT 0
          )
        """)\
        .execute("""-- sql
            CREATE TABLE IF NOT EXISTS items (
                cod INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                category VARCHAR(50)
            )
        """)\
        .execute("""-- sql
            CREATE TABLE IF NOT EXISTS items_ingredients (
                ing_cod INT NOT NULL,
                itm_cod INT NOT NULL,
                qty INT NOT NULL DEFAULT 1,
                FOREIGN KEY  fk_ing_itm_ing (ing_cod) REFERENCES ingredients(cod),
                FOREIGN KEY  fk_ing_itm_itm (itm_cod) REFERENCES items(cod),
                CONSTRAINT pk_ing_itm PRIMARY KEY (ing_cod,itm_cod)
            )
        """)\
        .execute("""-- sql
            CREATE TABLE IF NOT EXISTS orders (
                num INT AUTO_INCREMENT PRIMARY KEY ,
                cli_cpf VARCHAR(14) NOT NULL,
                FOREIGN KEY  fk_cli_order (cli_cpf) REFERENCES clients(cpf)
            );
        """)\
        .execute("""-- sql
            CREATE TABLE IF NOT EXISTS orders_items (
                ord_num INT NOT NULL,
                itm_cod INT NOT NULL,
                FOREIGN KEY fk_ord_itm_ord (ord_num) REFERENCES orders(num),
                FOREIGN KEY fk_ord_itm_itm (itm_cod) REFERENCES items(cod),
                CONSTRAINT pk_ord_itm PRIMARY KEY (ord_num,itm_cod)
            );
        """)
        cursor.commit()