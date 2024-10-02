Bitola= dict(
    S = "SEXTAVADO",  # OK
    R = "REDONDO", # OK
    Q = "QUADRADO", # OK
    # JL = "JOELHO 90\u00b0",
    # TL = "TEE",
    # K = "FORJADO 45\u00b0",
    # CZ = "CRUZETA",
    # A = "ANEL",
    TN = "TUBO SEM COSTURA",
    TC = "TUBO COM COSTURA",
    TB = "TUBO MECÂNICO",
    TNR = "TUBO COM COSTURA REMOVIDA",
    CH = "CHAPA",
    BC = "BARRA CHATA",
    # JC = "JOELHO LONGO 90\u00b0",
    # JM = "JOELHO ORIENT\u00c1VEL",
    # FLANGE = "FLANGE"
)
Material= dict(
    A= ("A\u00c7O", 7.85),
    B= ("COBRE", 8.96),
    C= ("LAT\u00c3O", 8.55),
    D= ("BRONZE GRAFITADO", 7.8),
    F= ("FERRO FUNDIDO", 7.3),
    I= ("INOX", 7.8),
    L= ("ALUM\u00cdNIO", 2.7),
    M= ("POLIACETAL", 1.42),
    N= ("NYLON", 1.15),
    P= ("ACR\u00cdLICO", 1.18),
    T= ("TEFLON", 2.2)
)
Norma= dict(
    # Site encontrei alguns dos pesos, o resto foi no chatgptola
    # https://compraco.com.br/blogs/especificacoes-do-aco/aco-sae-aisi-5160-propriedades-de-aco-de-mola-5160-com-alto-teor-de-carbono-composicao?srsltid=AfmBOooSUiMgWdTkZJ-cxrTLpCDvkA8Q3HWz_GSlHDDD05qdZU3p15-b
    A= ("DIN 11SMN37", 8.1),
    B= ("DIN 12L14", 7.87),
    C= ("DIN 11SMN30", 7.85),
    D= ("SAE 1045", 7.85),
    E= ("ASTM A182f11", 7.9),
    F= ("DIN 316", 8.03),
    G= ("SAE 1020", 7.87),
    H= ("CA 377", 8.0),
    I= ("SAE 1010", 7.87),
    J= ("CA 360", 8.5),
    K= ("SAE 841", 8.5),
    L= ("DIN 304", 7.93),
    M= ("ASTM 564", 8.9),
    N= ("ASTM 630", 7,75),
    O= ("ASTM 17-4PH", 7.75),
    P= ("SAE 1215", 7.87),
    Q= ("6351 T6", 2.7),
    R= ("SAE 4140", 7.85),
    S= ("C 110 ELETROL\u00cdTICO", 8.96),
    T= ("H13", 7.76),
    U= ("SAE 5160", 7.8),
    V= ("NAVAL", 0),
    W= ("DIN 20MNCR5", 7.85),
    X= ("DIN ST52.3", 7.85),
    Y= ("NYLON 6.0",1.14),
    Z= ("ASTM A36", 7.85),
    AA= ("SAE 8640", 7.85),
    AB= ("LNE 380", 2.8),
    AC= ("SAE 8620", 7.85),
    AD= ("VW3", 1.15),
    AE= ("TM23", 0),
    AF= ("PTFE", 2.2),
    AG= ("POLIACETAL", 1.41),
    AH= ("VC 131", 8.96),
    AI= ("ASTM A182 F22", 7.9),
    AJ= ("DIN 310", 7.9),
    AK= ("FC 300", 7.15),
    AL= ("NBR 5590", 7.85),
    AM= ("AISIO1 (VND)", 2.7),
    AN= ("FERRO FUNDIDO NODULAR", 7.15),
    LL= ("DIN 304L",7.9),
    FL= ("DIN 316L", 7.9)
)
Fabricacao= [
    "RETIFICADO",
    "LAMINADO",
    "TREFILADO",
    "FORJADO",
    "DESCASCADO",
    "EXTRUSADO",
    "OXICORTE"  
    ]


from math import sqrt
from math import pow
from math import pi

def merge(*args):
    try:
        if len(args) == 1:
            value = args[0]
            return value
        elif len(args) == 2:
            value = args[0] + args[1]
            return value
        elif len(args) == 3:
            value = args[0] + args[1] + args[2]
            return value
    except ValueError as err:
        print(f'Informe um valor valido. O erro que foi feito é {err}')


def inch_to_meters(*args):
    for item in inch_or_cm:
        if item == '/' or item == '-':    
            if len(args) == 2:
                res = 25.4 * args[0] / args[1]
                return f'{round(res, 2)}mm'
            elif len(args) == 3:
                res = args[1] * 25.4 + 25.4 * args[1] / args[2]
                return f'{round(res, 2)}mm'
            elif len(args) == 4:
                res = 25.4 * args[0] / args[1] + 25.4 * args[2] / args[3]
                return f'{round(res, 2)}mm'
        elif item == '"' or item == "'":
            res = round(25.4 * float(args[0]), 2)
            return f'{res}mm'
        else:
            if item == 'm':
                return f'O valor ja esta em milimetros.'
                

def bitola(tipo):
    return Bitola.get(f'{tipo}', "Bitola não encontrada.")


def material(tipo):
    return f'{Material.get(tipo, "Material não encontrada.")[0]}'


def norma(tipo):
    return Norma.get(f'{tipo}', "Norma não encontrada.")


def fabricacao(tipo):
    if tipo in Fabricacao:
        return f'{tipo}'
    return 'Fabricação não encontrada.'


def inch_weight_mesure(mesure):
    weight = Norma.get(f'{peso}')
    part = ' '.join(medida[1])
    part = part.split()
    mm = [num for num in part if num in '0123456789'] 
    mm = float(mm[0] + mm[1] + mm[2])
    mm /= 100
    if Bitola.get(bit) == 'REDONDO':
        return f'{round(pi * pow(mm / 2, 2) * mesure * weight[1]/ 10, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'QUADRADO':
        return f'{round((pow(mm) * mesure * weight[1])/10, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'SEXTAVADO':
        return f'{round((((3 * sqrt(3) / 2 * ((mm / sqrt(3))**2)) * mesure) * weight[1])/ 10, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'TUBO SEM COSTURA' or Bitola.get(bit) == 'TUBO COM COSTURA' or Bitola.get(bit) == 'TUBO MECÂNICO' or Bitola.get(bit) ==  'TUBO COM COSTURA REMOVIDA':
        diam_inter = float(input(f'Digite o diametro interno do {Bitola.get(bit)}: '))
        diam_exter = float(input(f'Digite o dimetro externo do {Bitola.get(bit)}: '))
        parametros.append(f'Diametro interno: {diam_inter}mm -- Diametro externo: {diam_exter}mm')
        diam_inter = pi * pow(diam_inter / 2, 2) * mesure * weight[1]/ 10
        diam_inter = pi * pow(diam_exter / 2, 2) * mesure * weight[1]/ 10
        if diam_exter > diam_inter:
            return f'{round(diam_exter - diam_inter, 3)}Kg', f'{mesure * 1000}mm' 
        else:
            return f'{round(diam_inter - diam_exter, 3)}Kg', f'{mesure * 1000}mm'


def milimeters_weight_mesure(mesure):
    weight = Norma.get(f'{peso}')
    Norma.get(f'{peso}')
    part = ' '.join(medida[0])
    part = part.split()
    mm = [num for num in part if num in '0123456789']
    num = float(merge(*mm))
    if Bitola.get(bit) == 'REDONDO':
        return f'{round(pi * pow(num / 2, 2) * mesure * weight[1]/ 1000, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'QUADRADO':
        return f'{round((pow(num) * mesure * weight[1])/1000, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'SEXTAVADO':
        return f'{round((((3 * sqrt(3) / 2 * ((num / sqrt(3))**2)) * mesure) * weight[1])/ 1000, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'TUBO SEM COSTURA' or Bitola.get(bit) == 'TUBO COM COSTURA' or Bitola.get(bit) == 'TUBO MECÂNICO' or Bitola.get(bit) ==  'TUBO COM COSTURA REMOVIDA':
        diam_inter = float(input(f'Digite o diametro interno do {Bitola.get(bit)}: '))
        diam_exter = float(input(f'Digite o dimetro externo do {Bitola.get(bit)}: '))
        parametros.append(f'Diametro interno: {diam_inter}mm -- Diametro externo: {diam_exter}mm')
        diam_inter = pi * pow(diam_inter / 2, 2) * mesure * weight[1]/ 1000
        diam_inter = pi * pow(diam_exter / 2, 2) * mesure * weight[1]/ 1000
        if diam_exter > diam_inter:
            return f'{round(diam_exter - diam_inter, 3)}Kg', f'{mesure * 1000}mm' 
        else:
            return f'{round(diam_inter - diam_exter, 3)}Kg', f'{mesure * 1000}mm'


parametros = []
bit = input('Bitola: ').upper()
parametros.append(f'{bitola(tipo= bit)}')
parametros.append(f'{material(tipo= input("Material: ").upper()) }')
peso = input("Norma: ").upper()
parametros.append(f'{norma(tipo= peso)} ')
parametros.append(f'{fabricacao(tipo= input('Fabricação: ').upper())} ')

inch_or_cm = []
inch = input(f'Digite o diametro do/a {Bitola.get(bit)}: (ex: 3-3/4 ou 3" ou 56mm) ')
inch_or_cm.extend(inch)
for item in inch_or_cm:
    if item == 'm':
        inch_or_cm.pop()
    if item == '"' or item == "'": # <- Polegada inteira
        medida = [inch]
        value = [num for num in inch if num in '0123456789']
        number = []
        number.append((merge(*value)))
        medida.append(inch_to_meters(*number))
        parametros.append(f'{inch_weight_mesure(mesure= float(input('Tamanho: ')))}')
        parametros.append(medida[:])
    elif item == '/' or item == '-': # <- Polegada fracionaria
        medida = [inch]
        value = ' '.join(inch).split()
        number = [float(item) for item in value if item in '0123456789']
        medida.append(inch_to_meters(*number))
        parametros.append(f'{inch_weight_mesure(mesure= float(input('Tamanho: ')))}')
        parametros.append(medida[:])
    elif item == 'm': # <- Milimetros
        medida = [inch]
        value = ' '.join(inch).split()
        number = [float(item) for item in value if item in '0123456789']
        medida.append(inch_to_meters(*number))
        parametros.append(f'{milimeters_weight_mesure(mesure= float(input('Tamanho: ')))}')
        parametros.append(medida[:])


print(parametros)
