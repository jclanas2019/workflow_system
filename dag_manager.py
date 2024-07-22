import logging
from dag import DAG

class DAGManager:
    def __init__(self):
        self.dags = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def agregar_dag(self, dag_id):
        if dag_id in self.dags:
            self.logger.warning(f"DAG con ID {dag_id} ya existe.")
        else:
            self.dags[dag_id] = DAG(dag_id)
            self.logger.info(f"DAG con ID {dag_id} ha sido creado.")
        return self.dags[dag_id]

    def eliminar_dag(self, dag_id):
        if dag_id in self.dags:
            del self.dags[dag_id]
            self.logger.info(f"DAG con ID {dag_id} ha sido eliminado.")
        else:
            self.logger.warning(f"DAG con ID {dag_id} no existe.")

    def modificar_dag(self, dag_id, nuevo_dag_id):
        if dag_id in self.dags:
            self.dags[nuevo_dag_id] = self.dags.pop(dag_id)
            self.dags[nuevo_dag_id].dag_id = nuevo_dag_id
            self.logger.info(f"DAG con ID {dag_id} ha sido modificado a {nuevo_dag_id}.")
        else:
            self.logger.warning(f"DAG con ID {dag_id} no existe.")

    def obtener_dag(self, dag_id):
        return self.dags.get(dag_id, None)
