from django.shortcuts import render

from .models import SkillLevelModel, SkillModel, CharacterModel


def chars_index_view(request):
    characters = CharacterModel.objects.all()

    context = {"characters": characters}
    return render(request, "chars_index.html", context)


def get_char_view(request, char_slug, skill_level="4 (Max)"):
    try:
        character = CharacterModel.objects.get(slug=char_slug)
    except CharacterModel.DoesNotExist:
        return redirect("oops")

    character_skills = SkillModel.objects.filter(
        owner=character, level__level=skill_level
    ).select_related("stype")

    context = {
        "character": character,
        "character_skills": character_skills,
    }
    return render(request, "character.html", context)
