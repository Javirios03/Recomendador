import pandas as pd
import funciones
import sys


df_movies = pd.read_csv('movies_metadata.csv', sep=",",
                        low_memory=False)[["title", "genres"]]

df_movies = funciones.clean_df("title", df_movies)
df_movies = funciones.clean_df("genres", df_movies)
lista_titulos = df_movies["title"].to_list()


if __name__ == "__main__":

    print("Bienvenido a nuestro recomendador. A continuación, podrá conocer",
          "nuevas películas basándose en las que les han gustado.")
    print("Para ello, encontrará películas de géneros similares a la que elija.")
    print("Le pedimos por favor que introduzca los títulos en inglés, ya que",
          "no reconocerá las películas por su título en castellano.\n")
    titulo = str(input("Introduzca el título de una película que le haya gustado: "))

    # Comprobamos que el título introducido pertenece a alguna peli del dataset
    correcto = False
    while not correcto:
        if titulo in lista_titulos:
            correcto = True
            pelicula = funciones.get_pelicula(titulo, df_movies)
            lista_generos = funciones.extraer_generos(pelicula)

        else:  # Probablemente, el usuario introdujo un caracter incorrecto
            # Le daremos a elegir entre hasta los 5 títulos más parecidos, para que
            # elija. Si ninguna de estos 5 lo es, significa que no tenemos
            # ese título en la base de datos
            print("No hemos encontrado una película con el título especificado.",
                  "¿Quizás se refiere a alguna de las siguientes?")
            similares = funciones.buscar_similares(titulo, lista_titulos)
            print(funciones.panel(similares, 1))
            opcion = int(input("Introduzca una opción: "))
            print()
            if opcion in [i+1 for i in range(len(similares))]:
                titulo = similares[opcion-1]
            elif opcion-1 in [i+1 for i in range(len(similares))]:
                print("La película que desea no se encuentra en la base de datos")
                titulo = str(input("Introduzca un título válido: "))
            else:
                print("Ha elegido una opción incorrecta")
                titulo = str(input("Introduzca un título válido: "))
            print()

    similares = funciones.similaridad_pelis(lista_generos, lista_titulos, df_movies)
    print(f"\nA continuación, se le muestran las {len(similares)} películas ",
          "que, creemos, debería ver si le ha gustado", titulo)
    print(funciones.panel(similares, 0))
    sys.exit(0)
