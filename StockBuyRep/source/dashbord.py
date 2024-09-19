from pathlib import Path
import numpy as np
import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import pandas as pd

from front_end import dashbord_davik_kone
from users import BuyerUser

# Criar a interface gráfica com o PySimpleGUI


def create_dashbord(area):
    graph_data = dict()

    if area == 'davik':
        full_path = Path(__file__).parent.parent / 'configuration\\davik_report.json'
    elif area == 'konemetal':
        full_path = Path(__file__).parent.parent / 'configuration\\konemetal_report.json'
    elif area == 'view':
        compras = BuyerUser('ambas', 'leo', '123')

        full_path = False
    else:
        raise ValueError('Area typed wrong or not existent')


    if full_path:
        with open(full_path, 'r') as file:
            data = json.load(file)
        dados = pd.DataFrame(data['report'])
    else:
        dados = compras.makeGeneralReport('view_graph') # esta passando relatorio de forma errada, deve ser em dicionario e com esse cabeçario
        dados['fabricacao'] = [0 for item in range(len(dados['index']))]
        dados['milimetros'] = [0 for item in range(len(dados['index']))]
        del(dados['index'])
        dados = pd.DataFrame(dados)
    # print(dados)

    # Grafico top 5
    mp_agrop_quilos = dados[['bitola','material','norma','dimensao','milimetros','fabricacao','quilos']].groupby(['bitola','material','norma','dimensao','fabricacao']).sum()

    mp_agrop_quilos.reset_index(inplace=True)
    materiais_dict = mp_agrop_quilos.to_dict(orient='list')

    materiais_dict = pd.DataFrame(mp_agrop_quilos)
    materiais_dict = materiais_dict.sort_values(by='quilos', ascending=False )

    top5 = materiais_dict.head(5)[['bitola', 'material', 'norma', 'dimensao', 'fabricacao', 'quilos']]

    top5_names = top5['bitola'] + top5['material'] + top5['norma'] + top5['dimensao']
    top5_values = list(top5['quilos'])

    graph_data['top5_names'] = top5_names
    graph_data['top5_values'] = top5_values


    # Grafico normas mais solicitadas
    mp_agrop_normas = pd.DataFrame(mp_agrop_quilos[['norma','quilos']].groupby('norma').sum().reset_index())

    norma_names = list(mp_agrop_normas['norma'])
    norma_values = list(mp_agrop_normas['quilos'])

    graph_data['norma_names'] = norma_names
    graph_data['norma_values'] = norma_values


    # Grafico bitolas
    mp_agrop_bitola = pd.DataFrame(mp_agrop_quilos[['bitola','quilos']].groupby('bitola').sum().reset_index())

    bitola_names = list(mp_agrop_bitola['bitola'])
    bitola_values = list(mp_agrop_bitola['quilos'])

    graph_data['bitola_names'] = bitola_names
    graph_data['bitola_values'] = bitola_values


    # Grafico tipos de fabricação
    mp_agrop_fabricacao  = pd.DataFrame(mp_agrop_quilos[['fabricacao','quilos']].groupby('fabricacao').sum().reset_index())
    
    fabricacao_names = list(mp_agrop_fabricacao['fabricacao'])
    fabricacao_values = list(mp_agrop_fabricacao['quilos'])

    graph_data['fabricacao_names'] = fabricacao_names
    graph_data['fabricacao_values'] = fabricacao_values

    print(graph_data)
    return graph_data

if __name__ == '__main__':
    gg = create_dashbord('konemetal')
    print(gg)