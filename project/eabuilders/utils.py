def get_pagination(pagination, queryset, page_number):
    """ Get pagination variables """
    total_builds_found = queryset.count()
    previous_page = page_number - 1 if page_number > 1 else 0
    next_page = (
        page_number + 1 if (page_number * pagination) < total_builds_found else 0
    )

    return (total_builds_found, previous_page, next_page)
