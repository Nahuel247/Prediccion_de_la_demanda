
###################################################################################
#                  PROYECTO: MODELO PARA PREDECIR LA DEMANDA
#                        CON INTELIGENCIA ARTIFICIAL
###################################################################################

#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

########################################
# IMPORTAMOS LAS LIBRERÍAS DE INTERÉS
########################################

import numpy as np
import pandas as pd
import random
from numpy.random import rand
import warnings
import seaborn as sns
warnings.filterwarnings('once')

seed=123
np.random.seed(seed) # fijamos la semilla
random.seed(seed)

#############################################
# CREAMOS LAS FUNCIONES QUE VAMOS A UTILIZAR
#############################################

# Se crea una función que construye las variables de interés según tienda a partir de un diccionario de variables
# diccionario_variablesF: arreglo que contiene las variables que servirán como "variable respuesta" (futuro)
# nombre_variablesF: arreglo con el nombre de las variables

def creacion_variablesF(x):
    d = {}
    for funcion in diccionario_variablesF:
        exec(funcion)
    return pd.Series(d, index=nombre_variablesF)

# Se construye una función que sirva para seleccionar los registros futuros, agruparlos según tienda y calcular
# las variables que se encuentran en "diccionario_variablesF" y que son de interés

def data_futuro(fecha_referencia):
    fecha_final=fecha_referencia + pd.offsets.Day(n_dfuturo)
    data_variables = data_pivot.loc[(data_pivot['date'] > str(fecha_referencia)) &
                                    (data_pivot['date'] <= str(fecha_final))].copy().\
        groupby(["store"]).apply(creacion_variablesF).reset_index()
    data_variables=data_variables.assign(fecha_referencia=fecha_referencia)
    variable_respuesta.append(data_variables)
    return variable_respuesta


# Se crea una función que construya las variables de interés según tienda a partir de un diccionario de variables
# diccionario_variablesP: arreglo que contiene las variables que van a servir como "variable explicativas" (pasado)
# nombre_variablesP: arreglo con el nombre de las variables

def creacion_variablesP(x):
    d = {}
    for funcion in diccionario_variablesP:
        exec(funcion)
    return pd.Series(d, index=nombre_variablesP)


# Se construye una función que sirva para seleccionar los registros pasados, agruparlos según tienda y calcular
# las variables que se encuentran en "diccionario_variablesP" y que son de interés

def data_pasado(fecha_referencia):
    fecha_inicio=fecha_referencia - pd.offsets.Day(n_dpasado)
    data_variables = data_pivot.loc[(data_pivot['date'] >= str(fecha_inicio)) &
                                   (data_pivot['date'] < str(fecha_referencia))].copy().\
        groupby(["store"]).apply(creacion_variablesP).reset_index()
    data_variables=data_variables.assign(fecha_referencia=fecha_referencia)
    variable_explicativa.append(data_variables)
    return variable_explicativa


########################################
# DEFINIMOS LOS REGISTROS DE REFERENCIA
#########################################

n_dfuturo= 7 # número de días en el futuro que se usara para la predicción (sin incluir el día de referencia)
n_dpasado= 21 # número de días en el pasado que se usara para la predicción (sin incluir el día de referencia)

corte_inferior=data_pivot["date"].min() + pd.offsets.Day(n_dpasado) # fecha donde comenzarán los calculos
corte_superior=data_pivot["date"].max() - pd.offsets.Day(n_dfuturo) # fecha donde terminaran los calculos


# Se crea una base con las fechas de referencias
data_referencia=data_pivot.loc[(data_pivot['date'] > corte_inferior ) &
                               (data_pivot['date'] < corte_superior)][["date","base"]].copy().\
    drop_duplicates().reset_index().drop("index",axis=1)

data_referencia.columns=["fecha_referencia","base"]

#data_referencia=data_referencia.iloc[1:10,].copy()

####################################################
# CREAMOS LA VARIABLE RESPUESTA PARA CADA LOCAL
####################################################

# Construimos el arreglo que nos permitira evaluar la venta total en los próximo 7 días por tienda e item
diccionario_variablesF=["d['item" + str(i+1) + "_total_F'] = x['item_" + str(i+1) + "'].sum()" for i in range(50)]
nombre_variablesF = ["item"+str(i+1)+"_total_F" for i in range(50)]

variable_respuesta=[]
data_referencia["fecha_referencia"].apply(data_futuro)
variable_respuesta=pd.concat(variable_respuesta).reset_index().drop("index",axis=1)


# se observa que para cada fecha de referencia-tienda existen 50 variables respuestas que
# corresponden al total de ventas en los próximos 7 días
variable_respuesta.shape

variable_respuesta.columns

####################################################
# CREAMOS LAS VARIABLES EXPLICATIVAS
####################################################

# Creamos un listado de funciones que servirán para construir las variables explicativas,
# es decir, la venta de cada items, en los últimos 21 días, será evaluado por cada una de las siguientes funciones
lista_funcionesP = ["sum", "max","min","mean","std","kurtosis","median","idxmin","idxmax","prod"]

# Construimos el arreglo que nos permitirá construir las variables explicativas en los últimos 21 días
diccionario_variablesP=["d['item" +str(i+1)+"_"+j+ "'] = x['item_" + str(i+1) + "']."+j+"()"
                        for i in range(50) for j in lista_funcionesP]
nombre_variablesP = ["item"+str(i+1)+"_"+ j for i in range(50) for j in lista_funcionesP]


variable_explicativa=[]
data_referencia["fecha_referencia"].apply(data_pasado)
variable_explicativa=pd.concat(variable_explicativa).reset_index().drop("index",axis=1)


# se observa que para cada fecha de referencia-tienda existen más de 500 variables explicativas
# que corresponden a las distintas funciones aplicadas a los distintos items vendidos en los últimos 21 días
variable_explicativa.shape
variable_explicativa.columns


#COMPROBAMOS LOS RESULTADOS PARA LA VARIABLE RESPUESTA
variable_respuesta.head(3)
fecha_final=pd.to_datetime("2013-01-24") + pd.offsets.Day(n_dfuturo)
data_pivot.loc[(data_pivot['store'] ==1) & (data_pivot['date'] > str("2013-01-24")) &
               (data_pivot['date'] <= str(fecha_final))]



#COMPROBAMOS LOS RESULTADOS PARA LA VARIABLE EXPLICATIVA
variable_explicativa.head(3)
fecha_final=pd.to_datetime("2013-01-24") + pd.offsets.Day(n_dfuturo)

data_pivot.loc[(data_pivot['store'] =='store_1') & (data_pivot['date'] >= str(fecha_final)) &
                                   (data_pivot['date'] < str("2013-01-24"))].copy()


####################################################################
# UNIMOS LOS REGISTROS EN BASE AL LOCAL Y LA FECHA DE REFERENCIA
####################################################################

# Unificamos la data
data_artificial=pd.merge(data_referencia,variable_explicativa, how="left", on="fecha_referencia")
data_artificial=pd.merge(data_artificial,variable_respuesta, how="left", on=["fecha_referencia","store"])


# Revisamos las dimensiones
data_artificial.shape
# (17960, 553)
variable_explicativa.shape
# (17960, 502)
variable_respuesta.shape
# (17960, 52)


# La guardamos para cargar de forma independiente (si se desea)
data_artificial.to_csv("data_artificial.csv", sep=";")