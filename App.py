from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_socketio import SocketIO
from flask_cors import CORS
from danielssondb import database
import win32com.client as win32
import pythoncom
import requests
from bs4 import BeautifulSoup

CODIGO_URL_CHEFE = "3h0qhwj9hdf42w0fh93ua3rfd23re2eg6vsd54ih08h49fwf"

class OperadorController():
    def __init__(self) -> None:
        app.add_url_rule('/operador', view_func=self.pagina_operador_sequencia, methods=['GET'])
        app.add_url_rule('/operador/peca-finalizar', view_func=self.finalizar, methods=['POST'])
        app.add_url_rule('/operador/peca-em-progresso', view_func=self.em_progresso, methods=['POST'])

    def pagina_operador_sequencia(self):
        return OperadorService.operador_sequencia()

    def finalizar(self):
        return OperadorService.operador_finalizar()
    
    def em_progresso(self):
        return OperadorService.operador_em_progresso()

class OperadorService():
    @staticmethod
    def operador_sequencia() -> None:
        
        current_data = database.all("sequencia_aprovada")
        return render_template('/operador.html', current_data=current_data)

    @staticmethod
    def operador_finalizar() -> None:

        req_data = request.get_json() 
        database.remove("sequencia_aprovada", where={"peca": req_data["peca"]})
        database.remove("sequencia_aguardando", where={"peca": req_data["peca"]})

        socket.update_all_tables()

        return {"message": "Peça finalizada com sucesso."}, 200

    @staticmethod
    def operador_em_progresso():

        req_data = request.get_json() 
        peca_value = req_data.get('peca') 

        database.update("sequencia_aguardando", {"peca": peca_value}, {"em_progresso": True})
        database.update("sequencia_aprovada", {"peca": peca_value}, {"em_progresso": True})

        socket.update_all_tables()

        return {'message': 'Atualização realizada com sucesso!', 'peca': peca_value}, 200

class PreparadorController():
    def __init__(self) -> None:
        app.add_url_rule('/preparador', view_func=self.pagina_preparador_sequencia, methods=['GET'])
        app.add_url_rule('/preparador/registrar-peca', view_func=self.pagina_registrar_peca, methods=['GET'])
        app.add_url_rule('/preparador/registrar-peca', view_func=self.registrar_peca, methods=['POST'])
        app.add_url_rule('/preparador/mover', view_func=self.mover, methods=['POST'])
        app.add_url_rule('/preparador/enviar-movimentacao', view_func=self.enviar_movimentacao, methods=['POST'])

    def pagina_preparador_sequencia(self) -> None:
        return PreparadorService.pagina_preparador_sequencia()
    
    def pagina_registrar_peca(self) -> None:
        return PreparadorService.pagina_registrar_peca()
    
    def registrar_peca(self) -> None:
        return PreparadorService.registrar_peca()
    
    def mover(self) -> None:
        return PreparadorService.mover()
    
    def enviar_movimentacao(self) -> None:
        return PreparadorService.enviar_movimentacao()
    
class PreparadorService():
    @staticmethod
    def pagina_preparador_sequencia() -> None:
    
        sequencia_aguardando = database.all("sequencia_aguardando")
        socket.update_sequencias()

        return render_template('/preparador.html', current_data=sequencia_aguardando)

    @staticmethod
    def pagina_registrar_peca() -> None:

        return render_template('/preparador_registrar.html')

    @staticmethod
    def registrar_peca() -> None:
        
        req_data = request.get_json() 
        print(req_data)
        
        if (len(req_data['peca']) > 25):
            return {'message': 'NÃO PODE MAIS DE 25 CARACTERES NO NOME DA PEÇA', 'dados': req_data}, 400
        
        if (len(req_data['peca']) == 0):
            return {'message': '?????????? CADE O NOME DA PEÇA OXI', 'dados': req_data}, 400
        
        database.insert("sequencia_aguardando", req_data)

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        usuario = Utils.pegar_login_ip(ip)

        database.truncate("usuario_aguardando_aprovacao")
        database.insert("usuario_aguardando_aprovacao", usuario)
        
        socket.update_all_tables()
        socket.update_preparador_modificou()
        socket.update_classificacao()

        return redirect(url_for('outra_funcao'))

    
    @staticmethod
    def enviar_movimentacao() -> None:
        
        req_data = request.get_json() 

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        usuario = Utils.pegar_login_ip(ip)

        elementos_tabelas = OutLook.pegar_body_html(f'http://10.1.39.20:5000/{CODIGO_URL_CHEFE}/chefe')
        corpo_html = OutLook.construir_corpo_html_para_chefe(elementos_tabelas)

        chefe = "danielsson"
        OutLook.mandar_email(
            f"{chefe}@weg.net", 
            "NOVA MODIFICAÇÃO NO SEQUENCIAMENTO DE PINTURA", 
            corpo_html
        )

        database.truncate("usuario_aguardando_aprovacao")
        database.insert("usuario_aguardando_aprovacao", usuario)

        database.truncate("sequencia_aguardando")
        database.insert_multiple("sequencia_aguardando", req_data)

        socket.update_all_tables()
        socket.update_classificacao()

        return {'message': 'Dados recebidos com sucesso!', 'dados': req_data}, 200

    @staticmethod
    def mover() -> None:
        req_data = request.get_json() 
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        usuario = Utils.pegar_login_ip(ip)

        database.truncate("usuario_aguardando_aprovacao")
        database.insert("usuario_aguardando_aprovacao", usuario)

        database.truncate("sequencia_aguardando")
        database.insert_multiple("sequencia_aguardando", req_data)

        socket.update_all_tables()
        socket.update_classificacao()

        return {'message': 'Dados recebidos com sucesso!', 'dados': req_data}, 200

class ChefeController():
    def __init__(self) -> None:
        app.add_url_rule(f'/{CODIGO_URL_CHEFE}/chefe', view_func=self.pagina_aprovacao, methods=['GET'])
        app.add_url_rule(f'/chefe/aprovacao', view_func=self.aprovar, methods=['POST'])
        app.add_url_rule(f'/chefe/reprovacao', view_func=self.reprovar, methods=['POST'])

    def pagina_aprovacao(self) -> None:
        return ChefeService.pagina_aprovacao()
    
    def aprovar(self) -> None:
        return ChefeService.aprovar()
    
    def reprovar(self) -> None:
        return ChefeService.reprovar()

class ChefeService():
    @staticmethod
    def pagina_aprovacao():
        sequencia_aprovada = database.all("sequencia_aprovada")
        
        dados_bd = database.data()
        new_data_classified = Utils.classificar_sequencias(dados_bd)
        new_data_classified = [item for item in new_data_classified.values()]

        usuario_que_modificou = database.all("usuario_aguardando_aprovacao")[0]
        usuario_que_modificou = usuario_que_modificou.upper()

        socket.update_all_tables()
        socket.update_classificacao()
   
        return render_template('/chefe.html', usuario=usuario_que_modificou, 
                                new_data=new_data_classified, current_data=sequencia_aprovada)
   
    @staticmethod
    def aprovar():
        status = "APROVADA"
        usuario_que_modificou = database.all("usuario_aguardando_aprovacao")[0]
        elementos_tabelas = OutLook.pegar_body_html(f'http://10.1.39.20:5000/{CODIGO_URL_CHEFE}/chefe')
        corpo_html = OutLook.construir_corpo_html(elementos_tabelas, "APROVADA")

        OutLook.mandar_email(
            f"{usuario_que_modificou}@weg.net", 
            f"SOLICITAÇÃO DE SEQUENCIAMENTO {status}", 
            corpo_html
        )
    
        data = database.all("sequencia_aguardando")
        database.truncate("sequencia_aprovada")
        database.insert_multiple("sequencia_aprovada", data)

        socket.update_all_tables()
        socket.update_classificacao()
        return {'message': 'Solicitação de modificação aprovada!'}, 200
    
    @staticmethod
    def reprovar():
        
        status = "REPROVADA"
        usuario_que_modificou = database.all("usuario_aguardando_aprovacao")[0]
        elementos_tabelas = OutLook.pegar_body_html(f'http://10.1.39.20:5000/{CODIGO_URL_CHEFE}/chefe')
        corpo_html = OutLook.construir_corpo_html(elementos_tabelas, "REPROVADA")

        OutLook.mandar_email(
            f"{usuario_que_modificou}@weg.net", 
            f"SOLICITAÇÃO DE SEQUENCIAMENTO {status}", 
            corpo_html
        )

        sequencia_aprovada = database.all("sequencia_aprovada")
        database.truncate("sequencia_aguardando")
        database.insert_multiple("sequencia_aguardando", sequencia_aprovada)

        socket.update_all_tables()
        socket.update_classificacao()
        
        return {'message': 'Solicitação de modificação reprovada'}, 200


class OutLook():
    @staticmethod
    def mandar_email(destinatario, assunto, corpo):
        try:
            pythoncom.CoInitialize()

            outlook = win32.Dispatch('outlook.application')

            email = outlook.CreateItem(0)
            email.To = destinatario
            email.Subject = assunto
            email.HTMLBody = corpo
            email.Send()
            print(f'Email enviado para {destinatario}')
        except Exception as e:
            print(f'Ocorreu um erro ao enviar o email: {e}')
        finally:
            pythoncom.CoUninitialize()


    def pegar_body_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status() 
        
            soup = BeautifulSoup(response.text, 'html.parser')
            container = soup.find(class_='tables')
            
            if container:
                return str(container)
            else:
                return "<p>Elemento com a classe 'container' não encontrado.</p>"
        
        except requests.exceptions.RequestException as e:
            print(f'Ocorreu um erro ao obter o HTML: {e}')
            return "<p>Erro ao obter a página.</p>"

    def construir_corpo_html(container, status):
        corpo_html = f"""
            <html>
            <body>
                <h1>SUA SOLICITAÇÃO DE MODIFICAÇÃO FOI {status}</h1>
                {container}
            </body>
            </html>
            """

        return corpo_html

    def construir_corpo_html_para_chefe(container):
        link_pagina_chefe = f'http://10.1.39.20:5000/{CODIGO_URL_CHEFE}/chefe'
        print("criou html email")
        corpo_html = f"""
            <html>
            <body>
                <h1>NOVA SOLICITAÇÃO DE MODIFICAÇÃO PARA APROVAR</h1>
                {container}
                <a href="{link_pagina_chefe}" target="_blank">Clique aqui para acessar o link</a>.
            </body>
            </html>
            """
        return corpo_html
    

class Utils():
    @staticmethod
    def mover_pecas_em_progresso(sequencia):
        em_progresso = []
        aguardando = []
        for key, item in sequencia.items():
            if item['em_progresso']:
                em_progresso.append((key, item))
            else:
                aguardando.append((key, item))
        
        nova_sequencia = {key: item for key, item in em_progresso}
        nova_sequencia.update({key: item for key, item in aguardando})
        return nova_sequencia
    
    def classificar_sequencias(data):
        aguardando = data["sequencia_aguardando"]
        aprovada = data["sequencia_aprovada"]
        novas_posicoes = {}

        for posicao, item in aprovada.items():
            peca = item['peca']
            novas_posicoes[peca] = int(posicao) 

        for posicao, item in aguardando.items():
            peca = item['peca']
            nova_posicao = novas_posicoes.get(peca)
            if nova_posicao is not None:
                casas_subiu = nova_posicao - int(posicao)
                item['casas_movidas'] = casas_subiu 
            else:
                item['casas_movidas'] = 99
        return aguardando
    
    def sequencia_igual():
        aguardando = database.all("sequencia_aguardando")
        aprovada = database.all("sequencia_aprovada")
        return aguardando == aprovada
            
    def pegar_login_ip(ip):
        match(ip):
            case "10.1.39.20":
                return "danielsson"
            case "10.1.72.78":
                return "poglia"
            case "10.1.39.88":
                return "henriqueme"
            case "10.1.36.41":
                return "ffelype"
        return "(desconhecido)"


class SocketUpdate():
    def __init__(self) -> None:
        pass

    def update_all_tables(self) -> None:
        self.update_sequencia_aprovada()
        self.update_sequencia_aguardando()
        self.update_preparador_modificou()

    def update_sequencias(self) -> None:
        self.update_sequencia_aprovada()
        self.update_sequencia_aguardando()

    def update_classificacao(self) -> None:
        dados_bd = database.data()
        new_data_classified = Utils.classificar_sequencias(dados_bd)
        new_data_classified = [item for item in new_data_classified.values()]

        socketio.emit('update_classificacao', new_data_classified)

    def update_sequencia_aprovada(self) -> None:
        sequencia_aprovada = database.all("sequencia_aprovada")
        socketio.emit('update_sequencia_aprovada', sequencia_aprovada)
    
    def update_sequencia_aguardando(self) -> None:
        dados_bd = database.data()
        new_data_classified = Utils.classificar_sequencias(dados_bd)
        new_data_classified = [item for item in new_data_classified.values()]
        socketio.emit('update_sequencia_aguardando', new_data_classified)

    def update_preparador_modificou(self) -> None:
        usuario_que_modificou = database.all("usuario_aguardando_aprovacao")[0]
        socketio.emit('usuario_que_modificou', usuario_que_modificou)
        
app = Flask(__name__, template_folder='templates') 
CORS(app)

socketio = SocketIO(app)
socket = SocketUpdate()

operador_controller = OperadorController()
preparador_controller = PreparadorController()
chefe_controller = ChefeController()


@socketio.on('carregar_classificacao')
def carregar_classificacao():
    dados_bd = database.data()
    new_data_classified = Utils.classificar_sequencias(dados_bd)
    new_data_classified = [item for item in new_data_classified.values()]
    socketio.emit('update_sequencia_aguardando', new_data_classified)

socketio.run(app, host='0.0.0.0', port=5000)