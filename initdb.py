import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from models import *


department_objects = []
funder_objects = []
expense_objects = []

def run():
    delete_and_migrate_db()
    create_permissions()
    set_timings()
    set_funders()
    set_expenses()
    set_consolidation_groups()
    set_programs_subprograms_deparatments()
    register_AO()
    create_PDU_members()
    create_ordinary_members()
    set_permissions()
    set_planning_timing()


def create_permissions():
    content_type_plan = ContentType.objects.get_for_model(Plan)
    content_type_requisition = ContentType.objects.get_for_model(Requisition)
    permissions = [("Can Prepare Plan", content_type_plan), ("Can Initiate Requisition", content_type_requisition)]
    for permission, content_type in permissions:
        perm = Permission.objects.create(
            codename=permission.lower().replace(' ','_').strip(),
            name=permission,
            content_type=content_type,
            )
        perm.save()

def delete_and_migrate_db():
    os.system('rm db.sqlite3; python3 manage.py migrate;')


def set_timings():
    plan_timing = Timing(process="Planning")
    plan_timing.save()
    inititation_timing = Timing(process="Initiation")
    inititation_timing.save()
    inititation_timing = Timing(process="Bidding")
    inititation_timing.save()
    inititation_timing = Timing(process="Contract")
    inititation_timing.save()
    

def set_funders():
    funders = ["GOU", "ADB", "DAAD"]
    for funder in funders:
        funder = Funder(name=funder, allowed=True)
        funder.save()
        funder_objects.append(funder)


def set_expenses():
    items = [
        {"code": 211101, "name":"General Staff Salaries", "type_of_procurement": "SUPPLIES"},
        {"code": 211102, "name": "Contract Staff Salaries and wages", "type_of_procurement": "WORKS"},
        {"code": 211103, "name": "Allowances", "type_of_procurement": "NON-CONSULTANCY SERVICES"}
    ]
    for item in items:
        expense = Expense(code=item['code'], name=item['name'], type_of_procurement = item["type_of_procurement"])
        expense.save()
        expense_objects.append(expense)


def set_consolidation_groups():
    # for funder in funder_objects:
    for expense in expense_objects:
        group = ConsolidationGroup(subject_of_procurement=expense.name, type_of_procurement=expense.type_of_procurement, expense=expense)
        group.save()


def set_programs_subprograms_deparatments():
    p1 = Programme(code="0751", name="Delivery of Tertiary Education and Research"); p1.save()
    p2 = Programme(code="0713", name="Support Services Programme"); p2.save()
    p3 = Programme(code="0714", name="Delivery of Tertiary Education Programme"); p3.save()

    sp1 = SubProgramme(code="01", name="Headquarters", programme=p1); sp1.save()

    sp2 = SubProgramme(code="02", name="Central Administration", programme=p2); sp2.save()
    sp3 = SubProgramme(code="03", name="Academic and Student Affairs", programme=p2); sp3.save()

    sp4 = SubProgramme(code="04", name="Faculty of Technoscience", programme=p3); sp4.save()
    sp5 = SubProgramme(code="05", name="Research and Innovation Department", programme=p3); sp5.save()
    sp6 = SubProgramme(code="06", name="Faculty of Education", programme=p3); sp6.save()
    sp7 = SubProgramme(code="07", name="Faculty of Health Sciences", programme=p3); sp7.save()
    sp8 = SubProgramme(code="08", name="Faculty of Science", programme=p3); sp8.save()
    sp9 = SubProgramme(code="09", name="Agriculture and Environmental Science", programme=p3); sp9.save()
    sp10 = SubProgramme(code="10", name="Faculty of Management Science", programme=p3); sp10.save()

    departments = [("Office of Accounting Officer", sp2, 10000000, False, True),
                   ("Procurement and Disposal Unit", sp2, 10000000, True, True),
                   ("Estates", sp2, 100000000, False, False),
                   ("Internal Audit", sp2, 30000000, False, False),
                   ("Office of the Vice Chancellor", sp2, 30000000, False, False),
                   ("Guild", sp3, 30000000, False, False),
                   ("Academic Registrar", sp3, 30000000, False, False),
                   ("Library", sp2, 40000000, False, False),
                   ("Faculty of Education", sp6, 50000000, False, False)
                   ]
    
    for name, sp, sealing, is_pdu, is_official in departments:
        ud = UserDepartment(name=name, sub_programme=sp, budget_sealing=sealing, is_pdu=is_pdu, is_official=is_official)
        ud.save()
        department_objects.append(ud)


def register_AO():
    user = User.objects.create_user(
        username = 'ao@muni.ac.ug',
        password = '123',
        first_name = 'Epiphany',
        last_name = 'Picho Odubuker'
        )
    user.save()

    profile = Profile(
        display_name=f'{user.first_name} {user.last_name}', title='Accounting Officer', telephone='0772299330', 
        is_ao=True, user_department=department_objects[0], 
        user=user
        )
    department_objects[0].hod = user
    department_objects[0].save()
    profile.save()


def create_PDU_members():
    head = User.objects.create_user(
        username = 'pdu_head@muni.ac.ug',
        password = '123',
        first_name = 'Richard',
        last_name = 'Anguyo'
        )
    head.save()
    head_profile = Profile(
        display_name=f'{head.first_name} {head.last_name}', title = 'Senior Procurement Officer',telephone='0772445560', 
        is_in_pdu=True, user_department=department_objects[1], 
        user=head
        )
    department_objects[1].hod = head
    department_objects[1].save()
    head_profile.save()
    member = User.objects.create_user(
        username = 'pdu1@muni.ac.ug',
        password = '123',
        first_name = 'Francis',
        last_name = 'Nyeko'
        )
    member.save()
    member_profile = Profile(
        display_name=f'{member.first_name} {member.last_name}', title = 'Junior Procurement Officer', telephone='0772299430', 
        is_in_pdu=True, user_department=department_objects[1], 
        user=member
        )
    member_profile.save()

def create_ordinary_members():
    head = User.objects.create_user(
        username = 'educ_head@muni.ac.ug',
        password = '123',
        first_name = 'Geofrey',
        last_name = 'Andogah'
        )
    head.save()
    head_profile = Profile(
        display_name=f'{head.first_name} {head.last_name}', title = 'Head of Department', telephone='0782455460', 
        user_department=department_objects[8], user=head
        )
    department_objects[8].hod = head
    department_objects[8].save()
    head_profile.save()

    member = User.objects.create_user(
        username = 'educ1@muni.ac.ug',
        password = '123',
        first_name = 'Vicky',
        last_name = 'Small'
        )
    member.save()
    member_profile = Profile(
        display_name=f'{member.first_name} {member.last_name}', title = 'Secretary',telephone='0782245555', 
        user_department=department_objects[8], user=member
        )
    member_profile.save()

    member2 = User.objects.create_user(
        username = 'educ2@muni.ac.ug',
        password = '123',
        first_name = 'Smith',
        last_name = 'Okot'
        )
    member2.save()
    member2_profile = Profile(
        display_name=f'{member2.first_name} {member2.last_name}', title = 'Lecturer',telephone='0777224555', 
        user_department=department_objects[8], user=member2
        )
    member2_profile.save()


def set_permissions():
    users = User.objects.all()
    can_prepare_plan = Permission.objects.get(codename='can_prepare_plan')
    can_initiate_requisition = Permission.objects.get(codename='can_initiate_requisition')
    for user in users:
        user.user_permissions.set([can_prepare_plan, can_initiate_requisition])
        user.save()


def set_planning_timing(start_date=timezone.now()):
    p_start = start_date - timedelta(1)
    p_dead = p_start + timedelta(2)
    p_stop = p_start + timedelta(4)

    i_start = p_stop
    i_dead = i_start + timedelta(2)
    i_stop = i_start + timedelta(4)

    b_start = i_stop
    b_stop = b_start + timedelta(4)

    c_start = b_stop
    c_stop = c_start + timedelta(4)

    planning_timing = Timing.objects.filter(process="Planning")
    planning_timing.update(start=p_start, submission_deadline=p_dead, stop=p_stop)
    # planning_timing.save()

    initiation_timing = Timing.objects.filter(process="Initiation")
    initiation_timing.update(start=i_start, submission_deadline=i_dead, stop=i_stop)
    # initiation_timing.save()

    bidding_timing = Timing.objects.filter(process="Bidding")
    bidding_timing.update(start=b_start, stop=b_stop)
    # bidding_timing.save()

    contract_timing = Timing.objects.filter(process="Contract")
    contract_timing.update(start=c_start, stop=c_stop)
    # contract_timing.save()



def set_initiation_timing(start_date=timezone.now()):
    i_start = start_date - timedelta(1)
    i_dead = i_start + timedelta(2)
    i_stop = i_start + timedelta(4)


    p_start = i_start - timedelta(4)
    p_dead = p_start + timedelta(1)
    p_stop = p_start + timedelta(1)

    
    b_start = i_stop
    b_stop = b_start + timedelta(4)

    c_start = b_stop
    c_stop = c_start + timedelta(4)

    planning_timing = Timing.objects.filter(process="Planning")
    planning_timing.update(start=p_start, submission_deadline=p_dead, stop=p_stop)
    # planning_timing.save()

    initiation_timing = Timing.objects.filter(process="Initiation")
    initiation_timing.update(start=i_start, submission_deadline=i_dead, stop=i_stop)
    # initiation_timing.save()

    bidding_timing = Timing.objects.filter(process="Bidding")
    bidding_timing.update(start=b_start, stop=b_stop)
    # bidding_timing.save()

    contract_timing = Timing.objects.filter(process="Contract")
    contract_timing.update(start=c_start, stop=c_stop)
    # contract_timing.save()
