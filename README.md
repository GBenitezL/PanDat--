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
Agregué los puntos neurálgicos para IF, IF-ELSE, WHILE y FOR, en los cuales se modifican los stacks declarados en el avance anterior. Utilicé casi la misma ubicación para los puntos neurálgicos que vimos en clase, los cuales hacen uso de las operaciones GOTO, GOTOF y GOTOV.

## Avance #5
Agregué los puntos neurálgicos para las funciones, las cuales utilizan la variable global "current_scope" para agregar las variables y parámetros de las funciones a al directorio de cada función respectivamente. Si la función regresa un valor, este se guarda en una variable temporal para permitir la recursión.

## Avance #6
Diseñé el mapa de memoria. El diseño es muy simple; se guardan en un diccionario los contadores para cada tipo de memoria (global, local, temporal), así como para constantes y pointers. Cada tipo de memoria tiene un contador distinto para cada tipo de variable, con excepción de los pointers que solo aceptan enteros. Modifiqué los puntos neurálgicos existentes para obtener esta funcionalidad.

## Avance #7
Por cuestiones de tiempo, decidí implementar arreglos de una dimensión únicamente (que pueden llegar a cambiar, dependiendo del tiempo). Se usa la variable global "is_array" para asignarle a cada variable un booleano que indica si es un arreglo, y esta información se almacena en el directorio de la variable. Modifiqué la gramática para agregar nuevas funciones estadísticas, las cuales están pensadas para arreglos de una dimensión.

## Avance #8
Agregué todas las funciones de la máquina virtual, incluyendo las funciones estadísticas. La máquina virtual cuenta con un stack de memorias para manejar las llamadas de las funciones. Se crea una "memoria" (que es en realidad un diccionario) cada vez que se llama a una función, y de esta manera no mezclar contextos. En ejecución, se leen cada uno de los cuádruplos, y se realizan acciones según sus códigos de operaciones.