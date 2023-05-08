# PanDat--
Compilador para el Lenguaje PanDat--, un lenguaje con funcionalidad básica, que permite hacer análisis estadístico.

## Avance #1
Agregué los analizadores léxicos y sintácticos. Incluí todas las palabras reservadas que se necesitan en el lenguaje (hasta ahora). También agregué el archivo main.py, que se usa para ejecutar el compilador.

## Avance #2
Creé la clase Directory, la cual tiene 2 subclases, Variables y ScopesDirectory. Al agregar un directorio, se verifica que este no exista anteriormente. La clase Variable almacena todas las variables que se encuentran dentro de un scope, y luego se utiliza para inicializar un objeto de tipo ScopesDirectory.
También definí las consideraciones semánticas del lenguaje. Utilicé un diccionario con una índice compuesto por 3 llaves. La primera es el operador, y las otras 2 son los tipos de los operandos. Se utiliza para buscar eficientemente el tipo del valor que debe regresar una operación con 2 operandos. 

## Avance #3
Creé los primeros puntos neurálgicos que facilitan las acciones semánticas a través de la sintaxis. Para esto, hice uso de la librería deque para crear las pilas de variables, operandos, operadores, y saltos, las cuales son variables globales. También creé la clase cuádruplos, la cual almacena el operando, los operadores y resultados. Con esto, se generan los cuádruplos de los estatutos y expresiones aritméticas.

## Avance #4
Agruegúe los puntos neurálgicos para IF, IF-ELSE, WHILE y FOR, en los cuales se modifican los stacks declarados en el avance anterior.