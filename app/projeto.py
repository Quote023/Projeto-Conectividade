from getpass import getpass
import persistence.config as dbcfg
from persistence.db import DbConnection
from typing import Literal, Callable
import os
from persistence.clients import ClientsSqlRepo

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

State = Literal["MENU","CLIENTS","INGREDIENTS","ITEMS","ORDERS"]

state: State = "MENU"

def update_state(val: State):
  global state
  state = val

def menu_screen(update_st: Callable[[State], None]):
  print("MENU PRINCIPAL:")
  print("1. Pedidos")
  print("2. Clientes:")
  print("3. Items:")
  print("4. Ingredientes:")
  while True: 
    res = input("Opção: ")[0]
    match res: 
      case '1': update_st("ORDERS"); return
      case '2': update_st("CLIENTS"); return
      case '3': update_st("ITEMS"); return
      case '4': update_st("INGREDIENTS"); return

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


        


def ingredients_screen(update_st: Callable[[State], None]):
  update_st("MENU")

def items_screen(update_st: Callable[[State], None]):
  update_st("MENU")


def orders_screen(update_st: Callable[[State], None]):
  update_st("MENU")


while True:
  os.system('clear')
  match state:
    case "MENU": 
      menu_screen(update_state)
    case "CLIENTS":
      clients_screen(update_state)
    case "INGREDIENTS":
      ingredients_screen(update_state)
    case "ITEMS":
      items_screen(update_state)
    case "ORDERS":
      orders_screen(update_state)
