import logging

class Worker:
    def __init__(self, dag):
        self.dag = dag
        self.logger = logging.getLogger("Worker")

    def start(self):
        self.logger.info(f"Worker starting execution for DAG {self.dag.dag_id}")
        self.dag.ejecutar(next(iter(self.dag.tasks)))
