import logging
from dag import DAG

class Ejecutor:
    def __init__(self, dag):
        self.dag = dag
        self.logger = logging.getLogger(self.__class__.__name__)

    def ejecutar(self, tarea_final):
        self.logger.info(f"Ejecutando DAG {self.dag.dag_id}")
        self.dag.ejecutar(tarea_final)
