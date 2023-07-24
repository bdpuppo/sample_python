"""This is a sample dummy Python script.

Press Shift+F10 to execute it or replace it with your code.
Press Double Shift to search everywhere for classes, files, tool windows, actions, and
settings.
"""


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import pathlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def load_sp500():
    sp500 = pd.read_excel('datascience_teste.xlsx')
    display(sp500)
    return sp500

def setup_selenium():
    servico = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=servico)
    return nav


def collect_indices(sp500, nav):
    for linha in sp500.index:
        indices=[]
        nome = sp500.loc[linha,'Company']
        arquivo = sp500.loc[linha,'Symbol']
        nav.get('https://statusinvest.com.br/')
        time.sleep(1)
        try:
            nav.find_element(By.XPATH,'//*[@id="main-nav-nav"]/div/div/div/ul/li[2]/a/i').click()
            nav.find_element(By.XPATH,'//*[@id="main-search"]/div[1]/span[1]/input[2]').send_keys(nome)
            time.sleep(4)
            nav.find_element(By.PARTIAL_LINK_TEXT,'STOCK').click()
            time.sleep(1)
            indicadores = nav.find_elements(By.CLASS_NAME,'indicator-today-container')
            for elemento in indicadores:
                texto = elemento.text
                indices.append(texto)
            data_df = pd.DataFrame(indices)
            data_df.to_csv(arquivo)
        except:
            print(nome)

def format_decision_matrix():
    caminho = Path(r'base_dados')
    arquivos = caminho.iterdir()
    for arquivo in arquivos:
        nome = arquivo.name
        indices = pd.read_csv(arquivo)
        lista=[]
        valores = indices.iloc[0,1].split('\n')
        for valor in valores:
            if valor not in ['format_quote', 'show_chart', 'help_outline', 'INDICADORES DE VALUATION', 'INDICADORES DE ENDIVIDAMENTO', 'INDICADORES DE EFICIÊNCIA', 'INDICADORES DE RENTABILIDADE', 'INDICADORES DE CRESCIMENTO']:
                lista.append(valor)
        lindices_df = pd.DataFrame(lista)
        itens = lindices_df[::2]
        valor = lindices_df[1::2]
        itens_df = pd.DataFrame(itens)
        itens_df.reset_index(inplace=True)
        valor_df = pd.DataFrame(valor)
        valor_df.reset_index(inplace=True)
        final_df = pd.concat([itens_df, valor_df], axis = 1)

        final_df.columns = ['nada', 'Indices', 'apagar', 'Valores']
        tabela_indices = final_df.drop(columns = ['nada','apagar'], axis = 1)

        for linha in tabela_indices['Valores']:
            try:
                tabela_indices['Valores'] = tabela_indices['Valores'].str.replace("%", "")
            except:
                print(nome)
        tabela_indices.rename(columns = {'Valores':nome}, inplace = True)
        tabela_indices.to_csv(nome)

def transpose_indices():
    caminho = Path(r'base_dados')
    arquivos = caminho.iterdir()
    concatenado = []
    for arquivo in arquivos:
        nome = arquivo.name
        lindices = pd.read_csv(arquivo)
        indices = pd.DataFrame(lindices)
        indices = indices.T
        indices = indices.iloc[2:]
        concatenado.append(indices)

def concatenate_indices():
    caminho = Path(r'base_dados')
    arquivos = caminho.iterdir()

    indices = []
    for arquivo in arquivos:
        nome = arquivo.name
        df = pd.read_csv(arquivo)
        indices.append(df)

    indice_ibov = pd.concat(indices)
    indice_ibov.to_csv('Indice_SP_500.csv')

if __name__ == '__main__':
    sp500_data=load_sp500()
    nav=setup_selenium()
    collect_indices(sp500_data,nav)
    format_decision_matrix()
    transpose_indices()
    concatenate_indices()

