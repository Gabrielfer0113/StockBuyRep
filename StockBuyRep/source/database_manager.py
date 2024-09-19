import sqlite3
from pathlib import Path
import datetime

CAMINHO_DATABASE = Path(__file__).parent.parent / 'configuration\database'

# DON'T EXECUTE ANYMORE - JUST TO VISUALIZE COLUMNS
def create_users_database():
    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\usuarios.db')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,

            user VARCHAR(25),
            password VARCHAR(10),
            area VARCHAR(10),
            
            config BOOL,
            themes BOOL,
            report_tools BOOL,
            receive_mp BOOL,
            delete_mp BOOL,
            register_mp BOOL,
            edit_mp BOOL,
            mp_filter BOOL,
            debug_tools BOOL,
            email_tools BOOL,
            historic BOOL
        )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\konemetal.sqlite3')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Konemetal_Main (
            id INTEGER PRIMARY KEY,

            Bitola VARCHAR(3),
            Material VARCHAR(2),
            Norma VARCHAR(3),
            Dimensao VARCHAR(10),
            Milimetros INTEGER,
            Fabricacao VARCHAR(15),

            Fornecedor VARCHAR(15),
            Valor Real,
            
            Kg_Solicitado INTEGER,
            Kg_Comprado INTEGER,

            Data_Entrega_Peca VARCHAR(10),
            Data_Solicitado VARCHAR(10),
            Data_Comprado VARCHAR(10),
            Data_Previsao VARCHAR(10),

            Ordem_Compra VARCHAR(7),

            Urgente BOOL,
            Comprado BOOL,

            Documento VARCHAR(7),
            Codigo_Peca VARCHAR(20),
            Solicitante VARCHAR(10)
        )
    '''
    cursor.execute(create_table_query)
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Konemetal_Historic (
            id INTEGER PRIMARY KEY,

            Bitola VARCHAR(3),
            Material VARCHAR(2),
            Norma VARCHAR(3),
            Dimensao VARCHAR(10),
            Fabricacao VARCHAR(15),

            Fornecedor VARCHAR(15),
            Valor Real,
            
            Kg_Solicitado INTEGER,
            Kg_Comprado INTEGER,
            Kg_Recebido INTEGER,

            Data_Entrega_Peca VARCHAR(10),
            Data_Solicitado VARCHAR(10),
            Data_Comprado VARCHAR(10),
            Data_Previsao VARCHAR(10),
            Data_Recebido VARCHAR(10),

            Ordem_Compra VARCHAR(7),
            Nota_Fiscal VARCHAR(10),

            Documento VARCHAR(7),
            Codigo_Peca VARCHAR(10),
            Solicitante VARCHAR(10)
        )
    '''
    cursor.execute(create_table_query)
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Konemetal_Extra_Itens (
            id INTEGER PRIMARY KEY,
            Descricao VARCHAR(15),
            Quantidade VARCHAR(15),
            Documento VARCHAR(15),
            Observacao VARCHAR(30)
        )
        '''
    cursor.execute(create_table_query)
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Konemetal_Portifolio (
            id INTEGER PRIMARY KEY,
            Cliente VARCHAR(15),
            Ordem_Interna VARCHAR(15),
            Pedido VARCHAR(15),
            Linha VARCHAR(30),
            Produto VARCHAR(30),
            Descricao VARCHAR(30),
            Quantidade INTEGER,
            Entregas VARCHAR(150),
            Data_recebido VARCHAR(30),
            Data_entrega VARCHAR(30), 
            Janela_entrega INTEGER
        )
        '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\davik.sqlite3')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Davik_Main (
            id INTEGER PRIMARY KEY,

            Bitola VARCHAR(3),
            Material VARCHAR(2),
            Norma VARCHAR(3),
            Dimensao VARCHAR(10),
            Milimetros INTEGER,
            Fabricacao VARCHAR(15),

            Fornecedor VARCHAR(15),
            Valor Real,

            Kg_Solicitado INTEGER,
            Kg_Comprado INTEGER,

            Data_Solicitado VARCHAR(10),
            Data_Comprado VARCHAR(10),
            Data_Previsao VARCHAR(10),

            Ordem_Compra VARCHAR(7),

            Urgente BOOL,
            Comprado BOOL,

            Solicitante VARCHAR(10)
        )
    '''
    cursor.execute(create_table_query)
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS Davik_Historic (
            id INTEGER PRIMARY KEY,

            Bitola VARCHAR(3),
            Material VARCHAR(2),
            Norma VARCHAR(3),
            Dimensao VARCHAR(10),
            Fabricacao VARCHAR(15),

            Fornecedor VARCHAR(15),
            Valor Real,

            Kg_Solicitado INTEGER,
            Kg_Comprado INTEGER,
            Kg_Recebido INTEGER,
            
            Data_Solicitado VARCHAR(10),
            Data_Comprado VARCHAR(10),
            Data_Previsao VARCHAR(10),
            Data_Recebido VARCHAR(10),

            Ordem_Compra VARCHAR(7),
            Nota_Fiscal VARCHAR(10),

            Solicitante VARCHAR(10)

        )
    '''
    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

def new_user(user, password, area, config, themes, report_tools, receive_mp,
delete_mp, register_mp,edit_mp,mp_filter,debug_tools,email_tools,historic):

    # Conectar ao arquivo SQLite
    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\usuarios.db')

    # Criar um cursor
    cursor = conn.cursor()

    # Executar um comando SQL para inserir valores em uma tabela
    cursor.execute(
        """
        INSERT INTO usuarios (
            user, password, area, config, themes, report_tools, receive_mp, delete_mp,
            register_mp, edit_mp, mp_filter, debug_tools, email_tools, historic 
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (user, password, area, config, themes, report_tools, receive_mp,
        delete_mp, register_mp,edit_mp,mp_filter,debug_tools,email_tools,historic)
    )

    # Lista de permissoes é:

    # CONFIGURAÇÕES
    # PERSONALIZAÇÃO
    # GERAR RELATORIOS
    # RECEBER MATERIAL
    # APAGAR MATERIAIS
    # REGISTRAR COMPRA
    # EDITAR INFORMAÇOES
    # FILTRO DE MATERIAIS
    # FERRAMENTAS DE DEBUG
    # FERRAMENTAS DE E-MAIL
    # HISTORICO DE MATERIAIS COMPRADOS

    # Commit para salvar as alterações no banco de dados
    conn.commit()

    # Fechar a conexão
    conn.close()

# generic read db
def read_database():

    # Conectar ao arquivo SQLite
    # conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\usuarios.db')
    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\konemetal.sqlite3')

    # Criar um cursor
    cursor = conn.cursor()

    # Executar uma consulta SQL para ler dados da tabela
    cursor.execute('''SELECT Valor, Data_Previsao FROM Konemetal_Historic''')

    # Recuperar os resultados da consulta
    resultados = cursor.fetchall()

    # Iterar pelos resultados
    print(resultados)

    # Fechar a conexão
    conn.close()

def fix_database():
    # Conecte-se ao seu banco de dados
    conn = sqlite3.connect(str(CAMINHO_DATABASE) + '\\konemetal.sqlite3')
    cursor = conn.cursor()

    # Seleciona todas as datas da tabela (exemplo: coluna 'data' na tabela 'seus_dados')
    cursor.execute("SELECT id, Data_Previsao, Valor FROM Konemetal_Historic")
    linhas = cursor.fetchall()

    # Para cada linha, converte e atualiza a data
    for linha in linhas:
        id = linha[0]
        data_antiga = linha[1]
        valor = linha[2]


        # if isinstance(valor, str):
        #     print('valor:',valor)
        #     try:
        #         valor = float(valor.replace(',','.'))
        #     except:
        #         print(valor)
        #         ...
        #         # valor = 13.07   
        #     cursor.execute("UPDATE Davik_Historic SET Valor = ? WHERE id = ?", (valor, id))

        try:
            # Converte a data de 'dd/mm/aaaa' para 'aaaa-mm-dd'
            data_nova = datetime.datetime.strptime(data_antiga, '%d/%m/%Y').strftime('%Y-%m-%d')
            
            # Atualiza a data no banco de dados
            cursor.execute("UPDATE Konemetal_Historic SET Data_Previsao = ? WHERE id = ?", (data_nova, id))
            

        except:
            print(data_antiga, data_nova)
            pass

    # Salva as mudanças e fecha a conexão
    conn.commit()
    conn.close()


if __name__=="__main__":

    # fix_database()
    read_database()
