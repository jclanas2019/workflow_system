import luigi
import time
import os
import sqlite3
import logging
import random
from datetime import datetime
from config import OUTPUT_DIR
from logging_config import configurar_logging
from experiment_manager import ExperimentManager
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

configurar_logging()
logger = logging.getLogger(__name__)
experiment_manager = ExperimentManager()

def log_task_execution(dag_id, task_name, task_type, start_time, end_time, duration):
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO monitoring (dag_id, task_name, task_type, start_time, end_time, duration)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (dag_id, task_name, task_type, start_time, end_time, duration))
    conn.commit()
    conn.close()
    logger.info(f"Logged task execution: {dag_id, task_name, task_type, start_time, end_time, duration}")

class MonitoredTask(luigi.Task):
    def run_task(self, dag_id, task_type):
        experiment_id = experiment_manager.create_experiment()
        experiment_manager.log_params(experiment_id, {"dag_id": dag_id, "task_name": self.__class__.__name__, "task_type": task_type})
        
        start_time = datetime.now()
        logger.debug(f"Task {self.__class__.__name__} started at {start_time}")
        self.run()
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.debug(f"Task {self.__class__.__name__} ended at {end_time} with duration {duration}")
        log_task_execution(dag_id, self.__class__.__name__, task_type, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"), duration)
        
        experiment_manager.log_metrics(experiment_id, {"start_time": start_time, "end_time": end_time, "duration": duration})
        # Save output as artifact
        experiment_manager.save_artifact(experiment_id, self.output().path)
        
        # Example of saving a model (mock example, assuming self.model_path and self.model_name are defined)
        if hasattr(self, 'model_path') and hasattr(self, 'model_name'):
            experiment_manager.log_model(experiment_id, self.model_path, self.model_name, stage="test")

class TareaHola(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'hola.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('¡Hola, Mundo!')
        print("¡Hola, Mundo!")

class TareaDependiente(MonitoredTask):
    def requires(self):
        return TareaHola()

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'dependiente.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Esta tarea depende de la primera tarea.')
        print("Esta tarea depende de la primera tarea.")

class TareaParalela1(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'paralela1.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea paralela 1 completada.')
        print("Tarea paralela 1 completada.")

class TareaParalela2(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'paralela2.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea paralela 2 completada.')
        print("Tarea paralela 2 completada.")

class TareaFinal(MonitoredTask):
    def requires(self):
        return [TareaParalela1(), TareaParalela2(), TareaDependiente()]

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'final.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea final completada después de tareas paralelas y dependientes.')
        print("Tarea final completada después de tareas paralelas y dependientes.")

# Nuevas tareas para los nuevos flujos de trabajo
class TareaInicial2(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'inicial2.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea inicial 2 completada.')
        print("Tarea inicial 2 completada.")

class TareaParalela3(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'paralela3.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea paralela 3 completada.')
        print("Tarea paralela 3 completada.")

class TareaFinal2(MonitoredTask):
    def requires(self):
        return [TareaInicial2(), TareaParalela3()]

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'final2.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea final 2 completada.')
        print("Tarea final 2 completada.")

class TareaInicial3(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'inicial3.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea inicial 3 completada.')
        print("Tarea inicial 3 completada.")

class TareaParalela4(MonitoredTask):
    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'paralela4.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea paralela 4 completada.')
        print("Tarea paralela 4 completada.")

class TareaFinal3(MonitoredTask):
    def requires(self):
        return [TareaInicial3(), TareaParalela4()]

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'final3.txt'))

    def run(self):
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Tarea final 3 completada.')
        print("Tarea final 3 completada.")

# Ejemplo de tareas que entrenan y guardan modelos
class EntrenarModelo(MonitoredTask):
    model_path = os.path.join(OUTPUT_DIR, 'model.pkl')
    model_name = 'model.pkl'

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'entrenar_modelo.txt'))

    def run(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, self.model_path)
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Modelo entrenado y guardado.')
        print("Modelo entrenado y guardado.")

class EntrenarModeloProduccion(MonitoredTask):
    model_path = os.path.join(OUTPUT_DIR, 'model_produccion.pkl')
    model_name = 'model_produccion.pkl'

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_DIR, 'entrenar_modelo_produccion.txt'))

    def run(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, self.model_path)
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        with self.output().open('w') as f:
            f.write('Modelo de producción entrenado y guardado.')
        print("Modelo de producción entrenado y guardado.")

    def run_task(self, dag_id, task_type):
        super().run_task(dag_id, task_type)
        # Guardar el modelo en producción
        experiment_id = experiment_manager.create_experiment()
        experiment_manager.log_model(experiment_id, self.model_path, self.model_name, stage="production")
