from characters.models import SkillModel

from .models import BuildModel


def get_base_buildmodel_request():
    """ Because there's much related field bringing some hard code pollution """
    return BuildModel.objects.select_related(
        "creator",
        "char",
        "skill_1",
        "skill_2",
        "skill_3",
        "skill_4",
        "skill_5",
        "skill_6",
        "item_1__race",
        "item_1__material",
        "item_2__race",
        "item_2__material",
        "item_3__race",
        "item_3__material",
        "item_4__race",
        "item_4__material",
        "item_5__race",
        "item_5__material",
        "item_6__race",
        "item_6__material",
        "item_7__race",
        "item_7__material",
        "item_8__race",
        "item_8__material",
    ).all()


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
            if not v in field_values and v != "No selection":
                field_values.append(v)
            else:
                wrong_field_values = True
                break

    return fields_number == fields_number_target and not wrong_field_values


def get_char_skills(char_slug):
    return (
        SkillModel.objects.filter(owner__slug=char_slug, level__level="4 (Max)")
        .select_related("owner", "stype", "level")
        .exclude(deprecated=True)
    )
