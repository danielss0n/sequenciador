import json
import os

class DanielssonDB():
    def __init__(self, db_path) -> None:
        self.path = db_path
        if not os.path.exists(self.path):
            with open(self.path, 'w') as file:
                json.dump({}, file, indent=4)
        
        self.no_name_table = "_default"
        
    def data(self) -> dict:
        with open(self.path, 'r') as file:
            return json.load(file)

    def all(self, table_name: str) -> list:
        with open(self.path, 'r') as file:
            data = json.load(file)
            data_table = data[table_name]
            return list(data_table.values())
        

    def create_table(self, name: str) -> None:
        if name.strip() == "":
            name = self.no_name_table

        with open(self.path, 'r') as file:
            data = json.load(file)

        if name not in data:
            data[name] = {}

            with open(self.path, 'w') as file:
                json.dump(data, file, indent=4)


    def truncate(self, table_name: str) -> None:
        with open(self.path, 'r') as file:
            data_base = json.load(file)

        if table_name in data_base:
            data_base[table_name] = {}

            with open(self.path, 'w') as file:
                json.dump(data_base, file, indent=4)


    def insert(self, table_name: str, item: object) -> None:
        with open(self.path, 'r') as file:
            data = json.load(file)

        if table_name.strip() == "":
            table_name = self.no_name_table

        keys = list(map(int, data[table_name].keys())) 
        next_key = str(max(keys) + 1) if keys else "1"
        data[table_name][next_key] = item

        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)


    def insert_multiple(self, table_name: str, items = list) -> None:
        with open(self.path, 'r') as file:
            data = json.load(file)

        if table_name.strip() == "":
            table_name = self.no_name_table
        
        if table_name not in data:
            data[table_name] = {}

        for item in items:
            next_key = str(len(data[table_name]) + 1)
            data[table_name][next_key] = item

        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)


    def update(self, table_name: str, where: list, update: dict) -> None:
        with open(self.path, 'r') as file:
            data_base = json.load(file)

        if table_name in data_base:
            table_data = data_base[table_name]    
            for item_key, item_value in table_data.items():
                match = True
                for key, value in where.items():
                    if item_value.get(key) != value:
                        match = False
                        break
                if match:
                    item_value.update(update)
                    break
            with open(self.path, 'w') as file:
                json.dump(data_base, file, indent=4)


    def remove(self, table_name: str, where: dict):
        with open(self.path, 'r') as file:
            data_base = json.load(file)

        if table_name in data_base:
            table_data = data_base[table_name]

            keys_to_delete = []

            for item_key, item_value in table_data.items():
                match = True 
                for key, value in where.items():
                    if item_value.get(key) != value:
                        match = False
                        break
                if match:
                    keys_to_delete.append(item_key)

            for key in keys_to_delete:
                del table_data[key]

            with open(self.path, 'w') as file:
                json.dump(data_base, file, indent=4)

database = DanielssonDB('Q:/GROUPS/BR_SC_JGS_WM_DEPARTAMENTO_CALDEIRARIA/DEPARTAMENTO DE CALDEIRARIA/02 - DOCUMENTOS/16 - RELATORIOS BI/Códigos Python/Sequenciador/app/db/tabela.json')

# add_data = [
#     {
#         "peca": "Peça aleatória 1",
#         "tinta": "Tinta qualquer 1",
#         "em_progresso": False
#     },
#     {
#         "peca": "Mais uma peça aleatória 2",
#         "tinta": "Mais uma tinta qualquer 2",
#         "em_progresso": False
#     },
#         {
#         "peca": "Peça aleatória 4444",
#         "tinta": "Tinta qualquer 1213",
#         "em_progresso": False
#     }
# ]
# my_db.insert_multiple("sequencia_aprovada", items=add_data)
# add_data = {
#         "peca": "Peça aleatória 1",
#         "tinta": "Tinta qualquer 2",
#         "em_progresso": False
#     }

# my_db.create_table("Minha tabela2233")
# my_db.remove("Minha tabela2", where={"em_progresso": False})
# my_db.insert_multiple("Minha tabela2", add_data)
# print(my_db.all("Minha tabela2"))
# my_db.truncate("Minha tabela2")
# my_db.update("Minha tabela2", {"tinta": "Tinta qualquer 1"}, add_data)