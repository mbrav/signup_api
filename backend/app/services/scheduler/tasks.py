
from itertools import permutations
from typing import List

from pydantic import BaseModel, Field
from transliterate import translit


class TaskDetail(BaseModel):
    description: str = Field(example='Capitalize string')
    arguments: List[str] = Field(example=['text'])


class ExecutableTasks:
    """Tasks available for execution"""

    @staticmethod
    async def combine(text: str, text2: str) -> str:
        """Combine two strings"""
        return text+text2

    @staticmethod
    async def permutation(text: str) -> str:
        """Find permutation of a string"""
        return str(list(permutations(text)))

    @staticmethod
    async def repeat(text: str, index: int, times: int) -> str:
        """Repeat character in string"""
        return str(text[index]*times)

    @staticmethod
    async def capital(text: str) -> str:
        """Capitalize string"""
        return text.capitalize()

    @staticmethod
    async def capslock(text: str) -> str:
        """Capslock string"""
        return text.upper()

    @staticmethod
    async def lower(text: str) -> str:
        """Convert the entire string to lowercase"""
        return text.casefold()

    @staticmethod
    async def check_decimal(text: str) -> str:
        """Check if string is decimal"""
        return str(text.isdecimal())

    @staticmethod
    async def reverse(text: str) -> str:
        """Reverse string"""
        return text[::-1]

    @staticmethod
    async def sort_alphabetically(text: str) -> str:
        """Sort letters in string alphabetically"""
        return ''.join(sorted(text))

    @staticmethod
    async def transliter(text: str) -> str:
        """Translit roman to russian"""
        return translit(text, 'ru')

    @ staticmethod
    async def translit_reverse(text: str) -> str:
        """Translit russian to roman"""
        return translit(text, reversed=True)


tasks_info = {
    str(name): TaskDetail(
        description=getattr(ExecutableTasks, name).__doc__,
        arguments=list(getattr(ExecutableTasks, name).__code__.co_varnames)).dict()
    for name in dir(ExecutableTasks) if not name.startswith('__')}
