def get_field(o: dict, *fields):
    current = o
    for field in fields:
        current = current.get(field)
        if current is not None:
            continue
        else:
            return None
    return current
