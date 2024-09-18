# Internal libraries
import os
from pathlib import Path
from datetime import datetime
import json
from random import choice

# My libraries
from front_end import register_buy_info
from front_end import filterpopup, dashbord, layout_viewer, edit_multiples_lines
from front_end import layout_material_comprado, create_layout_historic, editpopup
from front_end import item_infos, receive_mp_info, set_setings, register_standards
from front_end import layout_login, layout_davik, layout_konemetal, supplier_config
from front_end import add_pedido
from users import DavikUser, KonemetalUser, BuyerUser
from login import login

# External libraries
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Constants
MATERIAL_STANDARDS = Path(__file__).parent.parent / "configuration\\material_standards.json"
SUPPLIERS = Path(__file__).parent.parent / "configuration\\suppliers.json"
PREFERENCES = Path(__file__).parent.parent / "configuration\\preferences.json"
LOG_FILE = Path(__file__).parent.parent / "configuration\\log.log"


# Catch data to create object
def userSettings(name:str):
    with open(PREFERENCES, 'r') as file:
        preferences = json.load(file)

    with open(MATERIAL_STANDARDS, 'r', encoding='utf-8') as file:
        materiais_info = json.load(file)
	
    gauge_list = list()
    market_gauge_list = list()
    material_list = list()
    market_material_list = list()
    standards_list = list()
    market_standards_list = list()
    forging_weight_list = materiais_info['Peso_forjados']

    for key, item in materiais_info['Bitola'].items():
        gauge_list.append(key),
        market_gauge_list.append(item)

    for key, item in materiais_info['Material'].items():
        material_list.append(key)
        market_material_list.append(item)

    for key, item in materiais_info['Norma'].items():
        standards_list.append(key)
        market_standards_list.append(item)

    return {
    'theme':preferences[name.capitalize()]['Theme'],
    'button_color':preferences[name.capitalize()]['button_color'],
    'pressed_button_color':preferences[name.capitalize()]['pressed_button_color'],
    'second_color':preferences[name.capitalize()]['second_color'],
    'text_color':preferences[name.capitalize()]['text_color'],
    'font':preferences[name.capitalize()]['font'],
    'font_size':preferences[name.capitalize()]['font_size'],
    'gauge_list':gauge_list,
    'market_gauge_list':market_gauge_list,
    'material_list':material_list,
    'market_material_list':market_material_list,
    'standards_list':standards_list,
    'market_standards_list':market_standards_list,
    'forging_weight_list':forging_weight_list
    }
USUARIO = login()
settings = userSettings(USUARIO['user'])

# Create User (object)
if USUARIO['area'] == 'DaviK':
    user = DavikUser(    
        name=USUARIO['user'],
        password=USUARIO['password'],
        area=USUARIO['area'],
        user_pc=os.getenv("COMPUTERNAME"),

        config=USUARIO['config'],
        themes=USUARIO['themes'],
        report_tools=USUARIO['report_tools'],
        receive_mp=USUARIO['receive_mp'],
        delete_mp=USUARIO['delete_mp'],
        register_mp=USUARIO['register_mp'],
        edit_mp=USUARIO['edit_mp'],
        mp_filter=USUARIO['mp_filter'],
        debug_tools=USUARIO['debug_tools'],
        email_tools=USUARIO['email_tools'],
        historic=USUARIO['historic'],

        theme_name=settings['theme'],
        button_color=settings['button_color'],
        pressed_button_color=settings['pressed_button_color'],
        second_color=settings['second_color'],
        text_color=settings['text_color'],
        font=settings['font'],
        font_size=settings['font_size'],
    
        gauge_list=settings['gauge_list'],
        market_gauge_list=settings['market_gauge_list'],
        material_list=settings['material_list'],
        market_material_list=settings['market_material_list'],
        standards_list=settings['standards_list'],
        market_standards_list=settings['market_standards_list'],
        forging_weight_list=settings['forging_weight_list']
    )

    user.last_report = user.updateReport()
    sg.theme(user.theme_name)

    main_window = sg.Window(
        'DaviK', 
        layout_davik(
            report_data=user.last_report,
            color_list=user.coloringRows(
                user.last_report,
                user.text_color,
                user.second_color
            ),
            name=user.name,
            user_pc=user.PC,
            gauge_list=user.gauge_list,
            material_list=user.material_list,
            standards_list=user.standards_list,
            button_color=user.button_color,
            pressed_button_color=user.pressed_button_color,
            text_color=user.text_color,
            second_color=user.second_color
        ),
        resizable=True)
elif USUARIO['area'] == 'Konemetal':
    user = KonemetalUser(    
        name=USUARIO['user'],
        password=USUARIO['password'],
        area=USUARIO['area'],
        user_pc=os.getenv("COMPUTERNAME"),

        config=USUARIO['config'],
        themes=USUARIO['themes'],
        report_tools=USUARIO['report_tools'],
        receive_mp=USUARIO['receive_mp'],
        delete_mp=USUARIO['delete_mp'],
        register_mp=USUARIO['register_mp'],
        edit_mp=USUARIO['edit_mp'],
        mp_filter=USUARIO['mp_filter'],
        debug_tools=USUARIO['debug_tools'],
        email_tools=USUARIO['email_tools'],
        historic=USUARIO['historic'],

        theme_name=settings['theme'],
        button_color=settings['button_color'],
        pressed_button_color=settings['pressed_button_color'],
        second_color=settings['second_color'],
        text_color=settings['text_color'],
        font=settings['font'],
        font_size=settings['font_size'],
    
        gauge_list=settings['gauge_list'],
        market_gauge_list=settings['market_gauge_list'],
        material_list=settings['material_list'],
        market_material_list=settings['market_material_list'],
        standards_list=settings['standards_list'],
        market_standards_list=settings['market_standards_list'],
        forging_weight_list=settings['forging_weight_list']
    )
    sg.theme(user.theme_name)
    user.last_report = user.updateReport()
    main_window = sg.Window(
       'Konemetal',    
        layout_konemetal(
            report_data=user.last_report, 
            extra_mp_report_data=user.updateExtraMp(),
            color_list=user.coloringRows(
                user.last_report,
                user.text_color, 
                user.second_color
            ), 
            name=user.name, 
            user_pc=user.PC, 
            gauge_list=user.gauge_list, 
            material_list=user.material_list, 
            standards_list=user.standards_list, 
            today_date=datetime.now().date().strftime('%d/%m/%Y'), 
            button_color=user.button_color, 
            pressed_button_color=user.pressed_button_color, 
            text_color=user.text_color, 
            second_color=user.second_color
        ), 
        resizable=True
    )
elif USUARIO['area'] == 'Compras':
    user = BuyerUser(    
        name=USUARIO['user'],
        password=USUARIO['password'],
        area=USUARIO['area'],
        user_pc=os.getenv("COMPUTERNAME"),

        config=USUARIO['config'],
        themes=USUARIO['themes'],
        report_tools=USUARIO['report_tools'],
        receive_mp=USUARIO['receive_mp'],
        delete_mp=USUARIO['delete_mp'],
        register_mp=USUARIO['register_mp'],
        edit_mp=USUARIO['edit_mp'],
        mp_filter=USUARIO['mp_filter'],
        debug_tools=USUARIO['debug_tools'],
        email_tools=USUARIO['email_tools'],
        historic=USUARIO['historic'],

        theme_name=settings['theme'],
        button_color=settings['button_color'],
        pressed_button_color=settings['pressed_button_color'],
        second_color=settings['second_color'],
        text_color=settings['text_color'],
        font=settings['font'],
        font_size=settings['font_size'],
    
        gauge_list=settings['gauge_list'],
        market_gauge_list=settings['market_gauge_list'],
        material_list=settings['material_list'],
        market_material_list=settings['market_material_list'],
        standards_list=settings['standards_list'],
        market_standards_list=settings['market_standards_list'],
        forging_weight_list=settings['forging_weight_list']
    )
    user.last_report = user.updateReport()
    sg.theme(user.theme_name) # 5A5D40 "Jacarta"
    main_window = sg.Window(
        'Materiais comprados', 
        layout_material_comprado(
            user.last_report, 
            user.coloringRows(  # passar em forma de dicionario
                user.last_report, 
                user.text_color, 
                user.second_color
            )
        ), 
        resizable=True)

# Program Loop
while True:
    event, values = main_window.read()

    # App structure
    if event == sg.WIN_CLOSED:
        break
    elif event[:7] == 'area_jl':
        main_window['area_jl'].update(
            visible=not main_window['area_jl'].visible
        )
        main_window['area_jl'+'-BUTTON-'].update(
            main_window['area_jl'].metadata[0] \
                if main_window['area_jl'].visible \
                else main_window['area_jl'].metadata[1]
        )
    elif event[:8] =='area_tee':
        main_window['area_tee'].update(
            visible=not main_window['area_tee'].visible
        )
        main_window['area_tee'+'-BUTTON-'].update(
            main_window['area_tee'].metadata[0] \
                if main_window['area_tee'].visible \
                else main_window['area_tee'].metadata[1]
        )
    elif event[:11] =='area_flange':
        main_window['area_flange'].update(
            visible=not main_window['area_flange'].visible
        )
        main_window['area_flange'+'-BUTTON-'].update(
            main_window['area_flange'].metadata[0] \
                if main_window['area_flange'].visible \
                else main_window['area_flange'].metadata[1]
        )
    elif event[:7] =='area_cz':
        main_window['area_cz'].update(
            visible=not main_window['area_cz'].visible
        )
        main_window['area_cz'+'-BUTTON-'].update(
            main_window['area_cz'].metadata[0] \
                if main_window['area_cz'].visible \
                else main_window['area_cz'].metadata[1]
        )             
    
    # Menu / Buttons
    elif event == 'Historico':
        if user.historic_acess:
            user.last_report_historic = user.updateHistoric(
                column=user.last_filter, 
                order=user.last_filter_order
            )
            win_historic = sg.Window(
                f'Historico de recebidos {user.area}',
                create_layout_historic(
                    report=user.last_report_historic,
                    area=user.area, 
                    button_color=user.button_color, 
                    text_color=user.text_color, 
                    second_color=user.second_color
                ),
                keep_on_top=True
            )
            while True:
                event, values = win_historic.read()
                # print(event, values) FL 90G -16 X -20 TERM. MAN COD.61
                if event == 'Sair' or event == sg.WIN_CLOSED:
                    win_historic.close()
                    break
                elif '+CLICKED+' in event:
                    if isinstance(event[2][0], int):
                        if event[2][0] == -1:
                            try:
                                _order = user.last_filter_order
                                if event[2][1] == 0:
                                    selected_column = 'Data_Recebido'
                                elif event[2][1] == 1:
                                    selected_column = 'Fornecedor'
                                elif event[2][1] == 2:
                                    selected_column = 'Ordem_Compra'
                                elif event[2][1] == 3:
                                    selected_column = 'Bitola'
                                elif event[2][1] == 4:
                                    selected_column = 'Kg_Recebido'
                                elif event[2][1] == 5:
                                    selected_column = 'Valor'

                                if selected_column == user.last_filter and \
                                user.last_filter_order == _order:
                                    if _order == 'ASC':
                                        _order = 'DESC'
                                    else:
                                        _order = 'ASC'
                                
                                user.last_filter = selected_column
                                user.last_filter_order = _order

                                user.last_report_historic = user.updateHistoric(
                                    user.last_filter, 
                                    user.last_filter_order
                                )

                                win_historic['-tabela_historico-'].update(
                                    values=user.last_report_historic)

                                user.log_success(f"Relatório ordenado por {user.last_filter} com sucesso", user.debug_status)
                            except Exception as erro:
                                user.log_error(f'Falha ao filtrar relatório - ({erro})',user.debug_status)
                                sg.popup('Não foi possível ordenar relatório do historico')
                elif event == 'Informações':
                    try:
                        itens = user.last_report_historic[values['-tabela_historico-'][0]]
                        item_solicitante = itens[0]
                        item_id = itens[-1]
                        
                        material = user.catchValues(line=item_id, historic=True, requester=item_solicitante)
                        try:
                            _dimensao = f'{int(material["Dimensao"])}mm'
                        except:
                            dim = material["Dimensao"].rstrip('"')
                            _dimensao = f'{dim}"'
                        material["Dimensao"] = _dimensao

                        wind_infos = sg.Window(
                            f'{material["Bitola"]}{material["Material"]}{material["Norma"]} {material["Dimensao"]} {material["Fabricacao"]}',
                            item_infos(
                                material=user.marketStandard(material), 
                                area=user.area, 
                                comprado=True
                            ),
                            keep_on_top=True
                        )
                        event_inf, values_inf = wind_infos.read()

                        if event_inf or event:
                            wind_infos.close()

                    except Exception as erro:
                        user.log_error(f'Nao foi possivel filtrar o relatorio ({erro})', user.debug_status)
                        sg.Popup('Erro ao filtrar o relatorio')
                elif event == 'Filtrar':
                    try:
                        if values['fornecedor_hist']:
                            _filter_by = 'Fornecedor'
                        elif values['oc_hist']:
                            _filter_by = 'Ordem_Compra'
                        elif values['bitola_hist']:
                            _filter_by = 'Bitola'
                        elif values['dimensao_hist']:
                            _filter_by = 'Dimensao'
                        elif values['norma_hist']:
                            _filter_by = 'Norma'

                        user.last_report_historic =  user.filterReport(
                            filter_by=_filter_by, 
                            filter_key=values['chave_filtro'].upper(), 
                            historic=True
                        )
                        win_historic['-tabela_historico-'].update(
                            values=user.last_report_historic)

                        user.log_success('Relatorio filtrado com sucesso', user.debug_status)
                    except Exception as erro:
                        user.log_error(f'Falha ao filtrar relatorio - ({erro})', user.debug_status)
                        sg.Popup('Erro ao filtrar relatorio')
                elif event == 'Remover filtro':
                    try:
                        user.last_report_historic = user.updateHistoric(
                            column=user.last_filter, 
                            order=user.last_filter_order
                        )
                        win_historic['-tabela_historico-'].update(
                            values=user.last_report_historic)

                        user.log_success('Filtro removido com sucesso', user.debug_status)

                    except Exception as erro:
                        user.log_error(f'Falha ao remover filtro ({erro})',user.debug_status)
                        sg.Popup('Erro ao remover filtro')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'Exibir Calculadora':
        main_window['-frame_calculadora-'].update(visible=True)
        main_window['-menu-'].update(
            [
                ['Arquivo', ['Salvar BackUp', 'Gerar Relatorio em Excel']],
                ['Editar', ['Preferencias', ['Aparência', 'Configurações',['Bitola','Norma','Material','Fornecedor']]]],
                ['Ferramentas', ['Historico','Dashbord','Calculadora',['Desabilitar Calculadora']]],
                ['Ajuda', ['Visualizar Historico de Logs', 'Console Debug']]
            ]
        )
    elif event == 'Desabilitar Calculadora':
        main_window['-frame_calculadora-'].update(visible=False)
        main_window['-menu-'].update(
            [
                ['Arquivo', ['Salvar BackUp', 'Gerar Relatorio em Excel']],
                ['Editar', ['Preferencias', ['Aparência', 'Configurações',['Bitola','Norma','Material','Fornecedor']]]],
                ['Ferramentas', ['Historico','Dashbord','Calculadora',['Exibir Calculadora']]],
                ['Ajuda', ['Visualizar Historico de Logs', 'Console Debug']]
            ]
        )
    elif event == 'Aparência':
        if user.themes_acess:
            win_config = sg.Window(
                'Configurações de estrutura',
                set_setings(
                    button_color=user.button_color, 
                    pressed_button_color=user.pressed_button_color, 
                    second_color=user.second_color, 
                    text_color=user.text_color, 
                    font=user.font, 
                    font_size=user.font_size
                ),
                keep_on_top=True
            )

            _theme = user.theme_name
            _button = user.button_color
            _button_press = user.pressed_button_color
            _second = user.second_color
            _text = user.text_color
            _font=user.font,
            _font_size=user.font_size

            while True:
                event, values = win_config.read()
                # print(event, '\n',values)

                if event == sg.WIN_CLOSED or event == "Sair":
                    win_config.close()
                    break
                elif event == '-combo_themes-':
                    try:
                        if values['-combo_themes-'] == "Tema Cinza":
                            win_config['-combo_themes-'].update("Tema Cinza") # DarkGrey7
                            win_config['color_change_button'].update("#4c4c61", button_color="#4c4c61")
                            win_config['color_change_button_pressed'].update("lightblue", button_color="lightblue")
                            win_config['color_change_second'].update("Lightslategray", button_color='Lightslategray')
                            win_config['color_change_text'].update("black", button_color='gray')

                            _theme = 'DarkGrey7'
                            _button = "#4c4c61"
                            _button_press = "lightblue"
                            _second = "Lightslategray"
                            _text = "black"
                            
                        elif values['-combo_themes-'] == "Tema Verde":
                            win_config['-combo_themes-'].update("Tema Verde") # Green
                            win_config['color_change_button'].update("#517239", button_color="#517239")
                            win_config['color_change_button_pressed'].update("#8dc28d", button_color="#8dc28d")
                            win_config['color_change_second'].update("#96d669", button_color="#96d669")
                            win_config['color_change_text'].update('black', button_color='black')

                            _theme = 'Green'
                            _button = "#517239"
                            _button_press = "#8dc28d"
                            _second = "#96d669"
                            _text = "black"
                            
                        elif values['-combo_themes-'] == "Tema Azul":
                            win_config['-combo_themes-'].update("Tema Azul") # 'DarkBlue3'
                            win_config['color_change_button'].update("#4d4d94", button_color="#4d4d94")
                            win_config['color_change_button_pressed'].update("lightblue", button_color="lightblue")
                            win_config['color_change_second'].update("Lightslategray", button_color='Lightslategray')
                            win_config['color_change_text'].update('white', button_color=('black','white'))

                            _theme = 'DarkBlue3'
                            _button = "#4d4d94"
                            _button_press = "lightblue"
                            _second = "Lightslategray"
                            _text = "white"
                            
                        elif values['-combo_themes-'] == "Tema Claro":
                            win_config['-combo_themes-'].update("Tema Claro") # DefaultNoMoreNagging
                            win_config['color_change_button'].update("#3a5370", button_color="#3a5370")
                            win_config['color_change_button_pressed'].update("Blue", button_color="Blue")
                            win_config['color_change_second'].update("Lightslategray", button_color='Lightslategray')
                            win_config['color_change_text'].update('black', button_color=('white','black'))
                            
                            _theme = 'DefaultNoMoreNagging'
                            _button = "#3a5370"
                            _button_press = "Blue"
                            _second = "Lightslategray"
                            _text = "black"
                            
                        elif values['-combo_themes-'] == "Tema Escuro":
                            win_config['-combo_themes-'].update("Tema Escuro") # 'Dark'
                            win_config['color_change_button'].update("#004F00", button_color="#004F00")
                            win_config['color_change_button_pressed'].update("#324f32", button_color="#324f32")
                            win_config['color_change_second'].update("#505750", button_color="#505750")
                            win_config['color_change_text'].update('white', button_color=('black','white'))
                            
                            _theme = 'Dark'
                            _button = "#004F00"
                            _button_press = "#324f32"
                            _second = "#505750"
                            _text = "white"
                    except Exception as erro:
                        user.log_error(f'Falha ao escolher novo tema - ({erro})', user.debug_status)
                elif event == 'color_change_button':
                    try:
                        __color = user.popupColorChooser('Escolha a cor dos Botões.')
                    except:
                        __color = None
                    win_config['-combo_themes-'].update('Personalizado')
                    win_config['color_change_button'].update(__color['Cor'], button_color=__color['Codigo'])

                    _button = __color['Codigo']
                elif event == 'color_change_button_pressed':
                    try:
                        __color = user.popupColorChooser('Escolha a cor de Botões apertados.')
                    except:
                        __color = None
                    win_config['-combo_themes-'].update('Personalizado')
                    win_config['color_change_button_pressed'].update(__color['Cor'], button_color=__color['Codigo'])

                    _button_press = __color['Codigo']
                elif event == 'color_change_second':
                    try:
                        __color = user.popupColorChooser('Escolha a cor Secundaria do App.')
                    except:
                        __color = None
                    win_config['-combo_themes-'].update('Personalizado')
                    win_config['color_change_second'].update(__color['Cor'], button_color=__color['Codigo'])

                    _second = __color['Codigo']
                elif event == 'color_change_text':
                    try:
                        __color = user.popupColorChooser('Escolha a cor do Texto do App')
                    except:
                        __color = None
                    win_config['-combo_themes-'].update('Personalizado')
                    win_config['color_change_text'].update(__color['Cor'], button_color=__color['Codigo'])

                    _text = __color['Codigo']
                elif event == "Salvar":
                    try:
                        user.changePreferences(
                            theme=_theme, 
                            button_color=_button,
                            pressed_button_color=_button_press, 
                            second_color=_second, 
                            text_color=_text, 
                            font=values['combo_font'],
                            font_size=values['-font_size-']
                        )

                        user.theme_name=_theme
                        user.button_color = _button
                        user.pressed_button_color = _button_press
                        user.second_color = _second
                        user.text_color = _text
                        user.font = _font
                        user.font_size = _font_size

                        win_config.close()
                        main_window.close()
                        sg.theme(user.theme_name)

                        if user.area=='DaviK':
                            main_window = sg.Window(
                                'DaviK', 
                                layout_davik(
                                    report_data=user.last_report,
                                    color_list=user.coloringRows(
                                        user.last_report,
                                        user.text_color,
                                        user.second_color
                                    ),
                                    name=user.name,
                                    user_pc=user.PC,
                                    gauge_list=user.gauge_list,
                                    material_list=user.material_list,
                                    standards_list=user.standards_list,
                                    button_color=user.button_color,
                                    pressed_button_color=user.pressed_button_color,
                                    text_color=user.text_color,
                                    second_color=user.second_color
                                ),
                                resizable=True
                            )
                        elif user.area == 'Konemetal':
                            main_window = sg.Window(
                                'Konemetal',    
                                layout_konemetal(
                                    report_data=user.last_report, 
                                    color_list=user.coloringRows(
                                        user.last_report,
                                        user.text_color, 
                                        user.second_color
                                    ), 
                                    name=user.name, 
                                    user_pc=user.PC, 
                                    gauge_list=user.gauge_list, 
                                    material_list=user.material_list, 
                                    standards_list=user.standards_list, 
                                    today_date=datetime.now().date().strftime('%d/%m/%Y'), 
                                    button_color=user.button_color, 
                                    pressed_button_color=user.pressed_button_color, 
                                    text_color=user.text_color, 
                                    second_color=user.second_color,
                                    extra_mp_report_data=user.updateExtraMp()                        ), 
                                resizable=True
                            )
                        break
                    except Exception as erro:
                        user.log_error(f'Falha ao salvar temas selecionados - ({erro})', user.debug_status)
                        sg.Popup('Falha ao salvar temas selecionados')
                else:
                    ...
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'Bitola' or event == 'Norma' or event == 'Material':
        if user.config_acess:
            def __select_category(category:str):
                if category == 'Bitola':
                    combined_list = list(zip(user.gauge_list, user.market_gauge_list))
                    result_list = [[item[0],item[1]] for item in combined_list]
                    main_window['-bitola-'].update(values=user.gauge_list)
                elif category == 'Material':
                    combined_list = list(zip(user.material_list, user.market_material_list))
                    result_list = [[item[0],item[1]] for item in combined_list]
                    main_window['-material-'].update(values=user.material_list)
                elif category == 'Norma':
                    combined_list = list(zip(user.standards_list, user.market_standards_list))
                    result_list = [[item[0],item[1]] for item in combined_list]
                    main_window['-norma-'].update(values=user.standards_list)
                return result_list

            _category = event
            win_reg_std = sg.Window(
                f'Cadastro/Edição de {event}', 
                register_standards(values=__select_category(_category), area=_category),
                keep_on_top=True
            )
            while True:
                event, values = win_reg_std.read()
                if event == sg.WIN_CLOSED:
                    win_reg_std.close()
                    break
                elif event == 'Cadastrar':
                    try:
                        user.configurationSetter(
                            category=_category,
                            internal_std=values['-internal_std-'], 
                            market_std=values['-market_std-']
                        )

                        settings = userSettings(USUARIO['user'])

                        user.gauge_list = settings['gauge_list']
                        user.market_gauge_list = settings['market_gauge_list']
                        user.material_list = settings['material_list']
                        user.market_material_list = settings['market_material_list']
                        user.standards_list = settings['standards_list']
                        user.market_standards_list = settings['market_standards_list']

                        win_reg_std['-std_table-'].update(values=__select_category(_category))
                    except Exception as erro:
                        user.log_error(f'Falha ao cadastrar {_category} - ({erro})', user.debug_status)
                        sg.Popup(f'Falha ao cadastrar {_category}')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'Fornecedor':  
        if user.config_acess:
            with open(SUPPLIERS, 'r', encoding='UTF-8') as file:
                archive = json.load(file)
                supplier_list = list(archive.keys())

            win_sup_conf = sg.Window(
                'Configuração de fornecedores',
                supplier_config(supplier_list=supplier_list),
                keep_on_top=True
            )

            while True:
                event, values = win_sup_conf.read()
                # print(event,values)
                if event == sg.WIN_CLOSED or event == 'Sair sem salvar':
                    win_sup_conf.close()
                    break
                elif event == 'Salvar alterações':
                    try:
                        user.suppliers_parameter_config(
                            material_config=False,
                            empresa=values['-empresa-'], 
                            entrega=values['-entrega-'], 
                            kg_min=values['-min_kg-'], 
                            val_min=values['-min_val-'], 
                            item_min=values['-min_item-'],
                            tax=values['-tax-'],
                            seller=values['-vendedor-'],
                            email=values['-email-']
                        )
                        user.log_success(f'Dados do fornecedor {values["-empresa-"]} salvos',user.debug_status)
                    except Exception as erro:
                        user.log_error(f'Falha ao escolher novo tema - ({erro})', user.debug_status)
                        sg.Popup('Falha ao escolher novo tema')
                elif event == '-sup_selector-':
                    try:
                        supplier = values[event]

                        with open(SUPPLIERS, 'r') as file:
                            archive = json.load(file)

                            _bitola_list = archive[supplier]['Normas']['Bitolas']
                            _norma_list = archive[supplier]['Normas']['Normas']
                            _fabricacao_list = archive[supplier]['Normas']['Fabricacao']

                            seller_name = archive[supplier]['Nome_vendedor']
                            seller_email = archive[supplier]['email']

                            delivery = archive[supplier]['Frete']['Entrega']
                            kg_min = archive[supplier]['Frete']['Kg_minimo']
                            val_min = archive[supplier]['Frete']['Valor_minimo']
                            min_per_item = archive[supplier]['Frete']['Kg_minimo_por_item']
                            tax = archive[supplier]['Frete']['Taxa']
                        
                        win_sup_conf['-Bitola_list-'].update(_bitola_list)
                        win_sup_conf['-Norma_list-'].update(_norma_list)
                        win_sup_conf['-Fabricação_list-'].update(_fabricacao_list)
                        win_sup_conf['-empresa-'].update(supplier)
                        win_sup_conf['-vendedor-'].update(seller_name)
                        win_sup_conf['-email-'].update(seller_email)
                        win_sup_conf['-entrega-'].update(delivery)
                        win_sup_conf['-min_kg-'].update(kg_min)
                        win_sup_conf['-min_val-'].update(val_min)
                        win_sup_conf['-min_item-'].update(min_per_item)
                        win_sup_conf['-tax-'].update(tax)
                    except Exception as erro:
                        user.log_error(f'Falha ao carregar informações do fornecedor - ({erro})', user.debug_status)
                        sg.Popup('Falha ao carregar informações do fornecedor')
                elif event.startswith('add'):
                    try:
                        if event == 'add-Bitola':
                            _bitola_list.append(values['add-Bitola_parameter'])
                            user.suppliers_parameter_config(
                                material_config=True,
                                empresa=values['-empresa-'],
                                material_area='Bitolas',
                                material_parameter=values['add-Bitola_parameter'] 
                            )
                            win_sup_conf['-Bitola_list-'].update(values=_bitola_list)
                        elif event == 'add-Norma':
                            _norma_list_norma_list.append(values['add-Norma_parameter'])
                            user.suppliers_parameter_config(
                                material_config=True,
                                empresa=values['-empresa-'],
                                material_area='Normas',
                                material_parameter=values['add-Norma_parameter'] 
                            )
                            win_sup_conf['-Norma_list-'].update(values=_norma_list_norma_list)
                        elif event == 'add-Fabricação':
                            _bitola_list.append(values['add-Fabricação_parameter'])
                            user.suppliers_parameter_config(
                                material_config=True,
                                empresa=values['-empresa-'],
                                material_area='Fabricacao''',
                                material_parameter=values['add-Fabricação_parameter'] 
                            )
                            win_sup_conf['-Fabricação_list-'].update(values=_bitola_list)
                        user.log_success(f"{event} com sucesso na {values['-empresa-']}", user.debug)
                    except Exception as erro:
                        user.log_error(f"Falha ao {event} na empresa {values['-empresa-']}- ({erro}))",user.debug_status)
                        sg.Popup(f'Falha ao {event}')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'Visualizar Historico de Logs':
        if user.debug_tools_acess:
            with open((str(LOG_FILE)), 'r') as file:
                lines = file.readlines()[-10:]

            msg = ''
            for line in lines:
                msg += line + '\n' 

            sg.Popup('Historico de logs\n'+msg)        
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-debug-' or event == 'Console Debug':
        if user.debug_tools_acess:
            if user.debug_status:
                user.debug_status = False
                main_window['debug_status'].update('')
            else:
                user.debug_status = True
                main_window['debug_status'].update('Debug ON')
                sg.Print('Debug console ON...\n',colors=('black'))
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'add_ext_mp':
        if user.register_mp_acess:
            try:
                _description = values['decr_ext_mp'] if values['decr_ext_mp'] else ''
                _amount = values['qtd_ext_mp'] if values['qtd_ext_mp'] else ''
                _document = values['doc_ext_mp'] if values['doc_ext_mp'] else ''
                _observation = values['obs_ext_mp'] if values['obs_ext_mp'] else ''
                
                user.registerExtraMp(_description, _amount, _document, _observation)

                main_window['-tabela_kone_extra_mp-'].update(
                    values=user.updateExtraMp())
                user.log_success(f"Material extra registrado com sucesso", user.debug_status)   
            except Exception as erro:
                user.log_error(f'Falha ao resistrar material - ({erro})',user.debug_status)              
                sg.popup('Não foi possivel registar material')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == 'Apagar Linha':  # material extra
        if user.delete_mp_acess:
            try:
                extra_mp_report = user.updateExtraMp()
                __index = extra_mp_report[values['-tabela_kone_extra_mp-'][0]][-1]
                user.deleteExtraMp(__index)

                main_window['-tabela_kone_extra_mp-'].update(
                    values=user.updateExtraMp())
                user.log_success('Linha de mp extra apagada com sucesso', user.debug_status)
            except Exception as erro:
                user.log_error(f'Não foi possível apagar linha de mp extra - ({erro})',user.debug_status)
                sg.Popup('Não foi possível apagar linha de mp extra')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-search_item-':
        if user.mp_filter_acess:
            try:  
                window_filtermp = sg.Window('Filtrar linhas', filterpopup(), keep_on_top=True)
                while True:
                    event, values = window_filtermp.read()

                    if event == sg.WIN_CLOSED or event == 'Sair':
                        window_filtermp.close()
                        break
                    elif event == 'Filtrar':
                        filtro = values["filtro_valor"].upper()

                        if values['radio_filtro_bitola']:
                            _filter_by = 'Bitola'
                        elif values['radio_filtro_norma']:
                            _filter_by = 'Norma'
                        elif values['radio_filtro_Dimensao']:
                            _filter_by = 'Dimensao'
                        elif values['radio_filtro_documento']:
                            _filter_by = 'Documento'
                        elif values['radio_filtro_oc']:
                            _filter_by = 'Ordem_Compra'
                        else:
                            sg.Popup('Escolha o tipo de filtro...')

                        user.last_report =  user.filterReport(
                            filter_by=_filter_by, 
                            filter_key=filtro, 
                            historic=False
                        )

                        filtrado = True

                        main_window['-tabela_main-'].update(
                            values=user.last_report, 
                            row_colors=user.coloringRows(
                                data=user.last_report, 
                                user_text_color=user.text_color, 
                                user_background_color=user.second_color
                            )
                        )
                        window_filtermp.close()

                    user.log_success('Relatorio filtrado com sucesso', user.debug_status)
                    break
            except Exception as erro:
                user.log_error(f'Não foi possivel Filtrar relatorio - ({erro})',user.debug_status)
                sg.Popup('Não foi possivel Filtrar relatorio')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-refresh_report-':
        if user.report_tools_acess:
            try:
                filtrado = False
                user.last_report = user.updateReport()
                main_window['-tabela_main-'].update(
                        values=user.last_report, 
                        row_colors=user.coloringRows(user.last_report, user.text_color, user.second_color))
                user.log_success('Relatorio foi atualizado com sucesso.', user.debug_status)
            except Exception as erro:
                user.log_error(f'Falha ao atualizar relatorio - ({erro})',user.debug_status)
                sg.Popup('Não foi possivel atualizar relatorio.')             
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-register-':
        if user.register_mp_acess:
            try:   

                if '/' in values['-dimensao-']:
                    if '"' in values['-dimensao-']:
                        pass
                    else:
                        values['-dimensao-'] + '"'

                if user.area == 'Konemetal':
                    if values['-bitola-'] and values['-material-'] \
                    and values['-norma-'] and values['-dimensao-'] \
                    and values['-quantidade-'] and values['-documento-'] \
                    and values['-data-'] and values['-pfabricacao-']:
                        user.registerReport(
                            values['-bitola-'].strip(), values['-material-'].strip(),
                            values['-norma-'].strip(), values['-dimensao-'].strip(), 
                            int(values['-quantidade-']), values['-pfabricacao-'].strip(), 
                            values['-documento-'].strip(), values['-data-'].strip(),
                            user.name
                        )
                    else:
                        user.log_error('Falha ao resistrar material',user.debug_status)              
                        sg.popup('Digite todos os valores para adicionar material.')

                elif user.area == 'DaviK':
                    if values['-bitola-'] and values['-material-'] \
                    and values['-norma-'] and values['-dimensao-'] \
                    and values['-quantidade-']:
                        user.registerReport(
                            values['-bitola-'].strip(),
                            values['-material-'].strip(), 
                            values['-norma-'].strip(),
                            values['-dimensao-'].strip(), 
                            values['-quantidade-'].strip(),
                            values['-pfabricacao-'].strip(), 
                            user.name
                        )
                    else:
                        user.log_error('Falha ao resistrar material',user.debug_status)              
                        sg.popup('Digite todos os valores para adicionar material.')

                user.last_report = user.updateReport()
                main_window['-tabela_main-'].update(  
                    values=user.last_report, 
                    row_colors=user.coloringRows(user.last_report, user.text_color, user.second_color))
                user.log_success(f"Material {values['-bitola-'].strip()}{values['-material-'].strip()}{values['-norma-'].strip()} {values['-dimensao-'].strip()} {int(values['-quantidade-'])}mm {values['-pfabricacao-'].strip()} registrado com sucesso",user.debug_status)
            except Exception as erro:
                user.log_error(f'Falha ao registrar material - ({erro})')
                sg.Popup('Falha ao registrar material')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-save_backup-' or event == 'Salvar BackUp':
        if user.report_tools_acess:
            try:
                user.saveFile()
                sg.popup(f'Backup salvo')
                user.log_success('Backup salvo com sucesso', user.debug_status)
            except Exception as erro:
                user.log_error(f'Falha ao salvar Backup - ({erro})', user.debug_status)
                sg.popup('Não foi possivel salvar o Backup')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-make_excel_report-' or event == 'Gerar Relatorio em Excel':
        if user.report_tools_acess:
            try:
                # user.makeDictReport()
                user.makeExcelReport()
                sg.popup('Relatorio criado, verifique o Atalho "relatorios"')
                user.log_success('Relatorio Excel criado com sucesso', user.debug_status)
            except Exception as erro:
                user.log_error(f'Não foi possivel criar relatorio excel - ({erro})', user.debug_status)
                sg.popup("Não foi possivel criar relatorio excel") 
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-dashbord-' or event == 'Dashbord':
        if user.report_tools_acess:
            try:
                dash_data = user.dashbordData()
                window_dashbord = sg.Window('Gráficos', dashbord(user.name.capitalize(), user.area.capitalize(), 
                str(datetime.now().date())[2:], dash_data['kg_total'][0][0]), finalize=True, resizable=True,
                location=(200,100), keep_on_top=True)
                canvas_elem = window_dashbord['-CANVAS_row1-']
                canvas_elem2 = window_dashbord['-CANVAS_row2-']

                fig_top5_mat, ax_top5_mat = plt.subplots(figsize=(6,2.5))
                ax_top5_mat.bar(
                    dash_data['top5_names'], 
                    dash_data['top5_values'], 
                    label=['blue'], 
                    color=['tab:blue']
                )
                ax_top5_mat.set_ylabel('quilos')
                ax_top5_mat.set_title('Top 5 quantidades')
                canvas_barra = FigureCanvasTkAgg(fig_top5_mat, master=canvas_elem.Widget)
                canvas_barra.get_tk_widget().pack(side='left', fill='both', expand=1)


                porcent_normas, ax_norma = plt.subplots(figsize=(3.5,2.5))
                ax_norma.pie(
                    dash_data['norma_values'], 
                    labels=dash_data['norma_names'], 
                    autopct='%1.1f%%'
                    )
                ax_norma.set_title('Divisão por normas')
                canvas_norma = FigureCanvasTkAgg(porcent_normas, master=canvas_elem.Widget)
                canvas_norma.get_tk_widget().pack(side='right', fill='both', expand=1)


                porcent_bitola, ax_bitola = plt.subplots(figsize=(3.5,2.5))
                ax_bitola.pie(dash_data['bitola_values'], labels=dash_data['bitola_names'], autopct='%1.1f%%')
                ax_bitola.set_title('Divisão por bitola')
                canvas_bitola = FigureCanvasTkAgg(porcent_bitola, master=canvas_elem2.Widget)
                canvas_bitola.get_tk_widget().pack(side='right', fill='both', expand=1)


                porcent_fabr, ax_fabr = plt.subplots(figsize=(3.5,2.5))
                ax_fabr.pie(dash_data['fabricacao_values'], labels=dash_data['fabricacao_names'], autopct='%1.1f%%')
                ax_fabr.set_title('Divisão por fabricação')
                canvas_fabr = FigureCanvasTkAgg(porcent_fabr, master=canvas_elem2.Widget)
                canvas_fabr.get_tk_widget().pack(side='right', fill='both', expand=1)

                event, values = window_dashbord.read()
            except Exception as erro:
                user.log_error(f'Não foi possivel gerar grafico de necessidade - {erro}', user.debug_status)
                sg.Popup('Não foi possivel gerar grafico de necessidade')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == "Gerar relatorio semanal e avisar por E-mail":
        if user.email_tools_acess:
                pass
                # try:
                #     relatorio_kone = konemetal.updateReport()
                #     relatorio_davik = davik.updateReport()

                #     relatorio_unificado = compras.makeGeneralReport() # desatualizado
                #     relatorio_unificado = compras.convert_mm_kg(
                #         relatorio_unificado
                #     )
                #     relatorio_unificado = compras.updateReport(
                #         relatorio_unificado
                #     )

                #     compras.sendEmail(
                #         relatorio_kone, relatorio_davik, relatorio_unificado
                #     )
                # except:
                #     sg.popup('erro ao enviar gerar relatorio')
        else:
            sg.Popup(f'Usuario {user.name} não tem permissão para acessar {event}')
    elif event == '-info-':
        pass
        # frases_motivacionais = [
        #         "Continue tentando que vai dar certo! Errado já está dando.\nNa hora certa, tudo vai dar errado.\nO mérito da derrota é todo seu, orgulhe-se...",
        #         "Um dia você perde. No outro você não ganha.",
        #         "Tudo aquilo que você passou até agora está te preparando para algo pior.",
        #         "A inteligência artificial só não é mais incrível do que a sua burrice natural",
        #         "Você não pode mudar o seu passado, mas pode estragar seu futuro",
        #         "Não sabendo que era impossível, foi lá e descobriu",
        #         "Veja pelo lado bom: não há!",
        #         'Seu problema foi deixar a impressora perceber que você estava com pressa.',
        #         "O não você já tem, agora vá a luta! Busque a humilhação!",
        #         "Nenhum obstáculo é grande demais para quem desiste!",
        #         "Não deixe que uma frase motivacional melhore o seu dia!",
        #         "Não se preocupe se você perder, nós não esperávamos mais de você!"]

        # msg = choice(frases_motivacionais)
        # sg.Popup('Algo esta dando errado?', msg)
    elif event == '-add_item-':
        add_linhas_carteira = sg.Window('gg',add_pedido(), keep_on_top=True)
        while True:
            event, values = add_linhas_carteira.read()
            if event == sg.WIN_CLOSED:
                add_linhas_carteira.close()
                break
            elif event == '-new_line-':
                add_linhas_carteira.extend_layout(
                    add_linhas_carteira['linhas_frame'], [
                        [
                            sg.Frame('Bitola',[[sg.Input(size=3)]]),
                            sg.Frame('Material',[[sg.Input(size=7)]]), 
                            sg.Frame('Norma',[[sg.Input(size=3)]]), 
                            sg.Frame('Dimensão',[[sg.Input(size=10)]]),
                            sg.Frame('Comprimento',[[sg.Input(size=6)]]),
                            sg.Frame('Fabricação',[[sg.Input(size=10)]]),
                            sg.Frame('Data Entrega',[[sg.Input(size=10)]]),
                            sg.Frame('Documento',[[sg.Input(size=10)]])
                        ]
                    ])
            elif event == 'salvar':
                user.registerReport()
                
    # Calculator 
    elif event == 'botao_red':
        try:
            if values['radio_material_1']:
                material = 'aco'
            elif values['radio_material_2']:
                material = 'latao'
            elif values['radio_material_3']:
                material = 'aluminio'

            medida = values['valor_red'].replace(',', '.')
            medida = float(medida)

            valor = user.calculateWeight(
                'redondo', medida, material=material
                )
            main_window['kg_m_red'].update(valor)

            user.log_success(
                f'Calculo redondo {values["valor_red"]} = {valor}',
                user.debug_status)
        except Exception as erro:
            user.log_error(f'Falha ao calcular redondo {values["valor_red"]} - ({erro})',user.debug_status)
            sg.popup(f'Falha ao calcular redondo {values["valor_red"]}')
    elif event == 'botao_sext':
        try:
            if values['radio_material_1']:
                material = 'aco'
            elif values['radio_material_2']:
                material = 'latao'
            elif values['radio_material_3']:
                material = 'aluminio'

            medida = values['valor_sext'].replace(',', '.')
            medida = float(medida)

            valor = user.calculateWeight(
                'sextavado', medida, material=material
                )
            main_window['kg_m_sext'].update(valor)
            user.log_success(
                f'calculo_sext {values["valor_sext"]} = {valor}', user.debug_status
                )
        except Exception as erro:
            user.log_error(f'Falha ao calcular sextavado {values["valor_sext"]} - ({erro})',user.debug_status)
            sg.popup(f'Digite um valor valido')
    elif event == 'botao_quad':
        try:
            if values['radio_material_1']:
                material = 'aco'
            elif values['radio_material_2']:
                material = 'latao'
            elif values['radio_material_3']:
                material = 'aluminio'

            base = values['valor_quad1'].replace(',', '.')
            base = float(base)
            altura = values['valor_quad2'].replace(',', '.')
            altura = float(altura)

            valor = user.calculateWeight(
                'quadrado', base, altura, material=material
                )
            main_window['kg_m_quad'].update(valor)
            user.log_success(
                f'calculo_quad {values["valor_quad1"]}x{values["valor_quad2"]} = {valor}',
                user.debug_status)
        except Exception as erro:
            user.log_error(f'Falha ao calcular quadrado {values["valor_quad1"]}x{values["valor_quad2"]} - ({erro})',user.debug_status)
            sg.popup(f'Digite um valor valido')
    elif event == 'botao_tubo':
        try:
            if values['radio_material_1']:
                material = 'aco'
            elif values['radio_material_2']:
                material = 'latao'
            elif values['radio_material_3']:
                material = 'aluminio'

            dim_maior = values['valor_tubo_maior'].replace(',', '.')
            dim_maior = float(dim_maior)
            dim_menor = values['valor_tubo_menor'].replace(',', '.')
            dim_menor = float(dim_menor)

            valor = user.calculateWeight(
                'tubo', dim_maior, dim_menor, material
                )
            main_window['kg_m_tubo'].update(valor)
            user.log_success(
                f'calculo_tubo {values["valor_tubo_maior"]}x{values["valor_tubo_menor"]} = {valor}',
                user.debug_status)
        except Exception as erro:
            user.log_error(f'Falha ao calcular tubo {values["valor_tubo_maior"]}x{values["valor_tubo_menor"]} - ({erro})', user.debug_status)
            sg.popup(f'Digite um valor valido')
    elif event == 'calcular_mm_pol':
        try:
            valor = user.mm_polegada(str(values['valor_mm_pol']))
            main_window['resposta_mm_pol'].update(valor)
            user.log_success(f"Calculo mm/pol {values['valor_mm_pol']} = {valor}", user.debug_status)
        except Exception as erro:
            user.log_error(f"Falha ao converter {values['valor_mm_pol']} em polegada - ({erro})",user.debug_status)
            sg.popup(f'Digite um valor valido')
    elif event == 'calcular_pol_mm':
        try:
            valor = user.polegada_mm(str(values['valor_pol_mm']))
            main_window['resposta_pol_mm'].update(valor)
            user.log_success(f"Calculo pol/mm {values['valor_pol_mm']} = {valor}", user.debug_status)
        except Exception as erro:
            user.log_error(f"Falha ao converter {values['valor_pol_mm']} em mm\nerro: {erro}")
            sg.popup(f'Digite um valor valido\nerro: {erro}')
    elif event == 'calcular_quantidade':
        try:
            valores = user.forgedWeight(
                int(values['valor_calculo_forjados']), 'qtd'
                )

            main_window['jl2_result'].update(valores[0])
            main_window['jl3_result'].update(valores[1])
            main_window['jl4_result'].update(valores[2])
            main_window['jl5_result'].update(valores[3])
            main_window['jl6flange_result'].update(valores[4])
            main_window['tee2_result'].update(valores[5])
            main_window['tee3_result'].update(valores[6])
            main_window['tee5_result'].update(valores[7])
            main_window['teech36_result'].update(valores[8])
            main_window['cz4_result'].update(valores[9])
            main_window['cz6_result'].update(valores[10])

            user.log_success(f"Quantidade {values['valor_calculo_forjados']} de forjados calculada", user.debug_status)
        except Exception as erro:
            user.log_error(f"Falha em calcular quantidade de {values['valor_calculo_forjados']} forjados - ({erro})", user.debug_status)
            sg.popup('Erro ao calcular quantidade')
    elif event == 'calcular_kg':
        try:
            valores = user.forgedWeight(
                int(values['valor_calculo_forjados']), 'kg'
                )

            main_window['jl2_result'].update(valores[0])
            main_window['jl3_result'].update(valores[1])
            main_window['jl4_result'].update(valores[2])
            main_window['jl5_result'].update(valores[3])
            main_window['jl6flange_result'].update(valores[4])
            main_window['tee2_result'].update(valores[5])
            main_window['tee3_result'].update(valores[6])
            main_window['tee5_result'].update(valores[7])
            main_window['teech36_result'].update(valores[8])
            main_window['cz4_result'].update(valores[9])
            main_window['cz6_result'].update(valores[10])

            user.log_success('Quilos dos forjados calculado com sucesso.',user.debug_status)
        except Exception as erro:
            sg.popup('Erro ao calcular quilos dos forjados')
            user.log_error(f"Falha ao calcular quilos de {values['valor_calculo_forjados']} forjados. - ({erro})", user.debug_status)
     
    # Filtros
    elif '+CLICKED+' in event:
        if isinstance(event[2][0], int):
            if event[2][0] == -1:
                if user.mp_filter_acess:
                    # try:
                    _order = user.last_filter_order
                    if event[2][1] == 0:
                        selected_column = 'Bitola'
                    elif event[2][1] == 1:
                        selected_column = 'Material'
                    elif event[2][1] == 2:
                        selected_column = 'Norma'
                    elif event[2][1] == 3:
                        selected_column = 'Dimensao'
                    elif event[2][1] == 4:
                        selected_column = 'Fabricacao'
                    elif event[2][1] == 5:
                        selected_column = 'Kg_Solicitado'
                    elif event[2][1] == 6:
                        selected_column = 'Documento'
                    elif event[2][1] == 7:
                        selected_column = 'Data_Entrega_Peca'

                    if selected_column == user.last_filter and user.last_filter_order == _order:
                        if _order == 'ASC':
                            _order = 'DESC'
                        else:
                            _order = 'ASC'
                    
                    user.last_filter = selected_column
                    user.last_filter_order = _order

                    user.last_report = user.sortedRowsTables(user.last_report ,event[2][1], user.last_filter_order)

                    main_window['-tabela_main-'].update(
                        values=user.last_report, 
                        row_colors=user.coloringRows(
                            user.last_report,
                            user.text_color, 
                            user.second_color
                        )
                    )

                    # except Exception as erro:
                    #     user.log_error(f'Erro ao filtrar relatorio - ({erro})',user.debug_status)
                else:
                    sg.Popup(f'usuario {user.name} não tem permissão de filtrar relatorio')
    
    # Right click selection
    elif event == 'Editar':
        if len(values['-tabela_main-']) == 1:
            _line_selected = values['-tabela_main-'][0]
            mat_info = user.last_report[_line_selected]
            item_id = mat_info[-1]
            item_comprado = mat_info[-2]
            mat_values = user.catchValues(item_id)
            
            if item_comprado:
                __answer = sg.popup_yes_no('Material já comprado.\nA unica alteração possivel é a da data de entrega.\nDeseja altera a data?')
                if __answer == 'Yes':
                    new_date = sg.popup_get_date()
                    __day = new_date[1]
                    __month = new_date[0]
                    __year = new_date[2]
                    new_date = f'{__day}/{__month}/{__year}'
                    data_formatada = str(datetime.strptime(new_date, "%d/%m/%Y").date())

                    # try: ###                                  NAO É LISTA É DICIONARIO....
                    bitola = mat_values['Bitola']
                    material = mat_values['Material']
                    norma = mat_values['Norma']
                    dimensao = mat_values['Dimensao']
                    milimetros =  mat_values['Milimetros']
                    fabricacao = mat_values['Fabricacao']
                    data_entrega = data_formatada
                    urgente = mat_values['Urgente']
                    documento = mat_values['Documento']
                    codigo_peca = mat_values['Codigo_Peca']

                    if user.area == 'Konemetal':
                        user.editReport( 
                            item_id, 
                            bitola, material, norma, 
                            dimensao, milimetros, fabricacao, 
                            data_entrega, 
                            urgente, 
                            documento, codigo_peca 
                        )
                    elif user.area == "DaviK":                                
                        user.editReport(
                            item_id, 
                            bitola, material, norma, 
                            dimensao, milimetros, fabricacao, comprado,
                            urgente
                        )
                    user.last_report = user.updateReport()
                    main_window['-tabela_main-'].update(
                        values=user.last_report, 
                        row_colors=user.coloringRows(
                            user.last_report, 
                            user.text_color, 
                            user.second_color
                        )
                    )
                    user.log_success(f'Data alterada do item ja comprado  {bitola}{material}{norma} {dimensao} {milimetros}mm {fabricacao} {"Urgente" if urgente else "_"}', user.debug_status)
                    # except Exception as erro:
                    #     sg.popup('Falha ao editar relatorio')
                    #     user.log_error(f'Falha ao editar material: - ({erro})', user.debug_status)
            else:
                window_editmp = sg.Window(f'{mat_info[0]}{mat_info[1]}{mat_info[2]} {mat_info[3]}', editpopup(mat_values, user.area),
                keep_on_top=True)
                while True:
                    event, values = window_editmp.read()

                    if event == 'Sair' or event == sg.WIN_CLOSED:
                        window_editmp.close()
                        break
                    elif event == 'Excluir':
                        user.removeIten(item_id)

                        window_editmp.close()

                        user.last_report = user.updateReport()
                        main_window['-tabela_main-'].update(
                            values=user.last_report, 
                            row_colors=user.coloringRows(
                                user.last_report, 
                                user.text_color, 
                                user.second_color
                            )
                        )
                    elif event == 'Salvar':
                        # try:
                        if user.area == 'Konemetal':
                            user.editReport(
                                id=item_id,
                                bitola=values['-popbitola-'].upper(),
                                material=values['-popmaterial-'].upper(),
                                norma=values['-popnorma-'].upper(), 
                                dimensao=str(values['-popdimensao-']).upper(),
                                milimetros=int(values['-popquantidade-']),
                                fabricacao=values['-poppfrabricacao-'].upper(),
                                data_entrega=datetime.strptime(values['-popdata-'], "%d/%m/%Y").strftime("%Y-%m-%d"),
                                urgente=1 if values['-popurgente-'] else 0,
                                documento=values['-popdoc-'],
                                codigo_peca= values['-popcodigo-'].upper()
                                )

                        elif user.area == "DaviK":
                            bitola = values['-popbitola-'].upper()
                            material = values['-popmaterial-'].upper()
                            norma = values['-popnorma-'].upper()
                            dimensao = str(values['-popdimensao-'])
                            milimetros =  int(values['-popquantidade-'])
                            fabricacao = values['-poppfrabricacao-'].upper()
                            comprado = 1 if values['-popcomprado-'] else 0
                            urgente = 1 if values['-popurgente-'] else 0
                                
                            user.editReport(
                                item_id, 
                                bitola, material, norma, 
                                dimensao, milimetros, fabricacao, comprado,
                                urgente
                                )
                        window_editmp.close()
                        user.last_report = user.updateReport()
                        main_window['-tabela_main-'].update(
                            values=user.last_report, 
                            row_colors=user.coloringRows(
                                user.last_report, 
                                user.text_color, 
                                user.second_color
                            )
                        )
                        user.log_success(f"Salvo no banco de dados material: {values['-popbitola-'].upper()}{values['-popmaterial-'].upper()}{values['-popnorma-'].upper()} {str(values['-popdimensao-'])} {int(values['-popquantidade-'])}mm {values['-poppfrabricacao-'].upper()} {'Urgente' if values['-popurgente-'] else '_'} {'Comprado' if values['-popcomprado-'] else '_'}", user.debug_status)
                        break
                        # except Exception as erro:
                        #     sg.popup('Falha ao editar relatorio')
                        #     user.log_error(f'Falha ao editar material: - ({erro})', user.debug_status)
        elif len(values['-tabela_main-']) > 1:
            sg.Popup('Metodo de editar varias linhas desabilitado...')
        else:
            sg.Popup('Escolha ao menos uma linha para editar')
    elif event == 'Confirmar Recebimento': # Se a quantidade recebida for menor que a solicitada deve dividir a linha e ir para o historico apenas oq foi comprado e o saldo ficar na necessidade (se a pessoa quiser)
        _date = datetime.now().date().strftime('%d/%m/%Y')
        material_list_to_receive = list()
        __acesso = True
        for item in values['-tabela_main-']:
            material_list_to_receive.append(user.last_report[item])
            if not user.last_report[item][-2]:
                sg.Popup('Não é possivel receber um material que não foi comprado')
                __acesso = False
                break
        if __acesso:
            window_receivemp = sg.Window('Confirmar Recebimento', receive_mp_info(material_list_to_receive, _date, user.area),
                keep_on_top=True)
            while True:
                event, values = window_receivemp.read()
                if event == 'Sair' or event == sg.WIN_CLOSED:
                    window_receivemp.close()
                    break
                elif event == 'Confirmar Recebimento':
                    # try:
                    for item in material_list_to_receive:
                        _index = item[-1]
                    
                        _fiscal_note = values['-notafiscal-']
                        _date_receive = datetime.strptime(window_receivemp['-DATE-'].get(), "%d/%m/%Y").date()

                        try:
                            _kg_receive = values[f'mp_id_{_index}']
                            print(_kg_receive)
                        except:
                            _kg_receive = values[f'mp_id_{item[0]}{item[1]}{item[2]} {item[3]} {item[4]}']

                            _kg_total_solicitado = 0
                            _number_itens = 0
                            _kg_solicitado_item = item[5]

                            for i in material_list_to_receive:
                                if i[0] == item[0] and i[1] == item[1] and i[2] == item[2] and i[3] == item[3] and i[4] == item[4]:
                                    _kg_total_solicitado += int(i[5])        
                                    _number_itens += 1

                            _extramp = int((int(_kg_receive) - _kg_total_solicitado)/_number_itens) ## ERADO 
                            _kg_receive = _kg_solicitado_item + _extramp

                        user.receiveItem(
                            _index, _kg_receive, _date_receive, _fiscal_note
                        )
                        
                    user.last_report = user.updateReport()
                    main_window['-tabela_main-'].update(
                        values=user.last_report, 
                        row_colors=user.coloringRows(
                            user.last_report, 
                            user.text_color, 
                            user.second_color
                        )
                    )
                    window_receivemp.close()
                    user.log_success(f'Materiais Recebidos com sucesso',user.debug_status)
                    # except Exception as erro:
                    #     user.log_error(f'Não foi possivel Receber material(s) - ({erro})',user.debug_status)
                    #     sg.Popup('Não foi possivel Receber material(s)')
    elif event == 'Informações':
        # try:
        item = user.last_report[values['-tabela_main-'][0]]
        item_id = item[-1]

        if user.area == 'Compras':
            item_solicitante = item[0]
        
            material = user.catchValues(
                line=item_id, 
                historic=False, 
                requester=item_solicitante
            )
        else:
            material = user.catchValues(
                line=item_id, 
                historic=False
            )

        wind_infos = sg.Window(
            f'{material["Bitola"]}{material["Material"]}{material["Norma"]} {material["Dimensao"]} {material["Fabricacao"]}',
            item_infos(user.marketStandard(material),
            user.area
            ),
            keep_on_top=True
        )
        event_inf, values_inf = wind_infos.read()
        # except Exception as erro:
        #     sg.Popup('Erro ao Abrir informações')
        if event_inf or event:
            wind_infos.close()
    elif event == 'Excluir':

        _line_selected = values['-tabela_main-'][0]
        mat_info = user.last_report[_line_selected]
        item_id = mat_info[-1]
        try:
            if mat_info[-2]:
                sg.Popup('Não é possivel Excluir um material comprado')
            else:
                answer = sg.popup_yes_no(f'Deseja mesmo deletar esse item?\nId:{item_id}')
                if answer == 'Yes':
                    user.removeIten(str(item_id))

                    user.last_report = user.updateReport()
                    main_window['-tabela_main-'].update(
                        values=user.last_report, 
                        row_colors=user.coloringRows(user.last_report, user.text_color, user.second_color)
                    )
                    user.log_success('Material excluido com sucesso.',user.debug_status)
        except Exception as erro:
            user.log_error(f'Falha ao retirar a linha - ({erro})', user.debug_status)
            sg.popup('Falha ao retirar a linha')
    elif event == 'Registrar Compra':

        with open(SUPPLIERS, 'r', encoding='UTF-8') as file:
            archive = json.load(file)
            supplier_list = list(archive.keys())


        list_of_itens_buyed = values['-tabela_main-']
        
        _date = datetime.now().date().strftime('%d/%m/%Y')
        list_of_buyed_mp = list()

        for item in values['-tabela_main-']:
            list_of_buyed_mp.append(user.last_report[item])

        win_register_buy = sg.Window(
            'Registar Compra',
            register_buy_info(supplier_list,
                list_of_buyed_mp,
                _date
            ),
                keep_on_top=True
        )
        while True:
            event, values = win_register_buy.read()
            if event == sg.WIN_CLOSED:
                win_register_buy.close()
                break       
            elif event == 'Salvar':
                try:
                    _fornecedor = values['-Fonecedor-']
                    _oc = values['-OC-']
                    _data_recebido = datetime.strptime(values['-DATE-'], "%d/%m/%Y").date()

                    for item in list_of_itens_buyed:
                        __material = user.last_report[item]
                        __mat_id = __material[-1]
                        __mat_resquester = __material[0]

                        user.registerPurchase(
                            fornecedor=_fornecedor,
                            oc=_oc,
                            material_id=__mat_id,
                            quantidade=values[f'kg_id_{__mat_id}'],
                            valor_kg=values[f'valor_id_{__mat_id}'],
                            data_previsao=datetime.strptime(values[f'prev_id_{__mat_id}'], "%d/%m/%Y").date(),
                            data=_data_recebido,
                            para=__mat_resquester,
                        )

                    user.last_report = user.updateReport()
                    main_window['-tabela_main-'].update(  
                        values=user.last_report, 
                        row_colors=user.coloringRows(
                            user.last_report, 
                            user.text_color, 
                            user.second_color
                        )
                    )
                    
                    win_register_buy.close()
                    break
                    user.log_success('Compra registrada com sucesso',user.debug_status)
                except Exception as erro:
                    user.log_error(f'Erro ao registrar compra. - ({erro})', user.debug_status)
                    sg.Popup('Erro ao registrar compra.')
    elif event == 'Cancelar Compra':
        _lines = values['-tabela_main-']
        print(user.last_report)
        print(_lines)
        for i in _lines:
            user.unBuy(
                user.last_report[i][-1],
                user.last_report[i][0]
            )
