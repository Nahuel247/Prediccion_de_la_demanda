
###################################################################################
#             PROYECTO: MODELO PARA PREDECIR LA DEMANDA DE PRODUCTOS
#                             CON MACHINE LEARNING
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
sns.set(font_scale=1.3)

# Comportamiento e interrelación entre la venta de distintos items
sns.relplot(data=data.query('(item in ["item_1","item_3", "item_8","item_50"])').sample(9000).copy(), x="date",
            y="sales", hue="item", style="store", palette="tab10",s=80)

# Comportamiento de la demanda para el item_8 en distintas tiendas
sns.relplot(data=data.query( 'item=="item_8"').sample(8000).copy(), x="date", y="sales",
             hue="store", palette="tab10", marker="o",edgecolor="none")
