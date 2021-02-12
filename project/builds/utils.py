from characters.models import SkillModel
from items.models import ItemModel, RaceModel, MaterialModel

from .models import BuildModel


def get_base_buildmodel_request():
    """ Because there's much related field bringing some hard code pollution """
    return BuildModel.objects.select_related(
        "creator",
        "char",
        "skill_1__stype",
        "skill_2__stype",
        "skill_3__stype",
        "skill_4__stype",
        "skill_5__stype",
        "skill_6__stype",
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


def get_build_sets_bonus(build):
    build_items_list = []
    races_counter_dict = {}
    materials_counter_dict = {}

    def _extract_build_items_fk(build, items_list):
        build_as_dict = build.__dict__
        for field in build_as_dict:
            if "item" in field:
                items_list.append(build_as_dict[field])

    _extract_build_items_fk(build, build_items_list)

    def _update_or_create_dict_key(dicto, key):
        if dicto.get(key, None):
            dicto[key] += 1
        else:
            dicto[key] = 1

    def _update_race_and_material_dict(race_dict, material_dict, item):
        _update_or_create_dict_key(race_dict, item.race.name)
        _update_or_create_dict_key(material_dict, item.material.name)

    def _get_model_as_dict(model, selected_bonus):
        return {
            "img": model.img,
            "name": model.name,
            "selected_bonus": selected_bonus,
        }

    def _check_bonus_required_items(required_nb_items, nb_items):
        return required_nb_items and nb_items >= int(required_nb_items)

    # Query to get items from build's items foreign keys
    build_items = ItemModel.objects.filter(id__in=build_items_list).select_related(
        "race", "material"
    )

    for item in list(build_items):
        _update_race_and_material_dict(races_counter_dict, materials_counter_dict, item)

        # materials = model.objects.filter(name__in=[k for k in model_counter_dict.keys()])

    def _get_sets_bonus(Model, model_counter_dict):
        models = Model.objects.filter(name__in=[k for k in model_counter_dict.keys()])
        sets_bonus = []

        for model in models:
            nb_items = model_counter_dict[model.name]

            if _check_bonus_required_items(model.bonus_3_min_nb_items_req, nb_items):
                sets_bonus.append(_get_model_as_dict(model, model.bonus_3))
            elif _check_bonus_required_items(model.bonus_2_min_nb_items_req, nb_items):
                sets_bonus.append(_get_model_as_dict(model, model.bonus_2))
            elif _check_bonus_required_items(model.bonus_1_min_nb_items_req, nb_items):
                sets_bonus.append(_get_model_as_dict(model, model.bonus_1))

        return sets_bonus

    return (
        _get_sets_bonus(RaceModel, races_counter_dict),
        _get_sets_bonus(MaterialModel, materials_counter_dict),
    )