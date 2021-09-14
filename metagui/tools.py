def intersperse(elements, betweener_factory, first=False, last=False):
    output = []
    if first:
        output.append(betweener_factory())
    last_elem_idx = len(elements) - 1
    for idx, elem in enumerate(elements):
        output.append(elem)
        if idx < last_elem_idx:
            output.append(betweener_factory())
    if last:
        output.append(betweener_factory())
    return output
