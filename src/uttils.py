

def split_by_two(sequence, size: int = 2):

    for index in range(0, len(sequence), size):  # noqa WPS518
        yield sequence[index:index + size]
