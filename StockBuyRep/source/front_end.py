from pathlib import Path

import PySimpleGUI as sg

#_____TEMPLATES_________________________________________________________________
def template_menu():
	return sg.Menu([
			['Arquivo', ['Salvar BackUp', 'Gerar Relatorio em Excel']],
			['Editar', ['Preferencias', ['Aparência', 'Configurações',['Bitola','Norma','Material','Fornecedor']]]],
			['Ferramentas', ['Historico','Dashbord','Calculadora',['Exibir Calculadora']]],
			['Ajuda', ['Visualizar Historico de Logs', 'Console Debug']]
		],key='-menu-')

def template_buttons(gauge_list, material_list, standards_list, today_date, button_color, pressed_button_color):
	input_bt = [
			sg.Frame('Bitola',[[sg.Combo(gauge_list, size=7, key='-bitola-')]]), 
			sg.Frame('Material',[[sg.Combo(material_list,size=6, key='-material-')]]), 
			sg.Frame('Norma', [[sg.Combo(standards_list, size=6, key='-norma-')]]), 
			sg.Frame('Dimensão', [[sg.Input(size=17, key='-dimensao-')]]), 
			sg.Frame('Milimetros', [[sg.Input(size=6, key='-quantidade-')]]), 
			sg.Frame('Documento',[[sg.Input(size=9, key='-documento-')]]), 
			sg.Frame('Data de entrega',[[
			sg.CalendarButton(
				'Data', 
				target='-data-', 
				close_when_date_chosen=True, 
				month_names=[
					'Janeiro', 
					'Fevereiro', 
					'Março', 
					'Abril', 
					'Maio', 
					'Junho', 
					'Julho', 
					'Agosto', 
					'Setembro', 
					'Outubro', 
					'Novembro', 
					'Dezembro'
				], 
				day_abbreviations=[
					'Dom', 
					'Seg', 
					'Ter', 
					'Qua', 
					'Qui', 
					'Sex', 
					'Sáb'
				],
				format='%d/%m/%Y'
			),
			sg.InputText(default_text=today_date, key='-data-',size=(11))
			]]), 
			sg.Frame('Proc. Frabricação',[
				[sg.Combo(
					['Trefilado','Laminado','Forjado','Fresado','Retificado','Descascado','Torneado'], 
					size=13, 
					key='-pfabricacao-'
				)]
			]), 
			sg.Button(
				key='-register-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\add.png'), 
				image_size=(16,16), 
				image_subsample=8, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Registar material"
			)
		]
	controls_bt = [
			sg.Button(
				key='-add_item-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\add-document.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Adicionar Pedido"), 
			sg.Button(
				key='-search_item-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\search.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Localizar item"), 
			sg.Button(
				key='-refresh_report-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\refresh.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Atalizar relatorio"), 
			sg.Button(
				key='-dashbord-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\chart-mixed.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Dashbord de necessidade de material"), 
			sg.Button(
				key='-make_excel_report-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\file-excel.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Salvar Relatorio em Excel"),
			sg.Button(
				key='-save_backup-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\diskette.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Salvar Backup"),
			sg.Push(), 
			sg.Button(
				key='-info-', image_filename=(Path(__file__).parent.parent / 'resources\\info.png'),
				image_size=(32,32),
				image_subsample=4,
				button_color=button_color,
					mouseover_colors=pressed_button_color,
					tooltip="Informações"), 
			sg.Button(
				key='-debug-',
				image_filename=(Path(__file__).parent.parent / 'resources\\code.png'), 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Habilitar console de Debug")
		]
	
	return controls_bt

def template_footer():
	...
def template_calculator():
	...





def dashbord(nome, empresa, data, kg_total):
	return [
		[sg.Canvas(key='-CANVAS_row1-', background_color='Lightslategray')],
		[sg.Text(f'{nome}\n{empresa}\n{data}\n\nForam solicitados {kg_total}kg', font=('Roboto Condensed', 14, 'bold')),sg.Push(),sg.Canvas(key='-CANVAS_row2-')]
	]

def Collapsible(layout, key, title='', arrows=(sg.SYMBOL_DOWN, sg.SYMBOL_UP), collapsed=False):
    return sg.Column([[sg.T((arrows[1] if collapsed else arrows[0]), enable_events=True, k=key+'-BUTTON-'),
                       sg.T(title, enable_events=True, key=key+'-TITLE-')],
                      [sg.pin(sg.Column(layout, key=key, visible=not collapsed, metadata=arrows))]], pad=(0,0))

def create_layout_historic(report:list, area:str, button_color:str='#4d4d94', 
text_color:str="white", second_color:str="Lightslategray") -> list:

	column_filters = [
		[sg.Frame('Filtrar',[
			[sg.Radio('Fornecedor', 'filtro_comprados', key='fornecedor_hist')], 
			[sg.Radio('OC', 'filtro_comprados', key='oc_hist')], 
			[sg.Radio('Bitola', 'filtro_comprados', key='bitola_hist', default=True)], 
			[sg.Radio('Dimensão', 'filtro_comprados', key='dimensao_hist')], 
			[sg.Radio('Norma', 'filtro_comprados', key='norma_hist')],
			[sg.Frame('Pesquisar',[
				[sg.Input(size=15, key='chave_filtro')]
			])],
			[sg.Button('Filtrar'),sg.Button('Remover filtro')]
		])]
	]

	column_report = [
		[sg.Frame(f'Historico {area}',[
			[sg.Table(
				key='-tabela_historico-',
				expand_y = True, 
				enable_click_events=True, 
				header_background_color=button_color, 
				header_text_color=text_color, 
				alternating_row_color=second_color, 
				values=report,
				right_click_menu=['Click',['Informações',]],
				size=(100,25),
				headings=[
					'Data Recebido','Fornecedor','OC','Material','Kg Recebidos','R$/Kg'
				]
			)]
		])]
	]

	return [[sg.Col(column_filters),sg.Col(column_report)]]

def editpopup(values, user:str=''):
	layout =  [
		[
			sg.Text('Bitola:'),sg.Input(key='-popbitola-',size=(4), default_text=values['Bitola']),sg.Push(),
			sg.Text('Material:'),sg.Input(key='-popmaterial-',size=(2),default_text=values['Material']),sg.Push(),
			sg.Text('Norma:'),sg.Input(key='-popnorma-',size=(5),default_text=values['Norma'])
		],
		[
			sg.Text('Dimensão:'),sg.Input(key='-popdimensao-', size=(8),default_text=values['Dimensao']),sg.Push(),
			sg.Text('Quantidade em mm:'),sg.Input(key='-popquantidade-', size=(5),default_text=values['Milimetros'])
		],
		[
			sg.Text('Processo de fabricação:'),
			sg.Combo(
				['Trefilado','Laminado','Fresado','Retificado','Descascado','Torneado'], 
				default_value=values['Fabricacao'], 
				key='-poppfrabricacao-'
			)
		],
		[
			sg.Checkbox('Urgente', key='-popurgente-', default=values['Urgente']),
			sg.Checkbox('Comprado', key='-popcomprado-', default=values['Comprado'],visible=False),
			sg.Push()
		],
		[sg.Button('Salvar'),sg.Button('Excluir'),sg.Push(),sg.Button('Sair/Voltar', key='Sair')]
	]
	if user == 'Konemetal':
		layout.insert(3, [
			sg.Text('Documento:'), sg.Input(size=10, key='-popdoc-',
			default_text=values['Documento']), sg.Text('Data:'), 
			sg.Input(size=11, key='-popdata-',default_text=values['Data_Entrega_Peca'])
		])
		layout.insert(4,[
			sg.Text('Código da peça'),sg.Input(size=(20),key='-popcodigo-', 
			default_text=values['Codigo_Peca'])
		])
	return layout

def receive_mp_info(material_list:list, today_date:str, area:str):
	layout_receiving_mp = list()

	layout_receiving_mp.append(
		[sg.Text('Material',font=('Helvetica', 14)),sg.Push(),sg.Text('Kg Entregue',font=('Helvetica', 14))]
	)

	_lista_de_itens = list()
	_lista_de_ids = list()
	_lista_de_kg = list()

	for material in material_list:
		if area=='DaviK':
			_id = material[-1]
			_item = f"{material[1]}{material[2]}{material[3]} {material[4]} {material[5]}"
			_kg = int(material[6])

		elif area == 'Konemetal':
			_id = material[-1]
			_item = f"{material[0]}{material[1]}{material[2]} {material[3]} {material[4]}"
			_kg = int(material[5])

		if _item in _lista_de_itens:
			__index = _lista_de_itens.index(_item)

			_lista_de_ids[__index].append(_id)
			_lista_de_kg[__index] = _lista_de_kg[__index] + _kg

		else:
			_lista_de_itens.append(_item)
			_lista_de_ids.append([_id])
			_lista_de_kg.append(_kg)

	mat_somados ={
		'item':_lista_de_itens,
		'id':_lista_de_ids,
		'kg':_lista_de_kg
	}

	for i in range(len(_lista_de_itens)):
		id_format = mat_somados["id"][i][0] if len(mat_somados['id'][i])==1 else mat_somados['item'][i]
		layout_receiving_mp.append(
			[
				sg.Text(
					f"{len(mat_somados['id'][i])}- {mat_somados['item'][i]} - {mat_somados['kg'][i]}kg"
				),
				sg.Push(),
				sg.Input(
					key=f'mp_id_{id_format}', # [-1] = 'id'
					size=(15)
				),
				sg.Text('Kg')
			]
		)

	return [
		[
			sg.Frame('Data', [
				[
					sg.Text(
						today_date,
						key='-DATE-',
						size=(11)
					),
					sg.CalendarButton(
						'Alterar data', 
						key='-data_recebido-',
						target='-DATE-', 
						close_when_date_chosen=True, 
						month_names=[
							'Janeiro', 
							'Fevereiro', 
							'Março', 
							'Abril', 
							'Maio', 
							'Junho', 
							'Julho', 
							'Agosto', 
							'Setembro', 
							'Outubro', 
							'Novembro', 
							'Dezembro'
						], 
						day_abbreviations=[
							'Dom', 
							'Seg', 
							'Ter', 
							'Qua', 
							'Qui', 
							'Sex', 
							'Sáb'
						],
						format='%d/%m/%Y'
					)
				]
			]),
			sg.Frame('Nota Fiscal',[
				[sg.Input(key='-notafiscal-', size=(17))]
			])
		],
		[
			sg.Frame('Materiais a Receber',layout_receiving_mp)
		],
		[sg.Button('Confirmar Recebimento'),sg.Button('Sair/Voltar',key='Sair')]
	]

def register_buy_info(supplier_list:list, material_list:list, today_date:str):
	def __layout_receiving_mp():
		layout_receiving_mp = list()
		layout_receiving_material = list()
		layout_receiving_kgs = list()
		layout_receiving_valores = list()
		layout_receiving_previsao = list()

		layout_receiving_material.append([sg.Text('Material',font=('Helvetica', 14,'bold'))])
		layout_receiving_kgs.append([sg.Text('Quantidade',font=('Helvetica', 14,'bold'))])
		layout_receiving_valores.append([sg.Text('Valor',font=('Helvetica', 14,'bold'))])
		layout_receiving_previsao.append([sg.Text('Previsão',font=('Helvetica', 14,'bold'))])

		for material in material_list:
			__material = material[1]

			layout_receiving_material.append([sg.Text(f"{__material}")])
			layout_receiving_kgs.append([sg.Input(key=f'kg_id_{material[-1]}',size=(5)),sg.Text('Kg')])
			layout_receiving_valores.append([sg.Text('R$'),sg.Input(key=f'valor_id_{material[-1]}',size=(5))])
			layout_receiving_previsao.append([sg.Input(today_date, key=f'prev_id_{material[-1]}',size=(10))])

		layout_receiving_mp = [
			sg.Column(layout_receiving_material),
			sg.VSeperator(),
			sg.Column(layout_receiving_kgs),
			sg.VSeperator(),
			sg.Column(layout_receiving_valores),
			sg.VSeperator(),
			sg.Column(layout_receiving_previsao),
		]

		return layout_receiving_mp

	return [
		[
			sg.Frame('Informações gerais',[
				[
					sg.Frame('Data', [
						[
							sg.Input(today_date, key='-DATE-',size=(10)),
							sg.CalendarButton(
								'Alterar data',
								key='-data_recebido-',
								target='-DATE-',
								close_when_date_chosen=True,
								month_names=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
								day_abbreviations=['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
								format='%d/%m/%Y'
							)
						]
					]),
					sg.Frame('Fornecedor',[[sg.Combo(supplier_list, size=17,key='-Fonecedor-')]]),  # Fornecedor
					sg.Frame('OC',[[sg.Input(size=4,key='-OC-')]])
				]
			])
		],
		[sg.Frame('Materiais a Receber',[__layout_receiving_mp()])],
		[sg.Button('Confirmar Recebimento',key='Salvar'),sg.Button('Sair/Voltar',key='Sair')]
	]

def edit_multiples_lines():
	return [
		[sg.Text('Editar múltiplas linhas ao mesmo tempo')],

    	[sg.CalendarButton(
			'Data', 
			target='-DATE-', 
			close_when_date_chosen=True, 
			month_names=[
				'Janeiro', 
				'Fevereiro', 
				'Março', 
				'Abril', 
				'Maio', 
				'Junho', 
				'Julho', 
				'Agosto', 
				'Setembro', 
				'Outubro', 
				'Novembro', 
				'Dezembro'], 
			day_abbreviations=[
				'Dom', 
				'Seg', 
				'Ter', 
				'Qua', 
				'Qui', 
				'Sex', 
				'Sáb'],
			format='%d/%m/%Y')
		, sg.InputText(key='-DATE-',size=(11))],

		[sg.Checkbox('Urgente', key='-popurgente-', default=False),sg.Push()],

		[
			sg.Button('Excluir linhas selecionadas',key='-exclude_lines-'), 
			sg.Button('Marcar como recebido',key='-receve_lines-')
		],
		[sg.Button('Salvar'),sg.Button('Sair/Voltar', key='Sair')]
	]

def filterpopup() -> list:
	return [
		[
			sg.Radio("Bitola", '_filtro', key='radio_filtro_bitola'), 
			sg.Radio("Norma", '_filtro', key='radio_filtro_norma'), 
			sg.Radio("Dimensão", '_filtro', key='radio_filtro_Dimensao'), 
			sg.Radio("documento", '_filtro', key='radio_filtro_documento'),
			sg.Radio('Ordem de Compra', '_filtro', key='radio_filtro_oc', default=True)
		],
		[sg.Text('Valor para encontrar: '), sg.Input(key='filtro_valor', size=(20))],
		[sg.Button('Filtrar'),sg.Button('Sair/Voltar', key="Sair")]]

def set_setings(button_color, pressed_button_color, second_color, text_color, font, font_size):
	set_setings = [
		[sg.Frame('Tema/Cores',[
			[
				sg.Text('Temas Padrões'),sg.Push(), 
				sg.Combo(
					["Tema Claro","Tema Escuro","Tema Azul","Tema Verde","Tema Cinza"],
					size=(20),
					enable_events=True,
					key='-combo_themes-'
				)
			],
			[
				sg.Text(f'Cor dos Botões'),sg.Push(),
				sg.Button(
					button_color,
					key='color_change_button',
					button_color=button_color
				)
			],
			[
				sg.Text(f'Cor dos Botões apertado'),sg.Push(),
				sg.Button(
					pressed_button_color,
					key='color_change_button_pressed',
					button_color=pressed_button_color
				)
			],
			[
				sg.Text(f'Cor Secundaria'),sg.Push(),
				sg.Button(
					second_color,
					key='color_change_second',
					button_color=second_color
				)
			],
			[
				sg.Text(f'Cor do Texto'),sg.Push(),
				sg.Button(
					text_color,
					key='color_change_text',
					button_color=text_color
				)
			]
		])],
		[sg.Frame('Fonte e tamanho',[
			[
				sg.Text('Fonte'),sg.Push(), 
				sg.Combo(["Arial","Times New Roman","Calibri","Helvetica","Verdana"], key='combo_font', size=(20), default_value=font)
			],
			[
				sg.Text('Tamanho'),sg.Push(), 
				sg.Slider(range=(6,14), orientation='h', s=(15,10), default_value=int(font_size), key='-font_size-')
			]
		])],
		[sg.Frame('Salvar/Editar',[
			[sg.Button("Salvar"), sg.Button('Sair'), sg.Push()]
		])]
	]

	return set_setings

def create_dashbord():
	return [
		[sg.Text('Plot test')],
		[sg.Canvas(key='-CANVAS-')],
		[sg.Button('Ok')]]
#____________login____________________________________________________________________________

def layout_login():
	layout_login = [
			[sg.Text('STOCKBUYREP', font=('Roboto Condensed', 20, 'bold'))],
			[sg.Text('Sistema de pedidos para compra\n')],
			[sg.Text('Usuario: '), sg.Input(key='usuario', size=20, tooltip="Seu usuario é seu nome"), sg.Push()],
			[
				sg.Text('Senha:   '), 
				sg.Input(key='senha', password_char='*', size=20, tooltip="Sua senha é *****"), sg.Push()
			],
			[sg.Button('Confirmar'), sg.Push(),sg.Button('Novo Cadastro'), sg.Button('Sair')]]
	return layout_login
#____________Area de forjados________________________________________________________________________________
def layout_joelhos():
	layout_joelhos = [
		[sg.Frame('Joelhos', [
			[sg.Text('JL2'), sg.Push(), sg.Text(key='jl2_result', size=20)],
			[sg.Text('JL3'), sg.Push(), sg.Text(key='jl3_result', size=20)],
			[sg.Text('JL4'), sg.Push(), sg.Text(key='jl4_result', size=20)],
			[sg.Text('JL5'), sg.Push(), sg.Text(key='jl5_result', size=20)],
			[sg.Text('JL6 Flange'), sg.Push(), sg.Text(key='jl6flange_result', size=20)]
		])]]
	return layout_joelhos

def layout_tee():
	layout_tee = [
		[sg.Frame('TEE', [
			[sg.Text('TEE2'), sg.Push(), sg.Text(key='tee2_result', size=20)],
			[sg.Text('TEE3'), sg.Push(), sg.Text(key='tee3_result', size=20)],
			[sg.Text('TEE5'), sg.Push(), sg.Text(key='tee5_result', size=20)],
			[sg.Text('TEE CH36'), sg.Push(), sg.Text(key='teech36_result', size=20)]
		])]]
	return layout_tee

def layout_cz():
	layout_cz = [
		[sg.Frame('Cruzetas', [
			[sg.Text('CZ4'), sg.Push(), sg.Text(key='cz4_result', size=20)],
			[sg.Text('CZ6'), sg.Push(), sg.Text(key='cz6_result', size=20)]
		])]]
	return layout_cz

#____________Calculadora________________________________________________________________________________

def layout_peso_metro(button_color:str='#4d4d94', pressed_button_color:str="lightblue"):
	layout_peso_metro = [
		[
			sg.Radio('Aço/Inox', 'botoes_material', default=True, key='radio_material_1'), 
			sg.Radio('Latão', 'botoes_material', key='radio_material_2'), 
			sg.Radio('Aluminio', 'botoes_material', key='radio_material_3')
		],
		
		[sg.Frame('Redondo', [
			[
				sg.Button(key='botao_red',
					image_filename=(Path(__file__).parent.parent / 'resources\\round.png'), 
					image_size=(64,64), 
					image_subsample=2, 
					button_color=button_color, 
					mouseover_colors=pressed_button_color), 
					sg.Input(size=(16), 
					key='valor_red'
				),
				sg.Text(key='kg_m_red', size=10)
			],
			[sg.Text(size=8), sg.Text('Bitola'), sg.Push(),sg.Text('Kg/Metro')]
		])],

		[sg.Frame('Sextavado', [
			[
				sg.Button(
					key='botao_sext', 
					image_filename=(Path(__file__).parent.parent / 'resources\\hexagon.png'),
					image_size=(64,64), 
					image_subsample=2, 
					button_color=button_color, 
					mouseover_colors=pressed_button_color
				), 
				sg.Input(size=(16), key='valor_sext'),
				sg.Text(key='kg_m_sext', size=10)
			],
		[sg.Text(size=8), sg.Text('Bitola'), sg.Push(),sg.Text('Kg/Metro')]
		])],

		[sg.Frame('Quadrado', [
			[
				sg.Button(
					key='botao_quad', 
					image_filename=(Path(__file__).parent.parent / 'resources\\square.png'), 
					image_size=(64,64), 
					image_subsample=2, 
					button_color=button_color, 
					mouseover_colors=pressed_button_color
				), 
				sg.Input(size=(7), key='valor_quad1'), 
				sg.Input(size=(7), key='valor_quad2'),
				sg.Text(key='kg_m_quad', size=10)
			],
		[
			sg.Text(size=8), 
			sg.Text('Base'), 
			sg.Text('     Altura'), sg.Push(),
			sg.Text('Kg/Metro')]])],
		
		[sg.Frame('Tubos', [
			[
				sg.Button(
					key='botao_tubo', 
					image_filename=(Path(__file__).parent.parent / 'resources\\pipe.png'), 
					image_size=(64,64), 
					image_subsample=2, 
					button_color=button_color, 
					mouseover_colors=pressed_button_color
				), 
				sg.Input(
					size=(7), 
					key='valor_tubo_maior'
					), 
				sg.Input(size=(7), key='valor_tubo_menor'),
				sg.Text(key='kg_m_tubo', size=10)
			],
			[
				sg.Text(size=8), sg.Text('Ø Maior'), sg.Text('Ø Menor'), sg.Push(),sg.Text('Kg/Metro')
			]
		])]
	]
	return layout_peso_metro

def layout_forjados():
	layout_forjados = [
		[
			sg.Input(size=10, key='valor_calculo_forjados'), 
			sg.Button('Calcular kg', key='calcular_kg'), 
			sg.Button('Calcular quantidade', key='calcular_quantidade')
		],
		[Collapsible(layout_joelhos(), 'area_jl',  'Joelhos', collapsed=True)],
		[Collapsible(layout_tee(), 'area_tee',  'TEEs', collapsed=True)],
		[Collapsible(layout_cz(), 'area_cz',  'Cruzetas', collapsed=True)],]
	return layout_forjados

def layout_conversor_mm_pol():
	layout_conversor_mm_pol = [
		[sg.Frame('mm para polegada', [
			[sg.Text('Digite um valor em mm para converter para pol:')],
			[
				sg.Text('Valor: '), 
				sg.Input(key='valor_mm_pol', size=10), 
				sg.Button('Calcular', key='calcular_mm_pol')
			],
			[sg.Text('Resposta: '), sg.Text(key='resposta_mm_pol')]])],
		[sg.Frame('pol para mm', [
			[sg.Text('Digite um valor em pol para converter para mm:')],
			[
				sg.Text('Valor: '), 
				sg.Input(key='valor_pol_mm',size=10), 
				sg.Button('Calcular', key='calcular_pol_mm')
			],
			[sg.Text('Resposta: '), sg.Text(key='resposta_pol_mm')]])]]
	return layout_conversor_mm_pol

def layout_calculdora(button_color:str='#4d4d94', pressed_button_color:str="lightblue"):
	layout_calculdora = sg.Frame('Calculadora', [
		[sg.TabGroup([
			[sg.Tab('Peso/Metro', layout_peso_metro(button_color, pressed_button_color))],
			[sg.Tab('Forjados', layout_forjados())],
			[sg.Tab('conversor mm/Pol', layout_conversor_mm_pol())]
		])]
	], visible = False, key='-frame_calculadora-')
	return layout_calculdora

#____________DaviK____________________________________________________________________________
def layout_davik_relatorio(report_data:list, color_list:list, name:str, user_pc:str, 
gauge_list:list, material_list:list, standards_list:list, button_color:str='#4d4d94', 
pressed_button_color:str="lightblue", text_color:str="white", 
second_color:str="Lightslategray") -> list:
	return sg.Frame('Relatorio', [
		[template_menu()],

		[
			sg.Frame('Bitola',[[sg.Combo(gauge_list, size=7, key='-bitola-')]]),
			sg.Frame('Material',[[sg.Combo(material_list, size=7, key='-material-')]]),
			sg.Frame('Norma',[[sg.Combo(standards_list, size=5, key='-norma-')]]),
			sg.Frame('Dimensão',[[sg.Input(size=9, key='-dimensao-')]]),
			sg.Frame('Quantidade(mm)',[[sg.Input(size=13, key='-quantidade-')]]),
			sg.Frame('Proc. Fabricação',[
				[sg.Combo(
					['Trefilado','Laminado','Fresado','Retificado','Descascado','Torneado','FORJADO'], 
					size=13, 
					key='-pfabricacao-'
				)]
			]),

			sg.Button(
				key='-register-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\add.png') , 
				image_size=(16,16), 
				image_subsample=8, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Registar material"
			)
		],

		[sg.Table(  
			#display_row_numbers=True, 
			expand_y = True,
			right_click_menu=['Click',['Editar',"Excluir",'Informações','Confirmar Recebimento']],
			justification='left', 
			header_background_color=button_color, 
			header_text_color=text_color, 
			alternating_row_color=second_color, 
			enable_events=True, 
			key='-tabela_main-', 
			enable_click_events=True, 
			size=(300,25), 
			values=report_data, 
			auto_size_columns=True,
			headings=['Solicitado','Bitola','Material','Norma','Dimensão','Fabricação','Quilos'],
			row_colors=color_list
		)],
		[
			# sg.Button(key='-search_item-', image_filename=(Path(__file__).parent.parent / 'resources\\search.png') , image_size=(32,32), image_subsample=4, button_color=button_color, mouseover_colors=pressed_button_color, tooltip="Localizar item"), 
			# sg.Button(key='-refresh_report-', image_filename=(Path(__file__).parent.parent / 'resources\\refresh.png') , image_size=(32,32), image_subsample=4, button_color=button_color, mouseover_colors=pressed_button_color, tooltip="Atalizar relatorio"), 
			sg.Button(
				key='-dashbord-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\chart-mixed.png') , 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Dashbord de necessidade de material"
			), 
			sg.Button(
				key='-make_excel_report-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\file-excel.png') , 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Salvar Relatorio em Excel"
			),
			sg.Button(
				key='-save_backup-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\diskette.png') , 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Salvar Backup"
			),
			sg.Push(), 
			sg.Button(
				key='-info-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\info.png') , 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Informações"
			), 
			sg.Button(
				key='-debug-', 
				image_filename=(Path(__file__).parent.parent / 'resources\\code.png') , 
				image_size=(32,32), 
				image_subsample=4, 
				button_color=button_color, 
				mouseover_colors=pressed_button_color, 
				tooltip="Habilitar console de Debug"
			)
		],
		[
			sg.Text(f'Usuario:{name} -  Maquina:{user_pc}'),
			sg.Push(),sg.Text(key='debug_status'), 
			sg.Sizegrip()
		]
	], expand_y = True)
#____________Konemetal____________________________________________________________________________

def tabs_konemetal(report_data:list, extra_mp_report_data:list, color_list:list, 
name:str, user_pc:str, gauge_list:list, material_list:list, standards_list:list, 
button_color:str='#4d4d94', pressed_button_color:str="lightblue", text_color:str="white", 
second_color:str="Lightslategray") -> list:
	return sg.TabGroup([
		[sg.Tab('Materia Prima',[		
			[sg.Table( 
				#display_row_numbers=True, 
				expand_y = True,
				expand_x = True,
				right_click_menu=['Click',['Editar',"Excluir",'Informações','Confirmar Recebimento']],
				justification='left', 
				header_background_color=button_color, 
				header_text_color=text_color, 
				alternating_row_color=second_color, 
				select_mode='extended',
				enable_events=True, 
				key='-tabela_main-', 
				enable_click_events=True, 
				size=(120,25), 
				values=report_data, 
				headings=['Bitola','Material','Norma','dimensão','Fabricação','Kg','Documento','Data entrega'],
				row_colors=color_list
			)]
		])],
		[sg.Tab('Carteira Ativa',[
			[sg.Table(
				alternating_row_color=second_color, 
				header_background_color=button_color, 
				header_text_color=text_color, 
				size=(120,25), 
				headings=['Cliente', 'OI', 'N° Pedido', 'Linha', 'Código', 'Quantidade', 'Entregues', 'Data Entrega', 'Valor'],
				right_click_menu=['Click',['Apagar Linha']],
				values=extra_mp_report_data,
				key='-tabela_kone_extra_mp-', 
				# enable_click_events=True, 
				# enable_events=True, 
				select_mode='extended',
			)]
		])],
	])

def layout_konemetal_relatorio(report_data:list, extra_mp_report_data:list, 
color_list:list, name:str, user_pc:str, gauge_list:list, material_list:list, 
standards_list:list, today_date:str, button_color:str='#4d4d94', 
pressed_button_color:str="lightblue", text_color:str="white", 
second_color:str="Lightslategray") -> list:
	layout_konemetal_relatorio = sg.Frame('Relatorio', [
		[template_menu()],
		template_buttons(gauge_list, material_list, standards_list, today_date, button_color, pressed_button_color),
		[tabs_konemetal(
			report_data=report_data,
			extra_mp_report_data=extra_mp_report_data,
		 	color_list=color_list,
			name=name,
			user_pc=user_pc,
			gauge_list=gauge_list,
			material_list=material_list,
			standards_list=standards_list,
			button_color=button_color,
			pressed_button_color=pressed_button_color,
			text_color=text_color,
			second_color=second_color	
		)],
				[sg.Text(
			f'Usuario:{name} -  Maquina:{user_pc}'),
			sg.Push(),
			sg.Text(key='debug_status'),
			sg.Sizegrip()]

		],
		expand_y = True)
	return layout_konemetal_relatorio
#____________layouts finais____________________________________________________________________________

def layout_konemetal(report_data:list, extra_mp_report_data:list, color_list:list, name:str, user_pc:str, 
gauge_list:list, material_list:list, standards_list:list, today_date:str, 
button_color:str='#4d4d94', pressed_button_color:str="lightblue", text_color:str="white", 
second_color:str="Lightslategray"):
	layout_konemetal = [[
		layout_konemetal_relatorio(
			report_data,
			extra_mp_report_data,
			color_list,
			name,
			user_pc,
			gauge_list, 
			material_list, 
			standards_list, 
			today_date, 
			button_color, 
			pressed_button_color, 
			text_color,
			second_color
		), 
		layout_calculdora(
			button_color, 
			pressed_button_color
		)
	]]
	return layout_konemetal

def layout_davik(report_data:list, color_list:list, name:str, user_pc:str, 
gauge_list:list, material_list:list, standards_list:list, button_color:str='#4d4d94', 
pressed_button_color:str="lightblue", text_color:str="white", 
second_color:str="Lightslategray") -> list():
	return [
		[
			layout_davik_relatorio(
				report_data,
				color_list,
				name,
				user_pc,
				gauge_list,
				material_list,
				standards_list,
				button_color,
				pressed_button_color,
				text_color,
				second_color
			), 
		layout_calculdora(
			button_color, 
			pressed_button_color
			)
		]
	]

def layout_material_comprado(report_data:list, color_list:list):
	layout_material_comprado = [[sg.Column([[sg.Frame('Relatorio', [
		[template_menu()],
		[sg.Button(
			key='-search_item-', 
			image_filename=(Path(__file__).parent.parent / 'resources\\search.png'), 
			image_size=(32,32), 
			image_subsample=4, 
			tooltip="Localizar item"),
		sg.Button(
			key='-refresh_report-', 
			image_filename=(Path(__file__).parent.parent / 'resources\\refresh.png'), 
			image_size=(32,32), 
			image_subsample=4, 
			# button_color=button_color, 
			# mouseover_colors=pressed_button_color, 
			tooltip="Atalizar relatorio"), 
		],
		[sg.Table(
			size=(25,30),
			expand_y = True,
			# display_row_numbers=True,
			justification='left', 
			header_background_color='#4c4c61', 
			right_click_menu=['Click',['Informações', 'Editar Compra', 'Registrar Compra', 'Cancelar Compra']],
			select_mode='extended',
			header_text_color='#FEFFFE', 
			alternating_row_color='#778899', 
			enable_events=True, 
			key='-tabela_main-', 
			# right_click_selects=True,
			enable_click_events=True, 
			values=report_data,
			headings=['Solicitante','Material','Quilos','Data','Valor','Data Entrega'],
			row_colors=color_list
		)],
		[sg.Sizegrip()]
	])]]),sg.Column([[layout_calculdora('blue','blue')]])]]
	return layout_material_comprado

def layout_viewer():
	viewer_col_left = [
    	[sg.Frame('Escolher empresa',[
			[sg.Checkbox('Davik',default=True, key='check_davik', enable_events=True)],
			[sg.Checkbox('Konemetal',default=True, key='check_kone', enable_events=True)]
		])]
	]

	viewer_col_right = [
		[sg.TabGroup([
			[sg.Tab('Graficos',[
				[sg.Frame('Graficos',[
					[sg.Canvas(key='-graph_row1-')],
					[sg.Canvas(key='-graph_row2-')]
				], size=(500,500))]
			])],

			[sg.Tab('Necessidades',[
				[sg.Frame('Relatório',[
					[sg.Text('Relatorio', key='-report_title-')],
					[sg.Table(
						display_row_numbers=True, 
						expand_y = True,
						justification='left', 
						# header_background_color=davik.button_color, 
						# header_text_color=davik.text_color, 
						# alternating_row_color=davik.second_color, 
						# enable_events=True, 
						key='-tabela_davik-', 
						# enable_click_events=True, 
						size=(100,25), 
						values=compras.makeGeneralReport('view_table'),
						# row_colors=davik.coloringRows(davik.text_color, davik.second_color),
						headings=['Material','Dimensão','Quilos']
					)]
				])]
			])],

			[sg.Tab('Últimos valores',[
				[sg.Frame('Ultimos valores',[
					[sg.Text('Ultimos valores pagos pelos materiais',key='-last_value_title-')],
					[sg.Table(
						headings=['Bitola','Valor medio','Ultimo Valor','Fornecedor','OC','Data'],
						values=[[0,0,0,0,0,0]]
					)]])]
			])]
		])]
	]

	return [[sg.Col(viewer_col_left),sg.Col(viewer_col_right)]]

def item_infos(material:dict, area:str, comprado:bool=False) -> list:

	solicitado = [
		[sg.Text(f'Bitola: {material["Bitola"].capitalize()}')],
		[sg.Text(f'Material: {material["Material"].capitalize()}')],
		[sg.Text(f'Norma: {material["Norma"]}')],
		[sg.Text(f'Dimensão: {material["Dimensao"]}')],
		[sg.Text(f'Milimetros: {material["Milimetros"]}mm')], ###
		[sg.Text(f'Fabricação: {material["Fabricacao"].capitalize()}')],
		[sg.Text(f'Quilos: {material["Kg_Solicitado"]}kg')],
		[sg.Text(f'Data: {material["Data_Solicitado"]}')]
	]

	outras_infos = [
		[
			sg.Text(f'Urgente: {"Sim" if material["Urgente"] else "Não"}'), 
			sg.Text(f'Comprado: {"Sim" if material["Comprado"] else "Não"}')
		],
		[sg.Text(f'Solicitado por: {material["Solicitado_por"]}')],
		[sg.Text(f'Id: {material["id"]}',font=('Arial Bold', 18))]
	]
	
	if area == 'Konemetal':
		outras_infos.insert(0, [sg.Text(f'Material para peça: {material["Codigo_Peca"]}')])
		outras_infos.insert(1, [sg.Text(f'Data de entrega da peça: {(material["Data_Entrega_Peca"])}')])
		outras_infos.insert(2, [sg.Text(f'Documento: {material["Documento"]}')])
	
	if comprado:
		solicitado.pop(4)
		outras_infos.pop(0)

	layout = [
		[
			sg.Frame('Solicitado',solicitado),
			sg.Frame('Informações de Compra',[
				[sg.Text(f'Fornecedor: {material["Fornecedor"].capitalize() if material["Fornecedor"] else "Não Comprado ainda"}')],
				[sg.Text(f'Valor/Quilo: R$ {material["Valor"] if material["Valor"] else "Não Comprado ainda"}')],
				[sg.Text(f'Quilos comprados: {material["Kg_Comprado"] if material["Kg_Comprado"] else "Não Comprado ainda"} Kg')],
				[sg.Text(f'Data de Compra: {material["Data_Comprado"] if material["Data_Comprado"] else "Não Comprado ainda"}')],
				[sg.Text(f'Previsao de chegada: {material["Data_Previsao"] if material["Data_Previsao"] else "Sem previsão"}')],
				[sg.Text(f'Ordem de Compra: {material["Ordem_Compra"] if material["Ordem_Compra"] else "Não Comprado ainda"}')],
			], visible=(True if material["Fornecedor"] else False))
		],
		[
			sg.Frame('Informações Recebimento',[
				[sg.Text(f"Kg Recebido: {material['Kg_Recebido'] if material['Kg_Recebido'] else ''}")],
				[sg.Text(f"Data Recebido: {material['Data_Recebido'] if material['Data_Recebido'] else ''}")],
				[sg.Text(f"Nota Fiscal: {material['Nota_Fiscal'] if material['Nota_Fiscal'] else ''}")]
			], visible=(True if material['Kg_Recebido'] else False))
		],
		[sg.Frame('Outras Informações',outras_infos)],
		[sg.Button('Sair')]
	]

	return layout

def register_standards(values:list, area:str):
	layout = [
		[sg.Frame(f'Cadastro de {area}', [
			[
				sg.Frame('Norma Interna', [
					[sg.Input(size=10, key='-internal_std-')]
				]), 
				sg.Frame('Norma Mercado', [
					[sg.Input(size=10, key='-market_std-')]
				]),
				sg.Button('Cadastrar')
			]
		])],
		[sg.Frame('Normas Salvas', [
			[sg.Table(
				headings=['Norma Interna','Norma Mercado'],
				values=values,
				justification='left',
				key='-std_table-'
			)]
		])]
	]

	return layout

def supplier_config(supplier_list:list=[], bitola_list:list=[], norma_list:list=[], fabricacao_list:str=[]):
	def _column(area:str, values:list):
		return [[sg.Frame(f'{area}',[
			[sg.Frame('Adicionar/Editar',[[sg.Input(size=7,key=f'add-{area}_parameter'),sg.Button('Add',key=f'add-{area}')]])],
			[sg.Listbox(values=values, size=(12,10), key=f'-{area}_list-')]
		])]]

	return [
		[sg.Col([
			[sg.Text('Selecione a Empresa'), sg.Combo(supplier_list, enable_events=True, key='-sup_selector-')],
			[sg.Button('Salvar alterações'), sg.Button('Sair sem salvar')],
			[sg.Frame('Informações',[
				[sg.Frame('Empresa',[[sg.Input(size=15,key='-empresa-')]])],
				[sg.Frame('Vendedor',[[sg.Input(size=16, key='-vendedor-')]])],
				[sg.Frame('E-mail',[[sg.Input(size=35, key='-email-')]])]
			])]
		]),
		sg.Col([[sg.Frame('Frete',[
			[sg.Checkbox('Entrega aqui na região',key='-entrega-')],
			[sg.Frame('Minimo por Kg',[[sg.Input(size=15, key='-min_kg-')]])], 
			[sg.Frame('Minimo por valor',[[sg.Input(size=15, key='-min_val-')]])],
			[sg.Frame('Minimo por item',[[sg.Input(size=15, key='-min_item-')]])],
			[sg.Frame('Taxa',[[sg.Input(size=15, key='-tax-')]])]
		])]])],
		[sg.Frame('Materiais',[
			[sg.Text('Itens adicionados serão salvos altomaticamente, para excluir falar com o Leo.')],
			[
				sg.Col(_column(area='Bitola',values=bitola_list)), 
				sg.Col(_column(area='Norma',values=norma_list)),
				sg.Col(_column(area='Fabricação',values=fabricacao_list))
			]
		])]
	]

def add_pedido():
	return [
		[sg.Button(
			key='-date-', 
			image_filename=(Path(__file__).parent.parent / 'resources\\calendar-clock.png'), 
			image_size=(32,32), 
			image_subsample=0, 
			# button_color=button_color, 
			# mouseover_colors=pressed_button_color, 
			tooltip="Alterar todas as datas"),
		sg.Button(
			key='-save-', 
			image_filename=(Path(__file__).parent.parent / 'resources\\diskette.png'), 
			image_size=(32,32), 
			image_subsample=4, 
			# button_color=button_color, 
			# mouseover_colors=pressed_button_color, 
			tooltip="Salvar Materiais"),
		sg.Button(
			key='-new_line-', 
			image_filename=(Path(__file__).parent.parent / 'resources\\add.png'), 
			image_size=(16,16), 
			image_subsample=8, 
			# button_color=button_color, 
			# mouseover_colors=pressed_button_color, 
			tooltip="Registar material"
			),
			######### ADD EXCLUDE MP
		],
		[sg.HorizontalSeparator()],
		[sg.Frame('Linhas',[
			[
				sg.Frame('Bitola',[[sg.Input(size=4)]]),
				sg.Frame('Material',[[sg.Input(size=6)]]), 
				sg.Frame('Norma',[[sg.Input(size=4)]]), 
				sg.Frame('Dimensão',[[sg.Input(size=10)]]),
				sg.Frame('Comprimento',[[sg.Input(size=10)]]),
				sg.Frame('Fabricação',[[sg.Input(size=10)]]),
				sg.Frame('Data Entrega',[[sg.Input(size=10)]]),
				sg.Frame('Documento',[[sg.Input(size=10)]])
			]
		],key='linhas_frame')]
	]

if __name__ == '__main__':  # apenas para visualizar o layout
	window = sg.Window(
		'StockBuyRep', 
		layout_konemetal(), 
		resizable=True
	)

	while True:
		event, values = window.read()
		print('\n\neventos:',event, '\n\nValores:',values)
		if event == sg.WIN_CLOSED:
			break
			window.close()
		elif event == '-new_line-':
			window.extend_layout(window['linhas_frame'], [[sg.Frame('Linha',[[sg.Input(size=3)]]),sg.Frame('Produto',[[sg.Input(size=15)]]), sg.Frame('Descrição',[[sg.Input(size=15)]]), sg.Frame('Quantidade',[[sg.Input(size=10)]]),sg.Frame('Data Entrega',[[sg.Input(size=10)]])]])

		else:
			...

	# importing_preferences('')
