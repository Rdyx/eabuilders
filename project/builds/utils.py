from characters.models import SkillModel


def get_selected_skills(request):
    skills_id_list = []
    for key in request.POST:
        if "skill_" in key:
            skills_id_list.append(request.POST[key])

    return SkillModel.objects.filter(id__in=skills_id_list).select_related(
        "owner", "stype", "level"
    )


def check_form_values(form, field_name_to_check, fields_number_target):
    """
    Form field values checker.
    Count if we get required number of fields and no double value before saving
    """
    fields_number = 0
    field_values = []
    wrong_field_values = False

    for k, v in form.items():
        if field_name_to_check in k:
            fields_number += 1
        if not v in field_values:
            field_values.append(v)
        else:
            wrong_field_values = True
            break

    return fields_number == fields_number_target and not wrong_field_values