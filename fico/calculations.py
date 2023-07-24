"""Collects the indices of the actions (alternatives).

This module allows the user to automatically collect performance evaluation indexes 
(criteria) for each of the actions (alternatives) and return a matrix with the information 
of the actions and the chosen indices

The module contains the following functions:

- `load_sp500()` - Loads the data file of the actions to be analyzed.
- `setup_selenium()` - Start command to open the browser. 
- `collect_indices(a, b)` - Collects the indices of the actions.
- `format_decision_matrix(a, b)` - Arranges collected data in matrix format.
- `transpose_indices(a, b)` - Formats the data by transposing the array data.
- `concatenate_indices(a, b)` - Concatenates the data in the form of a decision matrix.

Examples:
    Examples should be written in `doctest` format, and should illustrate how to use the
    function.
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
    """The load_sp500 function loads data from an Excel file.

    Args:
        None

    Returns:
        A DataFrame containing data from the Excel file.

    Examples:
        >>> sp500 = load_sp500()
    """
    sp500 = pd.read_excel("datascience_teste.xlsx")
    display(sp500)
    return sp500


def setup_selenium():
    """The setup_selenium function sets up a Selenium WebDriver.

    Args:
        None

    Returns:
        A Selenium WebDriver object.

    Examples:
        >>> nav = setup_selenium()
    """
    servico = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=servico)
    return nav


def collect_indices(sp500, nav):
    """The collect_indices function collects indices from a website.

    Args:
        sp500: A DataFrame containing information about companies
        nav: A Selenium WebDriver object used to navigate the website

    Returns:
        None

    Examples:
        >>> collect_indices(sp500, nav)
    """
    for linha in sp500.index:
        indices = []
        nome = sp500.loc[linha, "Company"]
        arquivo = sp500.loc[linha, "Symbol"]
        nav.get("https://statusinvest.com.br/")
        time.sleep(1)
        try:
            nav.find_element(
                By.XPATH, '//*[@id="main-nav-nav"]/div/div/div/ul/li[2]/a/i'
            ).click()
            nav.find_element(
                By.XPATH, '//*[@id="main-search"]/div[1]/span[1]/input[2]'
            ).send_keys(nome)
            time.sleep(4)
            nav.find_element(By.PARTIAL_LINK_TEXT, "STOCK").click()
            time.sleep(1)
            indicadores = nav.find_elements(By.CLASS_NAME, "indicator-today-container")
            for elemento in indicadores:
                texto = elemento.text
                indices.append(texto)
            data_df = pd.DataFrame(indices)
            data_df.to_csv(arquivo)
        except:
            print(nome)


"""
The collect_indices function takes two arguments: sp500, which is a DataFrame containing
information about companies, and nav, which is a Selenium WebDriver object used to navigate
a website.

The function iterates over the rows of the sp500 DataFrame using a for loop. For each row, 
it creates an empty list called indices, and extracts the values of the 'Company' and 'Symbol'
 columns, storing them in the variables nome and arquivo, respectively.

Next, the function uses the get method of the nav object to navigate to the website 
'https://statusinvest.com.br/'. It then waits for 1 second using the time.sleep function.

Inside a try block, the function uses various methods of the nav object to interact with 
the website. It clicks on an element, enters text into an input field, waits for 4 seconds, 
clicks on another element, and waits for 1 more second.

After that, the function uses the find_elements method of the nav object to find multiple 
elements on the page with the class name 'indicator-today-container'. It iterates over 
these elements using a for loop, extracts their text using the text property, and appends 
this text to the indices list.

Finally, the function creates a DataFrame from the indices list using the pd.DataFrame 
constructor, and saves it to a CSV file with a name specified by the value of the arquivo 
variable.

If an exception occurs during any of these operations, the function prints the value of 
the nome variable using the print function.
"""


def format_decision_matrix():
    """The format_decision_matrix function formats decision matrices.

    Args:
        None

    Returns:
        None

    Examples:
        >>> format_decision_matrix()
    """
    caminho = Path(r"base_dados")
    arquivos = caminho.iterdir()
    for arquivo in arquivos:
        nome = arquivo.name
        indices = pd.read_csv(arquivo)
        lista = []
        valores = indices.iloc[0, 1].split("\n")
        for valor in valores:
            if valor not in [
                "format_quote",
                "show_chart",
                "help_outline",
                "INDICADORES DE VALUATION",
                "INDICADORES DE ENDIVIDAMENTO",
                "INDICADORES DE EFICIÊNCIA",
                "INDICADORES DE RENTABILIDADE",
                "INDICADORES DE CRESCIMENTO",
            ]:
                lista.append(valor)
        lindices_df = pd.DataFrame(lista)
        itens = lindices_df[::2]
        valor = lindices_df[1::2]
        itens_df = pd.DataFrame(itens)
        itens_df.reset_index(inplace=True)
        valor_df = pd.DataFrame(valor)
        valor_df.reset_index(inplace=True)
        final_df = pd.concat([itens_df, valor_df], axis=1)

        final_df.columns = ["nada", "Indices", "apagar", "Valores"]
        tabela_indices = final_df.drop(columns=["nada", "apagar"], axis=1)

        for linha in tabela_indices["Valores"]:
            try:
                tabela_indices["Valores"] = tabela_indices["Valores"].str.replace(
                    "%", ""
                )
            except:
                print(nome)
        tabela_indices.rename(columns={"Valores": nome}, inplace=True)
        tabela_indices.to_csv(nome)


def transpose_indices():
    """The transpose_indices function transposes indices.

    Args:
        None

    Returns:
        None

    Examples:
        >>> transpose_indices()
    """
    caminho = Path(r"base_dados")
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
    """The concatenate_indices function concatenates indices.

    Args:
        None

    Returns:
        None

    Examples:
        >>> concatenate_indices()
    """
    caminho = Path(r"base_dados")
    arquivos = caminho.iterdir()

    indices = []
    for arquivo in arquivos:
        nome = arquivo.name
        df = pd.read_csv(arquivo)
        indices.append(df)

    indice_ibov = pd.concat(indices)
    indice_ibov.to_csv("Indice_SP_500.csv")


if __name__ == "__main__":
    sp500_data = load_sp500()
    nav = setup_selenium()
    collect_indices(sp500_data, nav)
    format_decision_matrix()
    transpose_indices()
    concatenate_indices()

"""
The code above defines three functions: `format_decision_matrix`, `transpose_indices`, 
and `concatenate_indices`.

The `format_decision_matrix` function formats decision matrices. It starts by creating 
a `Path` object representing the `'base_dados'` directory and uses the `iterdir` method
 to get an iterator over the files in that directory. The function then iterates over 
 these files using a for loop.

For each file, the function reads its contents into a DataFrame using the `pd.read_csv` 
function, and extracts the file name using the `name` property of the `arquivo` object. 
It then creates an empty list called `lista`, and extracts the value in the first row 
and second column of the `indices` DataFrame, splits it on newline characters using the 
`split` method, and stores the resulting list in the `valores` variable.

Next, the function iterates over the values in the `valores` list using a for loop. For 
each value, it checks if it is not in a list of specific strings. If this condition is 
true, it appends the value to the `lista` list.

After that, the function creates a DataFrame from the `lista` list using the `pd.DataFrame` 
constructor, and uses slicing to extract every other row from this DataFrame, starting 
with the first row. It stores these rows in a new DataFrame called `itens`. It then uses
 slicing again to extract every other row from the original DataFrame, starting with the
   second row, and stores these rows in a new DataFrame called `valor`.

The function then resets the index of both DataFrames using their `reset_index` method 
with the `inplace` parameter set to `True`. It concatenates these two DataFrames along 
their columns using the `pd.concat` function, and stores the resulting DataFrame in a 
variable called `final_df`.

Next, the function sets the column names of this DataFrame to specific values using its 
`columns` property. It then drops two of these columns using its `drop` method with the 
`columns` parameter set to a list of column names and the `axis` parameter set to 1. It 
stores the resulting DataFrame in a variable called `tabela_indices`.

After that, the function iterates over the values in the `'Valores'` column of this DataFrame
 using a for loop. For each value, it tries to replace all occurrences of `"%"` with an 
 empty string using its `str.replace` method. If an exception occurs during this operation,
   it prints the value of the `nome` variable using the `print` function.

Finally, it renames one of its columns using its `rename` method with the `columns` 
parameter set to a dictionary mapping old column names to new column names and the `inplace` 
parameter set to `True`. It then saves this DataFrame to a CSV file with a name specified 
by the value of the `nome` variable using its `to_csv` method.

The second function defined in this code is called `transpose_indices`. This function 
transposes indices. It starts by creating a Path object representing the `'base_dados'` 
directory and uses its iterdir method to get an iterator over files in that directory. 
The function then creates an empty list called concatenado and iterates over these files 
using a for loop.

For each file, it reads its contents into a DataFrame using pd.read_csv, transposes this
 DataFrame using its T property, drops its first two rows using iloc indexing, and appends 
 it to concatenado.

The third function defined in this code is called concatenate_indices. This function 
concatenates indices. It starts by creating a Path object representing 'base_dados' 
directory and uses its iterdir method to get an iterator over files in that directory. 
The function then creates an empty list called indices and iterates over these files 
using a for loop.

For each file, it reads its contents into a DataFrame using pd.read_csv and appends 
this DataFrame to indices. After that, it concatenates all DataFrames in indices along 
their rows using pd.concat and stores resulting DataFrame in indice_ibov. Finally, 
it saves this DataFrame to 'Indice_SP_500.csv' file using its to_csv method.

At end of code there is an if statement checking if __name__ is equal '__main__'. 
If this condition is true (i.e., if code is being run as script rather than imported as
 module), code calls several functions: load_sp500(), setup_selenium(), collect_indices
 (sp500_data,nav), format_decision_matrix(), transpose_indices(), concatenate_indices().
"""
