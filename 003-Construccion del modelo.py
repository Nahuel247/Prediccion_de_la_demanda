
###################################################################################
#             PROYECTO: MODELO PARA PREDECIR LA DEMANDA DE PRODUCTOS
#                             CON MACHINE LEARNING
###################################################################################

#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################


########################################
# IMPORTAMOS LAS LIBRERIAS DE INTERÉS
########################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.random.seed(123)
from sklearn.multioutput import MultiOutputRegressor
import xgboost as xgb
import warnings
warnings.filterwarnings('once')


##########################################
# CONSTRUIMOS EL MODELO
##########################################

# Cargamos la data
data_artificial=pd.read_csv("data_artificial.csv", sep=";")

# Construimos dos variables de interés, asociadas al mes de la venta y al día.
data_artificial=data_artificial.assign(mes=pd.to_datetime(data_artificial['fecha_referencia']).dt.month)
data_artificial=data_artificial.assign(dia=pd.to_datetime(data_artificial['fecha_referencia']).dt.weekday)


# Segmentamos la data en train y test
variable_respuesta= ["item"+str(i+1)+"_total_F" for i in range(50)]

X_pretrain =data_artificial.loc[data_artificial["base"]=="train",:].drop(variable_respuesta+['fecha_referencia', 'base'],axis=1).copy()
y_pretrain = data_artificial.loc[data_artificial["base"]=="train",variable_respuesta].copy()
X_test =data_artificial.loc[data_artificial["base"]=="test",:].drop(variable_respuesta+['fecha_referencia', 'base'],axis=1).copy()
y_test = data_artificial.loc[data_artificial["base"]=="test",["fecha_referencia","store"]+variable_respuesta].copy()


# segmentamos pretrain para crear una muestra de entrenamiento y otra de validación,
# que nos servirá para ir ajustando los hiperparametros del modelo

n_rows=X_pretrain.shape[0]
X_validation=X_pretrain.loc[(n_rows-3500):,]
y_validation=y_pretrain.loc[(n_rows-3500):,]
X_train=X_pretrain.loc[:(n_rows-3501),]
y_train=y_pretrain.loc[:(n_rows-3501),]


# Definimos los párametros para el modelo (los cuales he ido cambiando por tanteo)
parametros = ({"objective":"reg:linear",
           "colsample_bytree" : 1,
           "learning_rate" : 0.2,
           "max_depth" : 3,
           "n_estimators" : 70
})

# Ajustamos el modelo
modelo = MultiOutputRegressor(xgb.XGBRegressor(**parametros)).fit(X_train, y_train)


###############################################
# DESEMPEÑO DEL MODELO EN TRAIN Y VALIDATION
###############################################

# TRAIN
y_train_pred=pd.DataFrame(modelo.predict(X_train))
y_train_pred.columns=y_train.columns

# Error cuadratico medio (RMSE)
print(np.sqrt(np.mean((y_train_pred.reset_index() - y_train.reset_index())**2, axis=0)))

# Error porcentual
np.sum(abs(np.array(y_train_pred)-np.array(y_train))/np.array(y_train)<=0.10)/(y_train.size)


# VALIDATION
y_validation_pred=pd.DataFrame(modelo.predict(X_validation))
y_validation_pred.columns=y_validation.columns

# Error cuadratico medio (RMSE)
print(np.sqrt(np.mean((y_validation_pred.reset_index() - y_validation.reset_index())**2, axis=0)))

# Error porcentual
np.sum(abs(np.array(y_validation_pred)-np.array(y_validation))/np.array(y_validation)<=0.10)/(y_validation.size)
np.sum(abs(np.array(y_validation_pred)-np.array(y_validation))/np.array(y_validation)<=0.15)/(y_validation.size)
np.sum(abs(np.array(y_validation_pred)-np.array(y_validation))/np.array(y_validation)<=0.20)/(y_validation.size)


####################################
# DESEMPEÑO DEL MODELO EN TEST
####################################

y_test_pred=pd.DataFrame(modelo.predict(X_test)).reset_index().drop("index",axis=1)
y_test_pred=pd.concat([y_test.loc[:,["fecha_referencia","store"]].reset_index().drop("index",axis=1),y_test_pred],axis=1)
y_test_pred.columns=y_test.columns

# Error cuadratico medio (RMSE)
print(np.sqrt(np.mean((y_test_pred.reset_index() - y_test.reset_index())**2, axis=0)))


# Error porcentual
np.sum(abs(np.array(y_test_pred)-np.array(y_test))/np.array(y_test)<=0.10)/(y_test.size)
np.sum(abs(np.array(y_test_pred)-np.array(y_test))/np.array(y_test)<=0.15)/(y_test.size)
np.sum(abs(np.array(y_test_pred)-np.array(y_test))/np.array(y_test)<=0.20)/(y_test.size)


# Visualizamos los resultados

y_test=y_test.assign(sales="actual value")
y_test_pred=y_test_pred.assign(sales="predict value")

resultados=pd.concat([y_test,y_test_pred])
resultados["date"]=pd.to_datetime(resultados['fecha_referencia'])


fig=sns.lineplot(data=resultados.query("store in [3, 5, 1]"), x="date", y="item8_total_F", hue="store",
             style="sales", linewidth = 2, palette="tab10")
fig.set_ylabel("sales")
fig.set_xlabel("date")