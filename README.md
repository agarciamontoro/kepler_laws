# Mecánica Celeste

## Uso
Asegúrate de tener instalado `Python` y la librería de `OpenGL`. La mayoría de las distribuciones de Linux tienen estos paquetes en sus repositorios oficiales.

En Arch Linux, por ejemplo, la siguiente órden es suficiente para instalar todo lo necesario:

```
pacaur -S python python-opengl
```

Para comenzar el programa, ejecuta la siguiente órden:

```
python main.py
```

Se puede mover la escena usando el ratón (haciendo click y moviendo). Además, se puede hacer zoom con la rueda.

Por terminal se imprime una línea por cada instante de tiempo (por cada frame, en realidad) y por cada planeta, indicando:
* Posición
* Valor de la energía
* Momento angular
* Anomalía excéntrica

## Notas:

La fórmula implementada se encuentra en el fichero `planet.py`, en la función `setPos(self, t)`. Se copia aquí también:

```python
def setPos(self, t):
    x_coord = self.semi_major_axis*math.cos(self.u(t))-self.eccentricity
    y_coord = self.semi_major_axis*math.sqrt(1-self.eccentricity**2)*math.sin(self.u(t))
    self.coord = [x_coord, 0.0, y_coord]
    print(t,self.u(t),self.coord)
```

Todo el código de dibujo se ha reciclado de un proyecto para otra asignatura (ver [repositorio en GitHub]((https://github.com/agarciamontoro/leap-motion-project) para más detalles).

Falta calcular los radios de los planetas bien y ajustar las escalas de visualización para que se vea bien todo, además de dibujar las elipses enteras.

## Trabajo del día 3 de diciembre
Se ha implementado Newton-Raphson, cuyo código es el siguiente:

```python
def NR(self,phi,u_0=math.pi,tol=0.00001):
    prev = u_0
    curr = phi(prev)

    while abs(prev - curr) >= tol:
        prev = curr
        curr = phi(prev)

    return curr
```

Esta función recibe la función `phi`, que está definida así:
```python
def build_phi(self,epsilon,xi):
    def phi(u):
        return (epsilon*(math.sin(u)-u*math.cos(u))+xi)/(1-epsilon*math.cos(u))

    return phi
```

Por último, esta función recibe la xi, que está definida como sigue:
```python
def xi(self,t):
    xi = (2*math.pi/self.period)*(t-self.t0)
    return xi
```
