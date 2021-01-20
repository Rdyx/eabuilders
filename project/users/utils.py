from builds.models import BuildModel


def get_user_builds(user):
    """ Simple common function to get a user's build """
    return BuildModel.objects.filter(creator=user).select_related(
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
    )
