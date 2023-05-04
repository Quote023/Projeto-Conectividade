import mysql.connector
from mysql.connector.types import RowType
from mysql.connector.connection import MySQLCursor
from .config import ConfigFile


class DbConnection():
    def __init__(self, config: ConfigFile):
        self.config = config
        self.conn = mysql.connector.connect(host=config.address,user=config.user, password=config.pwd, port=config.port, database=config.database)
        print(self.conn)

    def commit(self):
      self.conn.commit()

    def makeCursor(self) -> MySQLCursor:
        return self.conn.cursor()

    def create_initial_tables(self):
        print("[create_initial_tables] Criando Tabelas no Banco de Dados")
        cursor = self.makeCursor()
        print(cursor)
        cursor.execute("""-- sql
          CREATE TABLE IF NOT EXISTS clients(
            cpf VARCHAR(14) PRIMARY KEY,
            name VARCHAR(50)
          )
          """)
        cursor.execute("""-- sql
            CREATE TABLE IF NOT EXISTS items (
                name VARCHAR(50) PRIMARY KEY,
                category VARCHAR(50)
            )
        """)
        cursor.execute("""-- sql
            CREATE TABLE IF NOT EXISTS orders (
                num INT AUTO_INCREMENT PRIMARY KEY ,
                cli_cpf VARCHAR(14) NOT NULL,
                FOREIGN KEY  fk_cli_order (cli_cpf) REFERENCES clients(cpf)
            );
        """)
        cursor.execute("""-- sql
            CREATE TABLE IF NOT EXISTS orders_items (
                ord_num INT NOT NULL,
                itm_nam VARCHAR(50) NOT NULL,
                FOREIGN KEY fk_ord_itm_ord (ord_num) REFERENCES orders(num),
                FOREIGN KEY fk_ord_itm_itm (itm_nam) REFERENCES items(name),
                CONSTRAINT pk_ord_itm PRIMARY KEY (ord_num,itm_nam)
            );
        """)
        self.commit()
