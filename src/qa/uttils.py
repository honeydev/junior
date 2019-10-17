from collections.abc import Callable, Generator

from src.qa.models import Chapter


def select_chapters_with_splited_questions(
        split_method: Callable,
        split_size: int = 2) -> Generator:

    def map_method(chapter: Chapter) -> Chapter:
        chapter.splited_questions = split_method(chapter.questions, split_size)
        return chapter

    return (map_method(chapter) for chapter in Chapter.query.all())
