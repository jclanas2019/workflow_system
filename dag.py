import logging
import luigi
import networkx as nx
import matplotlib.pyplot as plt
from task import (
    TareaHola, TareaDependiente, TareaParalela1, TareaParalela2, TareaFinal,
    TareaInicial2, TareaParalela3, TareaFinal2,
    TareaInicial3, TareaParalela4, TareaFinal3, MonitoredTask
)

class DAG:
    def __init__(self, dag_id):
        self.dag_id = dag_id
        self.tasks = {}
        self.logger = logging.getLogger(self.dag_id)
        self.graph = nx.DiGraph()
        self.graph.add_node("Worker1")  # Añadir nodo para el primer trabajador
        self.graph.add_node("Worker2")  # Añadir nodo para el segundo trabajador
        self.graph.add_node("Worker3")  # Añadir nodo para el tercer trabajador
        self.graph.add_node("Worker4")  # Añadir nodo para el cuarto trabajador

    def agregar_tarea(self, task, worker, tipo="secuencial"):
        self.tasks[task.__class__.__name__] = task
        self.logger.info(f"Tarea {task.__class__.__name__} agregada al DAG {self.dag_id}")
        self.graph.add_node(task.__class__.__name__, tipo=tipo)
        self.graph.add_edge(worker, task.__class__.__name__)  # Conectar el trabajador con cada tarea

    def agregar_dependencia(self, task, dependency):
        self.graph.add_edge(dependency.__class__.__name__, task.__class__.__name__)
        self.logger.info(f"Dependencia de {dependency.__class__.__name__} a {task.__class__.__name__} agregada al DAG {self.dag_id}")

        # Verificar si se ha introducido un ciclo
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph.remove_edge(dependency.__class__.__name__, task.__class__.__name__)
            raise ValueError("Se ha detectado un ciclo en el DAG. La dependencia no se puede agregar.")

    def visualizar(self):
        pos = nx.spring_layout(self.graph)  # Usar spring_layout para minimizar el cruce de bordes
        node_colors = []
        for node in self.graph.nodes(data=True):
            tipo = node[1].get('tipo', 'secuencial')
            if tipo == 'paralelo':
                node_colors.append((1, 0, 1, 0.5))  # Magenta con 50% de transparencia
            elif tipo == 'final':
                node_colors.append((0, 0, 1, 0.5))  # Azul con 50% de transparencia
            else:
                node_colors.append((0, 1, 0, 0.5))  # Verde con 50% de transparencia
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=2000, font_size=10, font_weight='bold')
        plt.title(f"Grafo del DAG {self.dag_id}")
        plt.show()

    def ejecutar(self, tarea_final):
        self.logger.info(f"Ejecutando DAG {self.dag_id}")
        task = self.tasks[tarea_final]
        if isinstance(task, MonitoredTask):
            task.run_task(self.dag_id, task_type=self.graph.nodes[tarea_final]['tipo'])
        else:
            luigi.build([task], local_scheduler=True)

