from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Problem(Base):
    """Класс для описания таблицы problems."""

    __tablename__ = "problems"

    problem_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    rating: Mapped[Optional[int]]
    tags: Mapped[str] = mapped_column(ARRAY(String(100)))

    def __repr__(self) -> str:
        """Возвращает строковое представление о задаче."""

        return f"{self.name} (ID: {self.problem_id})"


class ProblemStatistics(Base):
    """Класс для описания таблицы problems_statistics."""

    __tablename__ = "problems_statistics"

    problem_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("problems.problem_id"), primary_key=True
    )
    solved_сount: Mapped[Optional[int]]

    def __repr__(self) -> str:
        """Возвращает строковое представление о статистике по задаче."""

        return f"Количество решений: {self.solved_сount} (ID: {self.problem_id})"
