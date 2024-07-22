from scheduler import Scheduler
from worker import Worker
from dag import DAG
from task import (
    TareaHola, TareaDependiente, TareaParalela1, TareaParalela2, TareaFinal,
    TareaInicial2, TareaParalela3, TareaFinal2, TareaInicial3, TareaParalela4, TareaFinal3,
    EntrenarModelo, EntrenarModeloProduccion
)
from experiment_manager import ExperimentManager

experiment_manager = ExperimentManager()

# Configurar y agregar tareas al DAG
dag1 = DAG("dag_ejemplo_1")
dag1.agregar_tarea(TareaHola(), "Worker1")
dag1.agregar_tarea(TareaDependiente(), "Worker1")
dag1.agregar_tarea(TareaParalela1(), "Worker1", tipo="paralelo")
dag1.agregar_tarea(TareaParalela2(), "Worker1", tipo="paralelo")
dag1.agregar_tarea(TareaFinal(), "Worker1", tipo="final")

dag1.agregar_dependencia(TareaHola(), TareaDependiente())
dag1.agregar_dependencia(TareaParalela1(), TareaFinal())
dag1.agregar_dependencia(TareaParalela2(), TareaFinal())
dag1.agregar_dependencia(TareaDependiente(), TareaFinal())

dag2 = DAG("dag_ejemplo_2")
dag2.agregar_tarea(TareaInicial2(), "Worker2")
dag2.agregar_tarea(TareaParalela3(), "Worker2", tipo="paralelo")
dag2.agregar_tarea(TareaFinal2(), "Worker2", tipo="final")

dag2.agregar_dependencia(TareaInicial2(), TareaFinal2())
dag2.agregar_dependencia(TareaParalela3(), TareaFinal2())

dag3 = DAG("dag_ejemplo_3")
dag3.agregar_tarea(TareaInicial3(), "Worker3")
dag3.agregar_tarea(TareaParalela4(), "Worker3", tipo="paralelo")
dag3.agregar_tarea(TareaFinal3(), "Worker3", tipo="final")

dag3.agregar_dependencia(TareaInicial3(), TareaFinal3())
dag3.agregar_dependencia(TareaParalela4(), TareaFinal3())

# DAG para entrenar y guardar modelos
dag4 = DAG("dag_modelo_test")
dag4.agregar_tarea(EntrenarModelo(), "Worker4")

dag5 = DAG("dag_modelo_produccion")
dag5.agregar_tarea(EntrenarModeloProduccion(), "Worker5")

# Crear trabajadores y programar la ejecución de los DAGs
trabajador1 = Worker(dag1)
trabajador2 = Worker(dag2)
trabajador3 = Worker(dag3)
trabajador4 = Worker(dag4)
trabajador5 = Worker(dag5)

scheduler = Scheduler()
scheduler.schedule(trabajador1, run_at="2024-07-21 20:35:00")
scheduler.schedule(trabajador2, run_at="2024-07-21 20:36:00")
scheduler.schedule(trabajador3, run_at="2024-07-21 20:38:00")
scheduler.schedule(trabajador4, run_at="2024-07-21 20:40:00")
scheduler.schedule(trabajador5, run_at="2024-07-21 20:42:00")

# Añadir ejecución directa de un DAG
dag_directo = DAG("dag_directo")
dag_directo.agregar_tarea(TareaHola(), "Worker6")
dag_directo.agregar_tarea(TareaDependiente(), "Worker6")
dag_directo.agregar_dependencia(TareaHola(), TareaDependiente())

trabajador_directo = Worker(dag_directo)
trabajador_directo.start()  # Ejecución directa

# Añadir ejecución secuencial con dependencias
dag_secuencial = DAG("dag_secuencial")
dag_secuencial.agregar_tarea(TareaInicial2(), "Worker6")
dag_secuencial.agregar_tarea(TareaDependiente(), "Worker6")
dag_secuencial.agregar_dependencia(TareaInicial2(), TareaDependiente())

trabajador_secuencial = Worker(dag_secuencial)
scheduler.schedule(trabajador_secuencial, run_at="2024-07-21 20:44:00")

# Ejecutar los DAGs programados
scheduler.start(interval=10)
