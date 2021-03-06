# Predicción de la demanda de múltiples ítems

El poder predecir de forma precisa la demanda de producto es de gran interés para el Retail o empresas importadoras, ya que esta información sirve para determina la cantidad de producto que debe ser incluido en la solicitud de importación, identificar la cantidad de producto que deben ser enviado a distintos locales (tienda, almacén, centro de distribución, etc.), entre otros.\
\
Sin embargo, es una tarea bastante difícil y aún más, lo es el predecir la demanda de múltiples ítems.  Esto debido al efecto que pueden tener factores tales cómo: La estacionalidad anual, el día de la semana, el tiempo desde la mayor venta, la competencia entre productos, el desarrollar ofertas, etc.\
\
En este repositorio encontraran el desarrollo metodológico para predecir, a través de Machine Learning, la demanda de 50 items en 10 tiendas distintas. Se utilizó cada día de ventas registradas como fecha de referencia para predecir las ventas en el futuro en base a múltiples variables del pasado, en particular:

* Se utilizó el modelo XGboost, una metodología que se basa en árboles de decisiones.

* Se utilizó una base de datos de ventas históricas de 50 items en 10 tiendas, que contenía 5 años de información de ventas diaria. Los datos fueron descargados desde la página de Kaggle: 
https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data

* A partir de los datos se construyeron 50 variables a predecir, que corresponden a la venta total de cada ítem en los próximos 7 días (sin incluir el día de referencia), para cada una de las tiendas.

* Como variable explicativa se construyeron variables que permitiesen determinar el promedio, el máximo, el mínimo, el total, número de días desde la mayor venta, número de días desde la menor venta, entre otras, para cada uno de los ítems en los 21 días anteriores a la fecha de referencia. Además, se crearon variables relacionadas con la estacionalidad, obteniéndose como resultado cerca de 500 variables explicativas relacionadas a las ventas de cada tienda-perido.

* El modelo fue construido a través de una muestra de construcción, ajustado con una muestra de validación y testeado en una muestra test. Finalmente, el desempeño del modelo fue estimado a través del error porcentual. 

# Resultados
A continuación, se presentan aquellos resultados más relevantes relacionados al desarrollo metodológico, la eficiencia del modelo y su implementación.

# Comportamiento de la demanda en distintas tiendas.
A modo de ejemplo, se muestra la serie de tiempo de ventas diarias de 4 items en las distintas tiendas, durante un periodo de 5 años. Es posible observar estacionalidad en las ventas.

[![Comportamiento-demanda-4-items-10-store.png](https://i.postimg.cc/N0DNbKYr/Comportamiento-demanda-4-items-10-store.png)](https://postimg.cc/3yyCxJkK)

#  Comportamiento de la demanda para el item_8 en distintas tiendas.
A modo de ejemplo, se muestra la serie de ventas del item_8 según tienda. Es posible observar un incremento de las ventas del producto a lo largo del tiempo.

[![Ventas-item8-10store.png](https://i.postimg.cc/43CVpBVL/Ventas-item8-10store.png)](https://postimg.cc/MnDnS0sV)

# Segmentación de la muestra
El modelo fue construido a través de una muestra de construcción, ajustado con una muestra de validación y testeado en una muestra de testeo.  La primera parte de la data fue utilizada para la construcción, la segunda parte para la validación y la última parte para el testeo. Esta forma de segmentación asegura que el modelo sea funcional en el futuro.

[![Segmentaci-n-de-la-muestra.jpg](https://i.postimg.cc/NFF6KBjH/Segmentaci-n-de-la-muestra.jpg)](https://postimg.cc/kRr6Zr8J)

# Construcción de variables
Para la construcción de variables, se utilizó cada registro de ventas como una “fecha de referencia”, es decir, para cada registro se estimó la cantidad de producto que se va vender en los próximos 7 días y a su vez se utilizaron los 21 días anteriores para construir las variables explicativas (500 variables). En ambos casos no se utilizó el día de referencia en los cálculos, ya que muchas veces cuando se quiere implementar el modelo, las ventas del mismo día no se han cerrado.

[![variables.jpg](https://i.postimg.cc/kXbrvSfh/variables.jpg)](https://postimg.cc/56bkxXcw)

# Desempeño del modelo

A modo de ejemplo, se muestra las ventas totales reales y predichas durante una semana, para el item_8 en 3 tiendas distintas. Es posible observar que el valor predicho se acerca bastante a la ventas observada en la tienda 1 y 5, a diferencia de lo que sucede en la tienda 3 donde no se alcanza a emular las ventas máximas, esto podría deberse a la estrategías de ventas que se realizan particularmente en esta tienda, como por ejemplo la creación de ofertas para lograr mayores ventas, que serán incluidos en la construcción de un próximo modelo.

[![resultados.png](https://i.postimg.cc/mk0dxc82/resultados.png)](https://postimg.cc/1Vr0w3kL)

El desempeño del modelo fue medido como el % de registros cuyo error porcentual de las ventas predichas es menor a un 10% a la del valor real.
 
Error porcentual = (valor estimado - valor real) / valor real × 100% (en valor absoluto)

[![Sin-t-tulo.jpg](https://i.postimg.cc/HW943vyK/Sin-t-tulo.jpg)](https://postimg.cc/z33gGjpS)

Los resultados indican que en construcción (train) el modelo muestra una alta capacidad predictiva, se puede observar que el 90% de los registros tienen un error porcentual menor al 10%. Por otro lado, durante la validación se observa que el 63% de los registros tienen un error porcentual menor al 10% alcanzando un 84% con un 15% de error porcentual y al 95% con un error porcentual del 20%. Lo cual indicaría un leve sobreajuste pero el modelo está siendo altamente eficiente.

Para asegurar la robustes del modelo se evaluó el desempeño del modelo sobre todo el periodo 2017 – 2018 (test). Los resultados mostraron ser altamente consistente con los logrados durante la validación, por lo cual, se sostiene que el modelo tiene una alta capacidad predictiva, es robusto y tiene poco sobre ajuste, por lo cual, puede ser llevado a producción.

