import json

# with open('\\\\SERVidor\\DOCUMENTOS\\LEONARDO\\programas\\StockBuyRep\\configuration\\konemetal_report.json','r') as file:
with open('C:\\Users\\Leo\\Documents\\GitHub\\StockBuyRep\\configuration\\konemetal_report.json','r') as file:
    konemetal = json.load(file)

print('~~~~\nPrinting konemetal report length...\n~~~~')
print(len(konemetal['report']['bitola']))
print(len(konemetal['report']['material']))
print(len(konemetal['report']['norma']))
print(len(konemetal['report']['dimensao']))
print(len(konemetal['report']['milimetros']))
print(len(konemetal['report']['fabricacao']))
print(len(konemetal['report']['urgente']))
print(len(konemetal['report']['atrasado']))
print(len(konemetal['report']['quilos']))
print(len(konemetal['report']['documento']))
print(len(konemetal['report']['data']))
print(len(konemetal['report']['index']))

_ = input()
