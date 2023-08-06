class Node:
    """
    Класс, реализующий вершину в графе для использования в алгоритме Дейкстры

    Данное решение является заимствованным
    Источник: https://gist.github.com/micahshute/bc8b45020636d862105543ecb231b9d2#file-adjacency_matrix_graphy-py
    """

    def __init__(self, data, indexloc=None):
        self.data = data
        self.index = indexloc
