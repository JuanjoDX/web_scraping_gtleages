## El siguiente codigo consolidado los archivos contenidos dentro de la carpeta Datos y los unifica en 1 solo archivos ademas agrega una columna nueva
## con el nombre del ganador o "X" en caso de empate

import pandas as pd 
import os

lista_archivos = os.listdir("../Datos/")

archivos_csv = [archivo for archivo in lista_archivos if archivo.endswith('.csv')]
datos = pd.DataFrame(columns=['Fecha', 'Equipo Local', 'Jugador Local', 'Equipo Vista',
                              'Jugador Visita', 'Resultado Local', 'Resultado Visita', 'Estado'])
for i in archivos_csv:
    df = pd.read_csv("../Datos/" + i,encoding = "utf-8-sig")
    
    datos = pd.concat([datos,df])
    
datos = datos.reset_index(drop = True)
datos.rename({'Equipo Vista':'Equipo Visita'},axis = 1,inplace = True)

datos["Resultado Local"] = pd.to_numeric(datos["Resultado Local"])
datos["Resultado Visita"] = pd.to_numeric(datos["Resultado Visita"])

datos = datos.fillna(0)
datos.insert(7,"HXA","S")

datos["Fecha"] = pd.to_datetime(datos["Fecha"], format='%d/%m/%Y %H:%M')
datos = datos.sort_values(by = "Fecha",ascending = True).reset_index(drop = True)

for i in range(0,datos.shape[0]):
    if datos.loc[i,"Resultado Local"] > datos.loc[i,"Resultado Visita"]:
        datos.loc[i,"HXA"] = datos.loc[i,"Jugador Local"]
    elif datos.loc[i,"Resultado Local"] < datos.loc[i,"Resultado Visita"]:
        datos.loc[i,"HXA"] = datos.loc[i,"Jugador Visita"]
    else:
        datos.loc[i,"HXA"] = "X"
        
datos.to_excel("../Historico.xlsx",index = False)
datos.to_csv("../Historico.csv",index = False, encoding = "utf-8-sig")
