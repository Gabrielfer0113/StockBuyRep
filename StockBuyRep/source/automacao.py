import pyautogui as pg
import pyperclip
import json
from time import sleep
from datetime import datetime


def sendEmailAuto(relatorio_kone, relatorio_davik, report):
        pg.alert('A criação de e-mails vai começar nao mexa em nada.')
        pg.PAUSE = 1
        pg.press('win')
        pg.typewrite('outlook')
        pg.press('enter')
        sleep(5)

        #email relatorio beatriz
        pg.hotkey('ctrl','n')
        pg.typewrite(r"beatriz@konemetal.com.br;")
        pg.press('tab')
        pg.press('tab')
        pg.press('tab')
        assunto = f'Relatório semanal ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        texto_email = (f'Bom dia.\nSegue abaixo o relatórios matéria prima solicitada\n\nKONEMETAL\n{relatorio_kone}\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        sleep(3)
        
        #Bom dia relatorio gessica
        pg.hotkey('ctrl','n')
        pg.typewrite(r"'Géssica - DAVIK' <vendas2@davik.com.br>")
        pg.press('tab')
        pg.press('tab') 
        pg.press('tab')
        assunto = f'Relatório semanal ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        texto_email = (f'Bom dia.\nSegue abaixo os relatórios de matéria prima solicitada\n\nDAVIK\n{relatorio_davik}\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        sleep(3)               
        #email relatorio unificado
        pg.hotkey('ctrl','n')
        pg.typewrite(r"mauro@konemetal.com.br;")
        pg.press('tab')
        pg.press('tab')
        pg.press('tab')
        assunto = f'Relatório semanal ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        texto_email = (f'Bom dia.\nSegue abaixo a soma dos relatórios de matéria prima solicitada pela Konemetal e DaviK\n\n{report}\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        pg.alert('emails enviados...')

def documentarComprasAuto(materiais_comprados):
        def gerarRelatorio(report_file):
            report = ''
            for i in range(0, len(report_file['indice'])):
                report_file['valor_kg'][i] = (report_file['valor_kg'][i]).replace(',','.')
                report += ("{:^13}|{:^7}|{:^12}|{:^9}|{:^8}|{:^13}\n".format(report_file['fornecedor'][i], report_file['oc'][i], report_file['material'][i], report_file['quantidade'][i], float(report_file['valor_kg'][i]), report_file['data'][i]))
            return report


        with open(materiais_comprados, 'r') as file:
            data = json.load(file)

        ### formatar forma do relatorio, esta printando no email em linha

        # Encontrar os índices dos elementos diferentes de 'KONEMETAL' na lista 'para'
        indices_para_remover = [i for i, value in enumerate(data["para"]) if value != "KONEMETAL"]
        # Criar um novo dicionário com as listas simplificadas, excluindo os elementos nos índices encontrados
        konemetal_comprado = {key: [value for i, value in enumerate(data[key]) if i not in indices_para_remover] for key in data}
        relatorio_konemetal = gerarRelatorio(konemetal_comprado)
        soma_valor_konemetal = 0
        soma_kg_konemetal = 0
        for i in range(len(konemetal_comprado['indice'])):
            valor = float(konemetal_comprado['valor_kg'][i].replace(",",'.'))
            quantidade = int(konemetal_comprado['quantidade'][i])

            soma_kg_konemetal += quantidade
            soma_valor_konemetal += (valor*quantidade)


        # Encontrar os índices dos elementos diferentes de 'KONEMETAL' na lista 'para'
        indices_para_remover = [i for i, value in enumerate(data["para"]) if value != "DAVIK"]
        # Criar um novo dicionário com as listas simplificadas, excluindo os elementos nos índices encontrados
        davik_comprado = {key: [value for i, value in enumerate(data[key]) if i not in indices_para_remover] for key in data}
        relatorio_davik = gerarRelatorio(davik_comprado)
        soma_valor_davik = 0
        soma_kg_davik = 0
        for i in range(len(davik_comprado['indice'])):
            valor = float(davik_comprado['valor_kg'][i].replace(",",'.'))
            quantidade = int(davik_comprado['quantidade'][i])

            soma_kg_davik += quantidade
            soma_valor_davik += (valor*quantidade)

        # Encontrar os índices dos elementos diferentes de 'KONEMETAL' na lista 'para'
        indices_para_remover = [i for i, value in enumerate(data["para"]) if value != "AMBAS"]
        # Criar um novo dicionário com as listas simplificadas, excluindo os elementos nos índices encontrados
        ambas_comprado = {key: [value for i, value in enumerate(data[key]) if i not in indices_para_remover] for key in data}
        relatorio_ambas = gerarRelatorio(ambas_comprado)
        soma_valor_ambas = 0
        soma_kg_ambas = 0
        for i in range(len(ambas_comprado['indice'])):
            valor = float(ambas_comprado['valor_kg'][i].replace(",",'.'))
            quantidade = int(ambas_comprado['quantidade'][i])

            soma_kg_ambas += quantidade
            soma_valor_ambas += (valor*quantidade)


        relatorio_total = gerarRelatorio(data)
        soma_valor_total = 0
        soma_kg_total = 0
        for i in range(len(data['indice'])):
            valor = float(data['valor_kg'][i].replace(",",'.'))
            quantidade = int(data['quantidade'][i])

            soma_kg_total += quantidade
            soma_valor_total += (valor*quantidade)

        pg.alert('A documentação das compras por e-mails vai começar\n NÃO MEXA NO PC...')
        pg.PAUSE = 0.7
        pg.press('win')
        pg.typewrite('outlook')
        pg.press('enter')
        sleep(7)

        #email relatorio beatriz
        pg.hotkey('ctrl','n')
        pg.typewrite(r"beatriz@konemetal.com.br;")
        pg.press('tab')
        pg.press('tab')
        pg.press('tab')
        assunto = f'Relatório semanal de materiais comprados de materiais comprados ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        texto_email = (f'Bom dia.\nSegue abaixo o relatórios matéria prima comprada para a Konemetal\n\nKONEMETAL\n{relatorio_konemetal}\n\nMATERIAL COMPRADO EM JUNTO COM A DAVIK\n{relatorio_ambas}\n\nNesta semana foi comprado {soma_kg_konemetal+soma_kg_ambas}kgs\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        sleep(3)
        
        #Bom dia relatorio gessica
        pg.hotkey('ctrl','n')
        pg.typewrite(r"'Géssica - DAVIK' <vendas2@davik.com.br>")
        pg.press('tab')
        pg.press('tab') 
        pg.press('tab')
        assunto = f'Relatório semanal de materiais comprados ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        texto_email = (f'Bom dia.\nSegue abaixo o relatórios matéria prima comprada para a DaviK\n\nDAVIK\n{relatorio_davik}\n\nMATERIAL COMPRADO JUNTO COM A KONEMETAL\n{relatorio_ambas}\n\nNesta semana foi comprado {soma_kg_davik+soma_kg_ambas}kgs\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        sleep(3)      

        #email relatorio unificado
        pg.hotkey('ctrl','n')
        pg.typewrite(r"mauro@konemetal.com.br;")
        pg.press('tab')
        pg.press('tab')
        pg.press('tab')
        assunto = f'Relatório semanal de materiais comprados ({str(datetime.now().date())[2:]})'
        pyperclip.copy(assunto)
        pg.hotkey('ctrl', 'v')
        pg.press('tab')
        sleep(3)
        soma_valor_total = str(soma_valor_total)
        soma_valor_total = soma_valor_total.replace('.',',')
        texto_email = (f'Bom dia.\nSegue abaixo o relatórios matéria prima comprada para Konemetal e DaviK\nRELATORIO\n{relatorio_total}\n\nNesta semana foi comprado {soma_kg_total}kgs e foi gasto uma valor total de R${soma_valor_total}\n\nRelatorio gerado automaticamente...')
        pyperclip.copy(texto_email.upper())
        pg.hotkey('ctrl', 'v')
        pg.hotkey('ctrl', 'enter')
        pg.alert('emails enviados...')
