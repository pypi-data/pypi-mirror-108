from gc import collect
from pydantic import BaseModel, root_validator
from typing import Tuple, List, Optional

from .funcs import count_weight


class Data(BaseModel):
    """
    Датакласс, хранящий все данные и гиперпараметры для построения маршрутов
    """

    # Перменные для заполнения вручную
    learned: List[int]
    preferred: List[int]

    graph_data: Tuple[Tuple[int, int, float]]

    # select id, title from public.workprogramsapp_workprogram;
    rpd_selection: List[Tuple[int, str]]

    # select id, name from public.dataprocessing_items;
    items_selection: List[Tuple[int, str]]

    # select item_id, workprogram_id from public.workprogramsapp_prerequisitesofworkprogram;
    prerequisites_selection: List[Tuple[int, int]]

    # select item_id, workprogram_id from public.workprogramsapp_outcomesofworkprogram;
    postrequisites_selection: List[Tuple[int, int]]

    # select work_program_id, work_program_change_in_discipline_block_module_id
    # from public.workprogramsapp_workprograminfieldofstudy;
    rpd_in_field_of_study_selection: List[Tuple[int, int]]

    # select id, discipline_block_module_id from workprogramsapp_workprogramchangeindisciplineblockmodule;
    rpd_change_in_rpd_block_module_selection: List[Tuple[int, int]]

    # select id, descipline_block_id from workprogramsapp_disciplineblockmodule;
    rpd_block_module_selection: List[Tuple[int, int]]

    # select id, academic_plan_id from workprogramsapp_disciplineblock;
    rpd_block_selection: List[Tuple[int, int]]

    # select id from workprogramsapp_academicplan;
    academic_plan_selection: List[Tuple[int]]

    # select academic_plan_id, id from workprogramsapp_implementationacademicplan;
    implementation_academic_plan_selection: List[Tuple[int, int]]

    # select implementationacademicplan_id, fieldofstudy_id
    # from workprogramsapp_implementationacademicplan_field_of_study;
    m2m_implementation_academic_plan2field_of_study_selection: List[Tuple[int, int]]

    # select id, number, qualification, title, faculty from workprogramsapp_fieldofstudy_table;
    workprogramsapp_fieldofstudy_selection: List[Tuple[int, str, str, str, Optional[str]]]

    # Внутренние переменные, задаваемые автоматически
    rpd_names: dict = {}
    items_names: dict = {}
    prerequisites: dict = {}
    postrequisites: dict = {}
    rpd_in_field_of_study: Tuple[Tuple[int, int]] = ()
    rpd_change_in_rpd_block_module: Tuple[Tuple[int, int]] = ()
    rpd_block_module: Tuple[Tuple[int, int]] = ()
    rpd_block: Tuple[Tuple[int, int]] = ()
    academic_plan: Tuple[int] = ()
    implementation_academic_plan: Tuple[Tuple[int, int]] = ()
    m2m_implementation_academic_plan2field_of_study: Tuple[Tuple[int, int]] = ()
    workprogramsapp_fieldofstudy: Tuple[Tuple[int, str, str, str, str]] = ()

    graph_data: Tuple[Tuple[int, int, float]] = ()

    @root_validator
    def prepare_data(cls, values):
        for rpd_id, rpd_title in values['rpd_selection']:
            values['rpd_names'][rpd_id] = rpd_title

        for item_id, item_name in values['items_selection']:
            values['items_names'][item_id] = item_name

        for rpd_id, _ in values['rpd_selection']:
            values['prerequisites'][rpd_id] = []
            values['postrequisites'][rpd_id] = []

        for item_id, rpd_id in values['prerequisites_selection']:
            values['prerequisites'][rpd_id].append(item_id)

        for item_id, rpd_id in values['postrequisites_selection']:
            values['postrequisites'][rpd_id].append(item_id)

        values['rpd_in_field_of_study'] = ((id1, id2) for id1, id2 in values['rpd_in_field_of_study_selection'])
        values['rpd_change_in_rpd_block_module'] = ((id1, id2) for id1, id2 in
                                                    values['rpd_change_in_rpd_block_module_selection'])
        values['rpd_block_module'] = ((id1, id2) for id1, id2 in values['rpd_block_module_selection'])
        values['rpd_block'] = ((id1, id2) for id1, id2 in values['rpd_block_selection'])
        values['academic_plan'] = (id1 for id1 in values['academic_plan_selection'])
        values['implementation_academic_plan'] = ((id1, id2) for id1, id2 in
                                                  values['implementation_academic_plan_selection'])
        values['m2m_implementation_academic_plan2field_of_study'] = ((id1, id2) for id1, id2 in values[
            'm2m_implementation_academic_plan2field_of_study_selection'])
        values['workprogramsapp_fieldofstudy'] = ((id1, number, qualification, title, faculty) for
                                                  id1, number, qualification, title, faculty in
                                                  values['workprogramsapp_fieldofstudy_selection'])

        values['graph_data'] = []
        for from_rpd_id, from_rpd_postrequisites in values['postrequisites'].items():
            for to_rpd_id, to_rpd_prerequisites in values['prerequisites'].items():
                if from_rpd_id == to_rpd_id:
                    continue
                weight = count_weight(from_rpd_postrequisites, to_rpd_prerequisites)
                if weight:
                    values['graph_data'].append((from_rpd_id, to_rpd_id, weight))
        values['graph_data'] = tuple(values['graph_data'])

        del values['rpd_selection']
        del values['items_selection']
        del values['prerequisites_selection']
        del values['postrequisites_selection']
        del values['rpd_in_field_of_study_selection']
        del values['rpd_change_in_rpd_block_module_selection']
        del values['rpd_block_module_selection']
        del values['rpd_block_selection']
        del values['academic_plan_selection']
        del values['implementation_academic_plan_selection']
        del values['m2m_implementation_academic_plan2field_of_study_selection']
        del values['workprogramsapp_fieldofstudy_selection']
        collect()

        return values
