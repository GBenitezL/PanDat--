# *PanDat--*
## *Compilador para el Lenguaje PanDat--*
## Manual de Usuario

El lenguaje PanDat-- es un lenguaje de programación enfocado en el paradigma imperativo procedural. Cuenta con funciones básicas de muchos lenguajes modernos, y además permite hacer análisis estadísticos muy fácilmente gracias a sus funciones pre-definidas, así como generar gráficos.

### Dependencias
Antes de poder usar el lenguaje PanDat--, requieres instalar una versión de Python superior a la 3.6. Te dejo el link a la versión actual:

https://www.python.org/downloads/

Una vez que tengas instalado python, corre el siguiente comando en tu terminal para instalar todas las librerías necesarias:
```
pip install matplotlib seaborn
```

### Estructura de un programa
Todos los programas en el lenguaje PanDat-- requiren usar la palabra reservada 'program' seguida de un identificador.
```
program nombre_programa;
```

Luego, se pueden declarar variables globales, aunque no es necesario.

Después, se puede hacer la declaración de funciones. Por último, se debe declarar una función 'main' de esta manera:

```
main()
{

}
```

Todo el código que se vaya a ejecutar debe empezar desde el contexto de 'main'. Por esto, la función 'main' debe ser la última que se declare. 

### Variables soportadas
- int
- char
- float
- bool

### Declaración de variables
Las variables deben de ser declaradas justo debajo del contexto al que pertenecen, y antes de abrir 
los corchetes.

Se pueden definir múltiples variables a la vez utilizando comas, pero estas deben de ser del mismo tipo. Para declarar un arreglo de cualquier tipo, se debe especificar su tamaño. 

Este es un ejemplo
```
main()
var variable1: bool;
var variable2, variable3: int;
var a, b, c: float[10];
{
    resto del codigo...
}

```
### Operaciones

#### Operaciones Aritméticas
- +: suma
- -: resta
- *: multiplicación
- /: división

#### Operaciones de Comparación
- <: menor
- \>: mayor
- <=: menor o igual
- \>=: mayor o igual
- ==: igual
- !=: diferente

#### Operaciones Booleanas
- &&: and
- ||: or

### Ciclos

#### While
El ciclo while ejecuta un segmento de código hasta que la condición de control sea falsa.
```
while (i < 10) {
    print(i);
    i = i + 1;
}
```

#### For
El ciclo for consta de 3 partes, una asignación a una variable de control, una condición, y un incremento para la variable de control (número entero). 
```
for (i = 0; i < 10; 1) {
    print(i);
}
```

### Funciones
#### Declaracion
Para declarar una función, se utiliza la plabra reservada 'function' seguida de un valor de retorno, el cual puede ser void (no regresa nada), y luego un par de paréntesis en el que se definen las variables que la función utiliza como parámetros, y sus tipos. Si la función es de cualquier tipo distinto a void, se requiere un estatuto de 'return' para regresar el resultado de la función.
```
function func1: int(number1: int, number2: int){
    return (number1 + number2);
}

function func2: void(letter: char){
    print("Number: ", number);
}
```
#### Llamado
```
variable = func1(2, 4);
func2('x');

```

### Funciones principales
```
print(expresion) --imprime en consola
read(valor) --lee una entrada
rand(limite_inferior, limite_superior) --genera un número aleatorio entre el parámetro 1 y el 2
```

### Funciones Especiales 

#### Un solo arreglo
```
mean(arreglo)
median(arreglo)
variance(arreglo)
std(arreglo)
sum(arreglo)
count(arreglo)
iqr(arreglo)
```

#### Dos arreglos (del mismo tamaño)
```
corr(arreglo1, arreglo2)
regression(arreglo1, arreglo2)
```

#### Sets (dos arreglos del mismo tamaño)
```
union(arreglo1, arreglo2)
diff(arreglo1, arreglo2)
intersect(arreglo1, arreglo2)
```

### Gráficas

#### Un solo arreglo
```
histplot(arreglo)
boxplot(arreglo)
```

#### Dos arreglos (del mismo tamaño)
```
scatterplot(arreglo1, arreglo2)
lineplot(arreglo1, arreglo2)
barplot(arreglo1, arreglo2)
```
