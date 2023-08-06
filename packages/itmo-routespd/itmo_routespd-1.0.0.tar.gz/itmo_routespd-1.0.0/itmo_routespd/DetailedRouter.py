from functools import reduce
from typing import Iterator, List, Tuple, Optional, Dict, Any

from .Data import Data
from .dijkstra import Node, Graph
from .funcs import get_rpd_id, get_fields_of_studies4rpd


class DetailedRouter:
    """
    Класс для построения детального маршрута для заданной РПД для абитуриента.
    """

    def __init__(self, data: Data):
        super().__init__()

        self._data = data

        self.__reset_params__()

    def __reset_params__(self):
        self.__graph_data = []

    def _get_nodes(self) -> List:
        return list(set(map(
            lambda x: Node(x),
            filter(
                lambda x: isinstance(x, int),
                reduce(
                    lambda x, y: x + y,
                    self.__graph_data,
                ),
            ),
        )))

    def _get_graph(self, nodes: List[Node]) -> Graph:
        graph = Graph.create_from_nodes(nodes)
        for relation in self.__graph_data:
            graph.connect(
                self._get_node(relation[1], nodes),
                self._get_node(relation[0], nodes),
                1 - relation[2],
            )

        return graph

    @staticmethod
    def _get_routes_from(graph: Graph, start_node: Node) -> List[Tuple[float, List[Dict[str, Any]]]]:
        return [(
            weight,
            [n.data for n in nodes],
        ) for weight, nodes in graph.dijkstra(start_node) if len(nodes) > 1]

    @staticmethod
    def _get_node(node_id: int, nodes: List[Node]) -> Node:
        return list(filter(lambda x: x.data == node_id, nodes))[0]

    def get_short_routes(self, rpd_title: str, threshold: float, routes_count: int) -> Optional[Iterator]:
        """
        Метод для построения детального маршрута для заданной РПД для абитуриента.

        :param rpd_title: название РПД
        :param threshold: порог для коэффициента покрытия связи в графе между РПД. Чем больше порог,
            тем меньше связей будет доступно
        :param routes_count: ограничение по максимальному количеству маршрутов в выдаче
        :return: упорядоченный генератор списка маршрутов к РПД
        """

        assert isinstance(rpd_title, str) and rpd_title in self._data.rpd_names.values()
        assert isinstance(threshold, float) and 0 < threshold < 1
        assert isinstance(routes_count, int) and routes_count > 0

        self.__graph_data.extend([relation for relation in self._data.graph_data if relation[2] >= threshold])

        nodes = self._get_nodes()
        graph = self._get_graph(nodes)

        try:
            start_node = self._get_node(get_rpd_id(rpd_title, self._data.rpd_names), nodes)
        except IndexError:
            return

        routes = sorted(self._get_routes_from(graph, start_node), key=lambda x: x[0])[: routes_count]

        for route in routes:
            yield dict(
                count=len(route[1]),
                rate=round(route[0], 2),
                route=list(map(
                    lambda x: dict(
                        rpd_id=x,
                        rpd_title=self._data.rpd_names[x],
                        fields_of_studies=get_fields_of_studies4rpd(x, self._data),
                    ),
                    route[1][::-1]),
                ),
            )
