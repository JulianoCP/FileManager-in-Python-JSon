import json
import os

f = open('disco.json')
data = json.load(f)

for i in data['blocks']['block_list']:
    print(i)

''' Adicionar um Elemento '''
data['blocks']['block_list'].update({'15': 'juliano.txt'})

''' Adicionar um Binario ao block_list '''
with open("codigo.pdf", "r") as f:
    byte = f.read()
data['blocks']['block_list'].update({'42':(byte)})


''' Buscar o Binario do block_list '''
binario = open('out.pdf', 'wb')
#binario.write(bytes(data['blocks']['block_list']['42'], encoding='utf8'))
binario.write((data['blocks']['block_list']['42']))
binario.close()

''' Remover um Elemento '''
data['blocks']['block_list'].pop('5')


''' Salvar Arquivo para Persistir'''
with open('output.json', 'w') as outfile:
    json.dump(data, outfile)

f.close()
