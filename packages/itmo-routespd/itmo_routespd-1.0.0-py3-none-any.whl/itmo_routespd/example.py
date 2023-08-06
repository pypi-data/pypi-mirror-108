"""
from json import dumps
import psycopg2

from itmo_routespd import Data, BaseRouter, DetailedRouter
from itmo_routespd.funcs import preferred_rpd_list, get_fields_of_studies4rpd


conn = psycopg2.connect(
    user='postgres',
    password='some_pass',
    host='127.0.0.1',
    port='5432',
    database='analytics_db',
)
cursor = conn.cursor()

rpd_table = 'public.workprogramsapp_workprogram'
items_table = 'public.dataprocessing_items'
ppk_table = 'public.workprogramsapp_prerequisitesofworkprogram'
rpk_table = 'public.workprogramsapp_outcomesofworkprogram'
rpd_in_field_of_study_table = 'public.workprogramsapp_workprograminfieldofstudy'
rpd_change_in_rpd_block_module_table = 'public.workprogramsapp_workprogramchangeindisciplineblockmodule'
rpd_block_module_table = 'public.workprogramsapp_disciplineblockmodule'
rpd_block_table = 'public.workprogramsapp_disciplineblock'
academic_plan_table = 'public.workprogramsapp_academicplan'
implementation_academic_plan_table = 'public.workprogramsapp_implementationacademicplan'
m2m_implementation_academic_plan2field_of_study_table = 'public.workprogramsapp_implementationacademicplan_field_of_study'
workprogramsapp_fieldofstudy_table = 'public.workprogramsapp_fieldofstudy'

cursor.execute(f'select id, title from {rpd_table};')
rpd_selection = cursor.fetchall()
cursor.execute(f'select id, name from {items_table};')
items_selection = cursor.fetchall()
cursor.execute(f'select item_id, workprogram_id from {rpk_table};')
postrequisites_selection = cursor.fetchall()
cursor.execute(f'select item_id, workprogram_id from {ppk_table};')
prerequisites_selection = cursor.fetchall()
cursor.execute(f'select work_program_id, work_program_change_in_discipline_block_module_id from {rpd_in_field_of_study_table};')
rpd_in_field_of_study_selection = cursor.fetchall()
cursor.execute(f'select id, discipline_block_module_id from {rpd_change_in_rpd_block_module_table};')
rpd_change_in_rpd_block_module_selection = cursor.fetchall()
cursor.execute(f'select id, descipline_block_id from {rpd_block_module_table};')
rpd_block_module_selection = cursor.fetchall()
cursor.execute(f'select id, academic_plan_id from {rpd_block_table};')
rpd_block_selection = cursor.fetchall()
cursor.execute(f'select id from {academic_plan_table};')
academic_plan_selection = cursor.fetchall()
cursor.execute(f'select academic_plan_id, id from {implementation_academic_plan_table};')
implementation_academic_plan_selection = cursor.fetchall()
cursor.execute(f'select implementationacademicplan_id, fieldofstudy_id from {m2m_implementation_academic_plan2field_of_study_table};')
m2m_implementation_academic_plan2field_of_study_selection = cursor.fetchall()
cursor.execute(f'select id, number, qualification, title, faculty from {workprogramsapp_fieldofstudy_table};')
workprogramsapp_fieldofstudy_selection = cursor.fetchall()

if conn:
    cursor.close()
    conn.close()

data = Data(
    learned=[969, 970, 1412, 2042, 2325, 3864, 8832, 12089, 15659, 15696, 15697, 1404, 16356, 1411, 9752, 435, 2369, 2356, 4534, 15632, 5465, 18650, 4573, 9539, 18510, 293, 1027, 7504, 3222, 18662, 18813, 18431, 2396, 18501, 18699, 120, 273, 9556, 2854, 115, 5844, 16214, 18465, 9694, 728, 10318, 18661, 4647, 18449, 992, 6191, 18697, 3109, 9659, 9285, 7246, 18487, 18890, 18655, 18432, 18433, 2910, 18, 18568, 9383, 4600, 327, 2390, 949, 409, 18893, 301, 6205, 18397, 3448],
    preferred=[2, 3, 15, 16, 19, 251, 253, 254, 255, 256, 257, 274, 275, 276, 277, 2096, 8909, 18861, 16638, 1003, 18875, 7538, 9556, 15313, 18592, 17654, 2280, 15340, 4569, 16538, 6560, 121, 337, 6567, 16288],
    rpd_selection=rpd_selection,
    items_selection=items_selection,
    prerequisites_selection=prerequisites_selection,
    postrequisites_selection=postrequisites_selection,
    rpd_in_field_of_study_selection=rpd_in_field_of_study_selection,
    rpd_change_in_rpd_block_module_selection=rpd_change_in_rpd_block_module_selection,
    rpd_block_module_selection=rpd_block_module_selection,
    rpd_block_selection=rpd_block_selection,
    academic_plan_selection=academic_plan_selection,
    implementation_academic_plan_selection=implementation_academic_plan_selection,
    m2m_implementation_academic_plan2field_of_study_selection=m2m_implementation_academic_plan2field_of_study_selection,
    workprogramsapp_fieldofstudy_selection=workprogramsapp_fieldofstudy_selection,
)

for batch in BaseRouter(data).produce(.2, 4, 10):
    print(dumps(batch, indent=4, ensure_ascii=False))

for route in DetailedRouter(data).get_short_routes('Основы технологически адекватного применения пищевых добавок', .01, 10):
    print(dumps(route, indent=4, ensure_ascii=False))

for rpd in preferred_rpd_list(data.preferred, data.postrequisites, data, 10):
    print(dumps(rpd, indent=4, ensure_ascii=False))

for fos in get_fields_of_studies4rpd(12438, data):
    print(dumps(fos, indent=4, ensure_ascii=False))
"""