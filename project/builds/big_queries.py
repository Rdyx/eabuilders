""" Centralisation of big select_related queries """

from .models import BuildModel, TeamModel


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
    )


def get_team_builds_request():
    return TeamModel.objects.select_related(
        "build_1__char",
        "build_2__char",
        "build_3__char",
    )
