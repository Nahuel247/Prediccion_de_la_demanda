
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


##############################
# CARGAMOS LOS DATOS
##############################

data=pd.read_csv("train.csv",sep=",")
data["date"] = pd.to_datetime(data["date"])
#data["store"] ="store_"+data["store"].astype(str)
data["item"] ="item_"+data["item"].astype(str)
data.info()

#Segmentamos la data en train y test
#np.where(condition, value if condition is true, value if condition is false)
data["base"]=np.where(data["date"] <"2017-01-01" , "train", "test")

# giramos la data para que en cada columna estén los items
data_pivot=data.pivot(index=["date","store","base"], columns="item", values="sales").reset_index()
data_pivot=data_pivot.sort_values(["date","store"]).copy()

# Guardamos la base de datos
data_pivot.to_csv("data_pivot.csv", sep=";")

##############################
# VISUALIZAMOS ALGUNOS CASOS
##############################

# Comportamiento de la demanda de los distintos items en la tienda 1
sns.relplot(data=data.query( 'store==1').sample(3000).copy(), x="date", y="sales",
             hue="item",style="item",s=60, palette="tab10", legend =False)


# Comportamiento de la demanda para el item_1 en distintas tiendas
sns.relplot(data=data.query( 'item=="item_1"').sample(3000).copy(), x="date", y="sales",
             hue="store",style="store", palette="tab10")



