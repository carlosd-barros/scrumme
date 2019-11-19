from enum import Enum

class ChoicesEnum(Enum):
    def __init__(self, code, display_name=''):
        self.code = code
        self.display_name = display_name

    def __eq__(self, other):
        if not other:
            raise ValueError()
        return self.code == other if isinstance(
            other, int) else self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def choices(cls):
        return tuple([
                (b.code, b.display_name) for a, b in cls.__members__.items()
            ])

    @classmethod
    def get(cls, index):
        choices = cls.choices()

        for t_index, t_value in choices:
            if t_index == index:
                return t_value

        return None


class JogadorType(ChoicesEnum):
    COMUM = (0, 'COMUM')
    MASTER = (1, 'SCRUM MASTER')
    OWNER = (2, 'PRODUCT OWNER')


class JogadorClass(ChoicesEnum):
    INICIANTE = (0, 'INICIANTE')
    INTERMEDIARIO = (1, 'INTERMEDIÁRIO')
    AVANCADO = (2, 'AVANÇADO')
    MESTRE = (3, 'MESTRE')
    JEDI = (4, 'JEDI')


class QuestLevel(ChoicesEnum):
    BAIXO = (0, 'BAIXO')
    MEDIO = (1, 'MÉDIO')
    ALTO = (2, 'ALTO')


