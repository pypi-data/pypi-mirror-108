from typing import Any, Iterator, Dict, Optional, List


def intersected_prerequisites(rpd_index: int, learned_items: list, prerequisites: dict) -> list:
    """
    Общие темы среди пререквизитов РПД и уже освоенных

    :param rpd_index: ID РПД
    :param learned_items: освоенные темы
    :param prerequisites: пререквизиты всех РПД
    :return: список общих тем
    """

    _prerequisites = prerequisites[rpd_index]

    return list(set(_prerequisites).intersection(set(learned_items)))


def intersected_postrequisites(rpd_index: int, preferred_items: list, postrequisites: dict) -> list:
    """
    Общие темы среди постреквизитов РПД и желаемых тем

    :param rpd_index: ID РПД
    :param preferred_items: желаемые темы
    :param postrequisites: постреквизиты всех РПД
    :return: список общих тем
    """

    _postrequisites = postrequisites[rpd_index]

    return list(set(_postrequisites).intersection(set(preferred_items)))


def count_base_coefficient(rpd_index: int, learned_items: list, prerequisites: dict) -> float:
    """
    Функция вычисления коэффициента покрытия знания пререквизитов на основании освоенных тем

    :param rpd_index: ID РПД
    :param learned_items: освоенные темы
    :param prerequisites: пререквизиты всех РПД
    :return: коэффициент покрытия
    """

    _prerequisites = prerequisites[rpd_index]

    return round(len(intersected_prerequisites(rpd_index, learned_items, prerequisites)) / len(_prerequisites),
                 3) if _prerequisites else .0


def count_prefer_coefficient(rpd_index: int, preferred_items: list, postrequisites: dict) -> float:
    """
    Функция вычисления коэффициента покрытия общей желаемости постреквизитов на основании желаемых тем

    :param rpd_index: ID РПД
    :param preferred_items: желаемые темы
    :param postrequisites: постреквизиты всех РПД
    :return: коэффициент покрытия
    """

    _postrequisites = postrequisites[rpd_index]

    return round(len(intersected_postrequisites(rpd_index, preferred_items, postrequisites)) / len(_postrequisites),
                 3) if _postrequisites else .0


def count_weight(from_postrequisites: list, to_prerequisites: list) -> float:
    """
    Функция вычисления веса ребра в графе для алгоритма построения детального маршрута к РПД

    :param from_postrequisites: постреквизиты начальной вершины
    :param to_prerequisites: пререквизиты конечной вершины
    :return: вес ребра
    """

    from_postrequisites = set(from_postrequisites)
    to_prerequisites = set(to_prerequisites)

    intersected_count = len(from_postrequisites.intersection(to_prerequisites))
    united_count = len(from_postrequisites.union(to_prerequisites))

    return round(intersected_count / united_count, 3) if united_count else .0


def get_rpd_id(title: str, rpd_names: Dict[int, str]) -> Optional[int]:
    """
    Функция получения ID РПД по его названию

    :param title: название РПД
    :param rpd_names: хэш-таблица названий РПД
    :return: ID РПД или None
    """

    try:
        return [rpd_id for rpd_id, rpd_title in rpd_names.items() if rpd_title == title][0]
    except IndexError:
        pass


def preferred_rpd_list(preferred_items: list, postrequisites: dict, data, count: int) -> Iterator[Dict]:
    """
    Функция получения списка наиболее желаемых РПД на основании списка желаемых тем без учёта освоенных тем

    :param preferred_items: желаемые темы
    :param postrequisites: постреквизиты всех РПД
    :param data: объект, хранящий все исходные данные из БД и гипер параметры
    :param count: максимальное количество РПД в выдаче
    :return: упорядоченный генератор РПД
    """

    selection = list(map(
        lambda x: (x, count_prefer_coefficient(x, preferred_items, postrequisites)),
        postrequisites.keys(),
    ))
    selection = sorted(selection, key=lambda x: x[1], reverse=True)[: count]

    for rpd, coefficient in selection:
        yield dict(
            rpd_id=rpd,
            rpd_title=data.rpd_names[rpd],
            fields_of_studies=get_fields_of_studies4rpd(rpd, data),
            rate=coefficient,
            common_items=intersected_postrequisites(rpd, preferred_items, postrequisites),
        )


def get_fields_of_studies4rpd(rpd: Any, data, is_id=True) -> List[Dict]:
    """
    Функция получения направлений подготовки для заданной РПД

    :param rpd: ID или название РПД
    :param data: объект, хранящий все исходные данные из БД и гипер параметры
    :param is_id: является ли rpd ID. В обратном случае rpd является названием
    :return: список направлений подготовки
    """

    rpd_id = rpd if is_id else get_rpd_id(rpd, data.rpd_names)

    rpd_change_in_rpd_block_module_id_list = list(
        map(lambda x: x[1], filter(lambda x: x[0] == int(rpd_id), data.rpd_in_field_of_study)))

    rpd_block_module_id_list = list(map(
        lambda x: x[1],
        filter(lambda x: x[0] in rpd_change_in_rpd_block_module_id_list, data.rpd_change_in_rpd_block_module)
    ))

    descipline_block_id_list = list(
        map(lambda x: x[1], filter(lambda x: x[0] in rpd_block_module_id_list, data.rpd_block_module))
    )

    academic_plan_id_list = list(
        map(lambda x: x[1], filter(lambda x: x[0] in descipline_block_id_list, data.rpd_block))
    )

    implementation_academic_plan_id_list = list(
        map(lambda x: x[1], filter(lambda x: x[0] in academic_plan_id_list, data.implementation_academic_plan)))

    field_of_study_id_list = list(map(lambda x: x[1], filter(lambda x: x[0] in implementation_academic_plan_id_list,
                                                             data.m2m_implementation_academic_plan2field_of_study)))

    field_of_study_list = filter(lambda x: x[0] in field_of_study_id_list, data.workprogramsapp_fieldofstudy)

    fos_list = []

    for fos in field_of_study_list:
        fos_list.append(dict(
            field_of_study_name=fos[3],
            field_of_study_code=fos[1],
            faculty=fos[4],
            level=fos[2],
        ))

    return fos_list
