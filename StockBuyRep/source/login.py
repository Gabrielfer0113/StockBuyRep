import PySimpleGUI as sg
from front_end import layout_login
import sqlite3
from pathlib import Path

USERS_DATABASE = str(Path(__file__).parent.parent / 'configuration'/'database'/'usuarios.db')

def import_users_data(user, password):
    conn = sqlite3.connect(USERS_DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        f'''
        SELECT * 
        FROM usuarios 
        WHERE 
            user=? AND password=?
        ''',
        (user.capitalize(), password)
        )
    dados_usuario = cursor.fetchall()
    conn.close()

    try:
        return {
            'id':dados_usuario[0][0],
            'user':dados_usuario[0][1],
            'password':dados_usuario[0][2],
            'area':dados_usuario[0][3],
            'config':dados_usuario[0][4],
            'themes':dados_usuario[0][5],
            'report_tools':dados_usuario[0][6],
            'receive_mp':dados_usuario[0][7],
            'delete_mp':dados_usuario[0][8],
            'register_mp':dados_usuario[0][9],
            'edit_mp':dados_usuario[0][10],
            'mp_filter':dados_usuario[0][11],
            'debug_tools':dados_usuario[0][12],
            'email_tools':dados_usuario[0][13],
            'historic':dados_usuario[0][14]
        }
    except:
        return False

def login():
    window_login = sg.Window('StockBuyRep', layout_login())
    while True:
        event, values = window_login.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif event == 'Confirmar':
            user_data = import_users_data(values['usuario'].lower(), values['senha'].lower())
            if user_data:
                window_login.close()
                return user_data
            else:
                sg.popup('usuario ou senha errada')

        elif event == 'Novo Cadastro':
            sg.popup('para novos cadastros falar com o leo.')
 
if __name__ == '__main__':
    # g = ['leo','bia','gessica','mauro']
    # print(g[0:2])
    ...