from django.shortcuts import render

from .models import SkillModel, CharacterModel


def get_char_view(request, char_slug):
    try:
        character = CharacterModel.objects.get(char_slug=char_slug)
    except CharacterModel.DoesNotExist:
        return redirect("oops")

    character_skills = list(SkillModel.objects.filter(skill_owner=character))

    context = {"character": character, "character_skills": character_skills}
    return render(request, "character.html", context)
