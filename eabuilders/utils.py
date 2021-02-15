tiers_colors = {
    "1": "gray-100",
    "2": "green-400",
    "3": "blue-400",
    "4": "purple-400",
    "5": "orange-300",
}


def get_pagination(pagination, queryset, page_number):
    """ Get pagination variables """
    total_builds_found = len(queryset)
    previous_page = page_number - 1 if page_number > 1 else 0
    next_page = (
        page_number + 1 if (page_number * pagination) < total_builds_found else 0
    )

    return (total_builds_found, previous_page, next_page)
