import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk
import requests


requisicao = requests.get('https://economia.awesomeapi.com.br/json/all')
moedas_dic = requisicao.json()
lista_moedas = list(moedas_dic.keys())
var_moedas = []


def buscar_cotacao():
    moeda_selecionada = combobox_moeda.get()
    data_cotacao = calendario.get()
    ano = data_cotacao[-4:]
    mes = data_cotacao[3:5]
    dia = data_cotacao[:2]
    link = f'https://economia.awesomeapi.com.br/{moeda_selecionada}-BRL/?start_date={ano}{mes}{dia}&end_date={ano+mes+dia}'
    requisicao_moeda = requests.get(link)
    cotacao = requisicao_moeda.json()
    valor_moeda = cotacao[0]['bid']
    texto_cotacao['text'] = f'A cotação da moeda {moeda_selecionada} no dia {data_cotacao} foi de R${valor_moeda}'


def checkbox_marcados():
    moedas_selecionadas = []
    for indice, moeda in enumerate(lista_moedas):
        if var_moedas[indice].get() == '1':
            moedas_selecionadas.append(moeda)
    return moedas_selecionadas


def buscar_cotacoes():
    resultados = []
    moedas_selecionadas = checkbox_marcados()

    for moeda in moedas_selecionadas:
        data_final_varias_moedas = calendario_final.get()
        ano_final = data_final_varias_moedas[-4:]
        mes_final = data_final_varias_moedas[3:5]
        dia_final = data_final_varias_moedas[:2]
        link = f'https://economia.awesomeapi.com.br/{moeda}-BRL/?start_date={ano_final}{mes_final}{dia_final}&end_date={ano_final}{mes_final}{dia_final}'
        requisicao_moeda = requests.get(link)
        cotacoes_moeda = requisicao_moeda.json()

        for cotacao in cotacoes_moeda:
            valor_cotacao = cotacao.get("bid")
            resultado = f'A cotação da moeda {moeda} no dia {data_final_varias_moedas} foi de R${valor_cotacao}'
            resultados.append(resultado)

    texto_cotacoes['text'] = '\n'.join(resultados)


janela = tk.Tk()
janela.title('Sistema de Busca de Cotação de Moedas')
janela.rowconfigure(0,weight=1)
janela.columnconfigure([0,1], weight=1)


# Cotacao de uma moeda só
msg_cotacao_moeda = tk.Label(text='Busca de uma moeda específica', fg='white', bg='#2602FC', borderwidth=2, relief='solid')
msg_cotacao_moeda.grid(row=0, column=0,  sticky='EW', padx=10, pady=10, columnspan=3)


selecionar_moeda = tk.Label(text='Selecione a moeda que deseja buscar:', anchor='w')
selecionar_moeda.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')


combobox_moeda = ttk.Combobox(janela, values=lista_moedas)
combobox_moeda.grid(row=1, column=2, pady=10, padx=10, sticky='nsew')


selecionar_dia_label = tk.Label(text='Selecione o dia que deseja pegar a cotação:', anchor='w')
selecionar_dia_label.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')


calendario = DateEntry(year=2023, locale='pt_br')
calendario.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')


texto_cotacao = tk.Label(text='')
texto_cotacao.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')


botao_cotacao = tk.Button(text='Buscar Cotação', command=buscar_cotacao)
botao_cotacao.grid(row=3, column=2, sticky='EW', padx=10, pady=10)


# Cotacao de varias moedas
msg_cotacao_varias_moedas = tk.Label(text='Buscar mais de uma moeda:', fg='white', bg='#2602FC', borderwidth=2, relief='solid')
msg_cotacao_varias_moedas.grid(row=4, column=0, sticky='nsew', padx=10, pady=10, columnspan=3)


selecionar_moedas = tk.Label(text='Selecione as moedas que deseja buscar:', anchor='w')
selecionar_moedas.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')


# Colocar número de colunas necessarias para todos os checkbox
num_colunas = 3
num_linhas = (len(lista_moedas) + num_colunas - 1) // num_colunas


# Colocando um checkbox para cada moeda
for i, moeda in enumerate(lista_moedas):
    var = tk.StringVar(master=janela)
    var_moedas.append(var)
    checkbox_moedas = ttk.Checkbutton(text=moeda, variable=var)
    checkbox_moedas.grid(row=6 + i // num_colunas, column=i % num_colunas, padx=10, pady=10, sticky='ew')


data_final = tk.Label(text='Selecione o dia que deseja pegar a cotação:')
data_final.grid(row=7 + num_linhas, column=0)


calendario_final = DateEntry(year=2023, locale='pt_br')
calendario_final.grid(row=7 + num_linhas, column=1)


botao_cotacoes = tk.Button(text='Buscar Cotação', command=buscar_cotacoes)
botao_cotacoes.grid(row=7 + num_linhas, column=2, sticky='EW', padx=10, pady=10)


texto_cotacoes = tk.Label(text='')
texto_cotacoes.grid(row=8 + num_linhas, column=0, columnspan=2, pady=10, padx=10, sticky='nsew')

janela.mainloop()
