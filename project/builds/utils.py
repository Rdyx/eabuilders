from characters.models import SkillModel


def get_selected_skills(request):
    skills_id_list = []
    for key in request.POST:
        if "skill_" in key:
            skills_id_list.append(request.POST[key])

    return SkillModel.objects.filter(id__in=skills_id_list).select_related(
        "skill_owner"
    )
