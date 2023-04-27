import pandas as pd 
import numpy as np
import missingno as msno 
import matplotlib.pyplot as plt
import seaborn as sns

data1 = pd.read_csv("Internet_Accesos_Xtecnologia_totalnac.csv", index_col= False, sep= ",", header= 0)
data2 = pd.read_csv("Internet_Accesos_Xtecnologia_xprovincia.csv", index_col= False, sep= ",", header= 0)
data3 = pd.read_csv("Internet_Accesos_xvelocidad_xprovincia_xrangos.csv", index_col= False, sep= ",", header= 0)
data4 = pd.read_csv("Internet_Ingresos.csv", index_col= False, sep= ",", header= 0)
data5 = pd.read_csv("Internet_Penetracion_xprovincia.csv", index_col= False, sep= ",", header= 0)
data6 = pd.read_csv("Internet_distribucion_Accesos_xvelocidad.csv", index_col= False, sep= ",", header= 0)
data7 = pd.read_csv("historico_velocidad_internet_xprovincia.csv", index_col= False, sep= ",", header= 0)

# Proceso de ETL de los dataset

# Definimos la funcion fecha
def to_fecha(df= pd.DataFrame):
    año = df["Año"]
    trimestre = int(df["Trimestre"])
    mes = (trimestre - 1) * 3 + 1
    return pd.to_datetime(f'{año}-{mes}-01')

# dataset5
data5["Accesos por cada 100 hogares"] = data5["Accesos por cada 100 hogares"].str.replace(",",".").astype(float)
data5["fecha"] = data5.apply(to_fecha, axis=1)
data5.set_index("fecha", inplace= True)
data5 = data5.pivot(columns= "Provincia", values= "Accesos por cada 100 hogares")

# dataset5
data4["Ingresos (miles de pesos)"] = data4["Ingresos (miles de pesos)"].str.replace(".","").astype(float)
data4["fecha"] = data4.apply(to_fecha, axis=1)
data4.set_index("fecha", inplace= True)
data4.sort_index(inplace=True)
data4["cambio_pct"] = data4["Ingresos (miles de pesos)"].pct_change()*100

# KPI 1: Aumento de 2% en el acceso a Internet por provincia cada 100 hogares.
def to_provincia(df= pd.DataFrame):
    a = []
    for col in  df.columns.values.tolist():
        valor1 = df.iloc[-1][col] 
        valor2 = df.iloc[-2][col] 
        cambio_pct = (valor1 - valor2)/valor2
        
        if cambio_pct >= 0.02:
            a.append(cambio_pct)
            print(f"{col}, último trimestre: {valor1}")
            print(f"{col}, penúltimo trimestre: {valor2}")
            print(f"El cambio porcentual en el ultimo trimestre es:{ cambio_pct}")
           
    return "Indicador final:",len(a)/24

plt.title("Provincias que cumplieron el objetivo")
data5.Catamarca.plot(legend= "Catamarca", figsize=(10, 6))
data5.Jujuy.plot(legend= "Jujy", figsize=(10, 6))
data5["La Pampa"].plot(legend= "La Pampa", figsize=(10, 6))
data5["Mendoza"].plot(legend= "Mendoza", figsize=(10, 6))
data5["San Juan"].plot(legend= "San Juan",figsize=(10, 6))
data5.Tucumán.plot(legend= "Tucumán",figsize=(10, 6))
