from functools import reduce
from typing import Iterator

from .Data import Data
from .funcs import count_base_coefficient, count_prefer_coefficient, get_fields_of_studies4rpd, get_rpd_id


class BaseRouter:
    """
    Класс для построения общего маршрута по всем РПД.
    """

    def __init__(self, data: Data):
        super().__init__()

        self._data = data
        self._rpd_id_list = set(data.rpd_names.keys())

        self.__reset_params__()

    def __reset_params__(self):
        self.__learned_items = self._data.learned
        self.__learned_rpd = set()

    @property
    def learned_rpd_count(self) -> int:
        """
        :return: Количество изученных РПД
        """

        return self.__learned_rpd.__len__()

    @property
    def learned_items_count(self) -> int:
        """
        :return: Количество освоенных тем
        """

        return self.__learned_items.__len__()

    def produce(self, threshold: float, iter_count: int, rpd_count: int) -> Iterator:
        """
        Метод для построения общего маршрута по всем РПД для абитуриента.

        :param threshold: порог для коэффициента допущения РПД к рассмотрению. Чем больше, тем меньше РПД пройдёт
        :param iter_count: количество итераций, где каждая представляет собой набор РПД
        :param rpd_count: количество РПД на итерацию
        :return: упорядоченный генератор списка наборов РПД
        """

        self.__reset_params__()

        assert isinstance(threshold, float) and 0 < threshold < 1
        assert isinstance(iter_count, int) and iter_count > 0
        assert isinstance(rpd_count, int) and rpd_count > 0

        for iter_num in range(iter_count):
            selection = list(map(
                lambda x: (x, count_base_coefficient(x, self.__learned_items, self._data.prerequisites)),
                self._rpd_id_list - self.__learned_rpd,
            ))

            available = list(filter(lambda x: x[1] >= threshold, selection))

            selection = list(map(
                lambda x: (x[0], count_prefer_coefficient(x[0], self._data.preferred, self._data.postrequisites)),
                available,
            ))

            selection.sort(key=lambda x: x[1], reverse=True)

            most_preferred = selection[: rpd_count]

            if not selection:
                break

            new_learned = list(filter(
                lambda x: x not in self.__learned_items,
                reduce(
                    lambda x, y: x + y,
                    [self._data.postrequisites[preferred_rpd[0]] for preferred_rpd in most_preferred],
                ),
            ))

            self.__learned_items.extend(new_learned)

            for rpd_id, _ in most_preferred:
                self.__learned_rpd.add(rpd_id)

            rpd_batch = []
            for rpd_details in [(self._data.rpd_names[rpd[0]], rpd[1]) for rpd in most_preferred]:
                rpd_batch.append(dict(
                    rpd_id=get_rpd_id(rpd_details[0], self._data.rpd_names),
                    rpd_title=rpd_details[0],
                    preferred_coefficient=rpd_details[1],
                    fields_of_studies=get_fields_of_studies4rpd(rpd_details[0], self._data, is_id=False),
                ))

            yield dict(
                learned_items_count=self.learned_items_count,
                learned_rpd_count=self.learned_rpd_count,
                rpd_batch=rpd_batch,
            )
