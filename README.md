# Proyecto de Ejecución de DAGs con Tareas en Paralelo y Secuenciales

Este proyecto implementa un sistema de ejecución de DAGs (Directed Acyclic Graphs) con tareas paralelas y secuenciales utilizando Python. A continuación, se describen las características del sistema y su configuración.

DAG (Directed Acyclic Graph) es una estructura que define un conjunto de tareas y sus dependencias. Esencialmente, es una colección de todas las tareas que se desea ejecutar, organizadas de tal manera que reflejan sus relaciones y el orden en que deben ser ejecutadas. Aquí hay una descripción más detallada:

Definición de un DAG
- Directed (Dirigido): Cada tarea dentro del DAG tiene una dirección específica, es decir, una tarea puede depender de una o varias tareas anteriores, pero no puede depender de ninguna tarea posterior.

- Acyclic (A-cíclico): No se permiten ciclos en el gráfico. Una tarea no puede depender, directa o indirectamente, de sí misma.

- Graph (Gráfico): La estructura del DAG se puede visualizar como un gráfico en el que los nodos representan tareas y las aristas representan las dependencias entre estas tareas.

## Características del Proyecto

### Importaciones y Dependencias

El sistema utiliza módulos y clases especializados para manejar la ejecución de DAGs y tareas. Las importaciones clave incluyen:

- `Scheduler`: Clase responsable de la programación y gestión del tiempo de ejecución de las tareas.
- `Worker`: Clase que representa a los trabajadores que ejecutan las tareas dentro de los DAGs.
- `DAG`: Clase que define la estructura y relaciones de dependencia entre tareas.
- `ExperimentManager`: Clase para gestionar experimentos y tareas específicas.
- `Task`: Clases que representan diversas tareas personalizadas, como `TareaHola`, `TareaDependiente`, `EntrenarModelo`, entre otras.

### Configuración de DAGs

Se configuran varios DAGs para diferentes propósitos:

1. **DAG de Ejemplo 1**: Incluye tareas de saludo, dependientes y tareas paralelas que culminan en una tarea final.
2. **DAG de Ejemplo 2**: Inicia con una tarea inicial, sigue con una tarea paralela y finaliza con una tarea final.
3. **DAG de Ejemplo 3**: Similar al DAG 2, pero con diferentes tareas iniciales y paralelas.
4. **DAG para Entrenamiento de Modelos**: Incluye DAGs específicos para entrenar modelos de prueba y modelos de producción.

### Dependencias entre Tareas

Cada DAG define dependencias entre sus tareas, asegurando que ciertas tareas no se ejecuten hasta que otras hayan sido completadas. Esto se logra a través de métodos que agregan dependencias específicas entre tareas.

### Creación de Trabajadores

Para cada DAG, se crea un `Worker` (trabajador) que será responsable de ejecutar las tareas definidas en el DAG correspondiente.

### Programación de la Ejecución

El `Scheduler` (programador) se utiliza para programar la ejecución de los trabajadores en momentos específicos. Cada trabajador se programa para comenzar a ejecutar su DAG en una hora y fecha definidas.

### Ejecución Directa y Secuencial

El sistema permite tanto la ejecución directa de un DAG como la ejecución secuencial con dependencias definidas. Esto proporciona flexibilidad para ejecutar tareas inmediatamente o en un orden específico basado en dependencias.

### Inicio de la Ejecución

El `Scheduler` se inicia con un intervalo definido, permitiendo la ejecución periódica y continua de los DAGs programados.

## Conclusión

Este proyecto proporciona un sistema robusto y flexible para la gestión y ejecución de flujos de trabajo complejos mediante el uso de DAGs. Permite definir tareas y dependencias, programar su ejecución y gestionar experimentos de manera eficiente.
