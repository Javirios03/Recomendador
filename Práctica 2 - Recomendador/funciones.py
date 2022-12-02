import pandas as pd
from difflib import SequenceMatcher
import random


def get_pelicula(title: str, df: pd.DataFrame) -> pd.Series:
    '''Given a title, returns the pandas
    series that has all the information of such film.
    The title must be right, this is, perfectly coincident
    with some value in the column "title" of the df

    Parameters
    ----------
    title:
        string; título de la película especificada por usuario

    Returns
    -------
    pd.Series:
        Row-like object of the Series class
    '''

    # Índice de la fila de los datos de la película con título "titulo"
    # df.index[] devuelve un objeto del tipo Int64Type. Podemos acceder
    # al índice entero con su primer elemento
    index = df.index[df["title"] == title]
    return df.loc[index]


def clean_df(label: str, df: pd.DataFrame) -> pd.DataFrame:
    '''Given a label (column title),
    cleans the dataset, eliminating all rows
    with a nan in such column value

    Parameters
    ----------
    label:
        string; título de la columna
    df:
        pd.DataFrame; base de datos original

    Returns
    -------
    pd.DataFrame:
        base de datos limpia
    '''
    df = df[df[label].notna()]
    return df


def extraer_generos(pelicula: pd.Series) -> list:
    '''Gets the original list of genres from a string that encapsules them

    Parameters
    ----------
    pelicula:
        df.Series; parte de la base de datos con todos
        los datos de la película especificada por el usuario

    Returns
    -------
    lista_generos:
        list; contiene cadenas con los géneros de la película
    '''
    lista_generos = []

    try:
        # Accedemos a la columna de géneros de la película en cuestión
        # Además, le hacemos slice para quitar los corchetes que separan
        # ya que son de la forma [{}, {}, ...]
        dicts = eval(pelicula["genres"].iloc[0][1:-1])
        # dicts es una tupla con n diccionarios de los géneros
        for dict in dicts:
            lista_generos.append(dict["name"])
    except TypeError:  # Por si acaso hay algún valor distinto de lo esperado
        pass
    return lista_generos


def buscar_similares(tit_original: str, titulos: list) -> list:
    '''Dado el título de una película que no está incluido en la base de datos
    (ya sea porque se equivocó el usuario o directamente no está contemplada)
    en el dataset, encuentra aquellas películas con un título más similar

    Parameters
    ----------
    tit_original:
        string; título de la película especificada por el usuario
    titulos:
        list; contiene los títulos de todas las películas del dataset

    Returns
    -------
    similares:
        lista; Los elementos son cadenas con los títulos de las películas
    '''
    similares = []
    for title in titulos:
        ratio = SequenceMatcher(None, tit_original, title).ratio()
        if ratio > 0.7:
            similares.append(title)
            if ratio > 0.9 or len(similares) == 5:
                return similares
    return similares


def panel(similares: list, idx: int) -> str:
    '''Forma la cadena que se usará para otorgar al usuario la elección
    de títulos similares al especificado

    Parameters
    ----------
    similares:
        list; contiene cadenas de los títulos
    idx:
        int; especifica el caso de panel (0 para enseñar al usuario los
        titulos similares y 1 cuando se ha equivocado y le proponemos títulos)

    Returns
    -------
    string:
        str
    '''

    string = ""
    for i in range(len(similares)):
        string += "\t" + str(i+1) + ". " + similares[i] + "\n"
    if idx:
        string += "\t" + str(len(similares)+1) + ". No es ninguna de estas"
    return string


def similaridad_pelis(lista_generos, lista_titulos, df) -> list:
    '''Obtiene una lista de 5 películas
    similares a la especificada por el usuario

    Parameters
    ----------
    lista_generos:
        list; contiene cadenas de los géneros de la película
    lista_titulos:
        list; contiene todos los títulos
    df:
        pf.Dataframe; base de datos con todos los datos

    Returns
    -------
    list:
        lista con los títulos de las 5 películas más parecidas
    '''
    titulos = lista_titulos.copy()
    perfecto, bien, mediocre = [], [], []

    while titulos:
        titulo = random.choice(titulos)
        pelicula = get_pelicula(titulo, df)
        generos = extraer_generos(pelicula)
        i = 0
        for genero in generos:
            if genero in lista_generos:
                i += 1
        if i == 1:
            mediocre.append(titulo)
        elif i == 2:
            bien.append(titulo)
        elif i == 3:
            perfecto.append(titulo)
        if len(perfecto) == 5:
            return perfecto
        titulos.remove(titulo)
    return bien
