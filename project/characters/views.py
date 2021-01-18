from django.shortcuts import render

from .models import CharacterModel


def get_char_view(request, char_slug):
    try:
        character = CharacterModel.objects.select_related(
            "char_skill_1__skill_type",
            "char_skill_2__skill_type",
            "char_skill_3__skill_type",
            "char_skill_4__skill_type",
            "char_skill_5__skill_type",
            "char_skill_6__skill_type",
            "char_skill_7__skill_type",
            "char_skill_8__skill_type",
            "char_skill_9__skill_type",
        ).get(char_slug=char_slug)
    except CharacterModel.DoesNotExist:
        return redirect("oops")

    context = {"character": character}
    return render(request, "character.html", context)
