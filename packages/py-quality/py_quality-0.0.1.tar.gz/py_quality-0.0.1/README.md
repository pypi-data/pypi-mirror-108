# Marketing Science | Adquality library

Developed by Carlos Trujillo, Marketing Scientist.

## Introduction

Si formas parte del mundo del marketing seguramente has escuchado acerca de Admetricks, Comscore, Lotame o Adquality. Herramientas que nos entregan datos
los cuales podemos utilizar para realizar distintos tipos de estudios a muchos de los fenomenos a los cuales nos enfretamos en el este rubro.

Cada día, la adopción de la tecnologia es más importante que nunca para poder llevar nuestro analisis un poco más allá de lo convencional.
Esto puede representar un reto muy cumplicado, debido a que muchas de las herramientas que utilizamos día a día no tienen habilitadas sus conectores para todos
los usuarios, dando como resultado que no podamos hacer grandes descargas de data.

Y aquellos usuarios que logran obtener un conector hacia alguna de estas plataformas, le espera un gran camino para entender el conector, su operabilidad y
resultados, con la poca información que existe en internet.

Por ello, decidi iniciar pequeños proyectos donde estaré creando pseudo paquetes, para aquellos que estan en el mundo del marketing y la programación. Esperando
poder acortar la curva de adaptación de algunos de los profesionales que nos encontramos aquí.

El primer paquete en este proyecto es PyQuality, una simplificación de la conection a el API REST de Adquality en Python.

¡Espero tu feedback!

``` python

pip install py_adquality
```

Incialmente el paquete cuenta con dos metodos, donde cada uno devuelve un DataFrame. El metodo principal, genera un reporte en formato Pandas donde se ven todos
los datos obtenidos por la API REST de Adquality.

El segundo paquete obtiene todas las imagenes capturadas por Adquality dentro de un periodo determinado.

``` python

adquality = reports(username = 'my_email_or_adquality_user', password = 'my_password')
publishers = adquality.report_generator(country = 'CO', report_type = 'publishers')

#Report options "publishers", "formats", "advertisers", "industries", "sources" or "categories"
```

Tambien puedes generar un reporte con todas las imagenes capturadas por Adquality.

``` python

adquality = reports(username = 'my_email_or_adquality_user', password = 'my_password')
images = adquality.image_extractor(country = 'CO')
```

Muy pronto se estaran añadiendo modulos de aprendizaje automatico para explotar la información que tenemos dentro de la plataforma.

¿Cuales creen que es el mejor modulo con el que podemos empezar?