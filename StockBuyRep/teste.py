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
        A= "DIN 11SMN37",
        B= "DIN 12L14",
        C= "DIN 11SMN30",
        D= "SAE 1045",
        E= "ASTM A182f11",
        F= "DIN 316",
        G= "SAE 1020",
        H= "CA 377",
        I= "SAE 1010",
        J= "CA 360",
        K= "SAE 841",
        L= "DIN 304",
        M= "ASTM 564",
        N= "ASTM 630",
        O= "ASTM 17-4PH",
        P= "SAE 1215",
        Q= "6351 T6",
        R= "SAE 4140",
        S= "C 110 ELETROL\u00cdTICO",
        T= "H13",
        U= "SAE 5160",
        V= "NAVAL",
        W= "DIN 20MNCR5",
        X= "DIN ST52.3",
        Y= "NYLON 6.0",
        Z= "ASTM A36",
        AA= "SAE 8640",
        AB= "LNE 380",
        AC= "SAE 8620",
        AD= "VW3",
        AE= "TM23",
        AF= "PTFE",
        AG= "POLIACETAL",
        AH= "VC 131",
        AI= "ASTM A182 F22",
        AJ= "DIN 310",
        AK= "FC 300",
        AL= "NBR 5590",
        AM= "AISIO1 (VND)",
        AN= "FERRO FUNDIDO NODULAR",
        LL= "DIN 304L",
        FL= "DIN 316L"
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


def inch_to_meters(*args):
    if len(args) == 2:
        res = 25.4 * args[0] / args[1]
        return f'{round(res, 2)}mm'
    elif len(args) == 3:
        res = args[1] * 25.4 + 25.4 * args[1] / args[2]
        return f'{round(res, 2)}mm'
    elif len(args) == 4:
        res = 25.4 * args[0] / args[1] + 25.4 * args[2] / args[3]
        return f'{round(res, 2)}mm'


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


def weight_mesure(mesure):
    weight = Material.get(f'{mat}')
    mm = ' '.join(medida[1])
    mm = [num for num in mm if num in '0123456789'] 
    mm = float(mm[0] + mm[1] + mm[2])
    mm /= 100
    if Bitola.get(bit) == 'REDONDO':
        return f'{round(pi * pow(mm / 2, 2) * mesure * weight[1]/ 10, 2)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'QUADRADO':
        return f'{round((pow(mm) * mesure * weight[1])/10, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'SEXTAVADO':
        return f'{round((((3 * sqrt(3) / 2 * ((mm / sqrt(3))**2)) * mesure) * weight[1])/ 10, 3)}Kg', f'{mesure * 1000}mm'
    elif Bitola.get(bit) == 'TUBO SEM COSTURA' or 'TUBO COM COSTURA' or 'TUBO MECÂNICO' or 'TUBO COM COSTURA REMOVIDA':
        diam_inter = float(input(f'Digite o diametro interno do {Bitola.get(bit)}: '))
        diam_exter = float(input(f'Digite o dimetro externo do {Bitola.get(bit)}: '))
        parametros.append(f'Diametro interno: {diam_inter}mm -- Diametro externo: {diam_exter}mm')
        diam_inter = pi * pow(diam_inter / 2, 2) * mesure * weight[1]/ 10
        diam_inter = pi * pow(diam_exter / 2, 2) * mesure * weight[1]/ 10
        if diam_exter > diam_inter:
            return f'{round(diam_exter - diam_inter)}Kg', f'{mesure * 1000}mm' 
        else:
            return f'{round(diam_inter - diam_exter)}Kg', f'{mesure * 1000}mm'

parametros = []
bit = input('Bitola: ').upper()
parametros.append(f'{bitola(tipo= bit)}')
mat = input("Material: ").upper()
parametros.append(f'{material(tipo= mat) }')
parametros.append(f'{norma(tipo= input("Norma: ").upper())} ')
parametros.append(f'{fabricacao(tipo= input('Fabricação: ').upper())} ')

inch = input(f'Digite o diametro do/a {Bitola.get(bit)}: (ex: 3-3/4) ')#'1/2-1/2'
if inch == '"':
    inch = inch.split('"')
    inch = [num for num in inch if num in '0123456789']
    print(inch)
elif inch == "'":
    inch = inch.split("'")
    inch = [num for num in inch if num in '0123456789']
    print(inch)
else:
    medida = [inch]
    inch = ' '.join(inch).split()
    inch = [float(item) for item in inch if item in '0123456789']
    medida.append(inch_to_meters(*inch))

parametros.append(medida[:])
parametros.append(f'{weight_mesure(mesure= float(input('Tamanho: ')))}')

print(parametros)

