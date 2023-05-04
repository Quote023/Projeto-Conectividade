from getpass import getpass
import persistence.config as dbcfg
from persistence.db import DbConnection
from typing import Literal, Callable
import os
from persistence.clients import ClientsSqlRepo
from persistence.items import ItemsSqlRepo
from persistence.orders import OrdersSqlRepo

DATABASE_NAME = "gdi"

def ask_config():
  print("Arquivo de configuração não encontrado, por favor responda as seguintes perguntas.\n")
  addr = input("Qual o endereço do banco? [localhost] ") or "localhost"
  port = input("Qual a porta do banco? [3306] ") or "3306"
  user = input("Qual o seu usuário? [admin] ") or "admin"
  pwd = getpass("E a sua senha? [] ")
  cfg = dbcfg.ConfigFile(addr,port,user,pwd,DATABASE_NAME)
  dbcfg.save_config(cfg)
  return cfg


config = dbcfg.load_config()
if(config == None):
  config = ask_config()

dbConn = DbConnection(config)
dbConn.create_initial_tables()

State = Literal["MENU","CLIENTS","ITEMS","ORDERS"]

state: State = "MENU"

def update_state(val: State):
  global state
  state = val

def menu_screen(update_st: Callable[[State], None]):
  print("MENU PRINCIPAL:")
  print("1. Pedidos")
  print("2. Clientes:")
  print("3. Cardápio:")
  while True: 
    res = input("Opção: ")[0]
    match res: 
      case '1': update_st("ORDERS"); return
      case '2': update_st("CLIENTS"); return
      case '3': update_st("ITEMS"); return

def clients_screen(update_st: Callable[[State], None]):
  repo = ClientsSqlRepo(dbConn)
  print("CLIENTES:")
  print("1. Listar")
  print("2. Novo:")
  print("3. Apagar:")
  print("0. Voltar:")
  while True: 
    match input("Opção: ")[0]: 
      case '0': return update_st("MENU")
      case '1': 
        for i,x in enumerate(repo.list_all()):
          print(f"{i}.\t{x.name}\t{x.cpf}")
        input("pressione qualquer tecla p/ voltar")
        return
      case '2': 
        while True:
          nome = input("nome (ou \"cancelar\" p/ sair): ")
          if(nome == "cancelar"): return
          cpf = input("cpf (ou \"cancelar\" p/ sair): ")[:11]
          if(cpf == "cancelar"): return
          if(len(cpf) != 11 or not cpf.isnumeric()): 
            print("Cpf invalido, tente novamente.")
            continue
          print(f"Cliente {repo.create(cpf,nome)} criado com sucesso!")
      case '3': 
        while True:
          cpf = input("cpf (ou \"cancelar\" p/ sair): ")[:11]
          if(cpf == "cancelar"): return
          if(len(cpf) != 11 or not cpf.isnumeric()): 
            print("Cpf invalido, tente novamente.")
            continue
          print(f"Cliente {cpf} {'apagado com sucesso' if repo.delete(cpf) else 'não pode ser apagado'}!")


def items_screen(update_st: Callable[[State], None]):
  repo = ItemsSqlRepo(dbConn)
  print("Cardápio:")
  print("1. Listar")
  print("2. Novo Prato:")
  print("3. Apagar:")
  print("4. Modificar Categoria:")
  print("5. Vendas:")
  print("0. Voltar:")
  while True: 
    match input("Opção: ")[0]: 
      case '0': return update_st("MENU")
      case '1': 
        for i,x in enumerate(repo.list_all()):
          print(f"{i}.\t{x.name}\t{x.category}")
        input("pressione qualquer tecla p/ voltar")
        return
      case '2': 
        while True:
          nome = input("nome (ou \"cancelar\" p/ sair): ")
          if(nome == "cancelar"): return
          cat = input("categoria (ou \"cancelar\" p/ sair): ")
          if(cat == "cancelar"): return
          print(f"Prato {repo.create(nome,cat)} criado com sucesso!")
      case '3': 
        while True:
          nome = input("nome (ou \"cancelar\" p/ sair): ")
          if(nome == "cancelar"): return
          print(f"Prato {nome} {'apagado com sucesso' if repo.delete(nome) else 'não pode ser apagado'}!")
      case '4': 
        while True:
          nome = input("nome (ou \"cancelar\" p/ sair): ")
          if(nome == "cancelar"): return
          cat = input("nova categoria (ou \"cancelar\" p/ sair): ")
          if(cat == "cancelar"): return
          print(f"Prato {nome} {'atualizado com sucesso' if repo.update_category(nome,cat) else 'não pode ser atualizado'}!")
      case '5': 
        for i,x in enumerate(repo.list_with_sales()):
          print(f"{i}.\t{x[0]}\t{x[1]}")
        input("pressione qualquer tecla p/ voltar")
        return


def orders_screen(update_st: Callable[[State], None]):
  repo = OrdersSqlRepo(dbConn)
  repo_itm = ItemsSqlRepo(dbConn)

  print("Pedidos:")
  print("1. Listar")
  print("2. Novo Pedido:")
  print("3. Detalhes")
  print("4. Listar por Cliente")
  print("0. Voltar:")
  while True: 
    match input("Opção: ")[0]: 
      case '0': return update_st("MENU")
      case '1': 
        print(f"#. num\tcliente")
        for i,x in enumerate(repo.list_all()):
          print(f"{i}.\t{x.num}\t{x.client.name}")
        input("pressione qualquer tecla p/ voltar")
        return
      case '2': 
          cpf_cli = input("cpf do cliente (ou \"cancelar\" p/ sair): ")
          if(cpf_cli == "cancelar"): return
          items = []
          while(True):
            item = input(f"item nº {len(items)} (0 p/ terminar | \"cancelar\" p/ sair): ")
            if(item == "0"): break
            if(item == "cancelar"): return
            items.append(item)
          print(f"Pedido {repo.create(cpf_cli,items)} criado com sucesso!")
          input("pressione qualquer tecla p/ voltar")
          return
      case '3': 
          num = input("num pedido (ou \"cancelar\" p/ sair): ")[:11]
          if(num == "cancelar"): return
          print("items no pedido:")
          print(f"#. nome\tcategoria")
          for i,x in enumerate(repo_itm.get_by_order(num)):
            print(f"{i}. {x.name}\t{x.category}")
          input("pressione qualquer tecla p/ voltar")
          return
      case '4': 
        cpf = input("cpf cliente (ou \"cancelar\" p/ sair): ")[:11]
        print(f"#. num\tcliente")
        for i,x in enumerate(repo.list_by_client(cpf)):
          print(f"{i}. {x.num}\t{x.client.name}")
        input("pressione qualquer tecla p/ voltar")
        return


while True:
  os.system('clear')
  match state:
    case "MENU": 
      menu_screen(update_state)
    case "CLIENTS":
      clients_screen(update_state)
    case "ITEMS":
      items_screen(update_state)
    case "ORDERS":
      orders_screen(update_state)
