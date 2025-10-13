from extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import type_coerce
from sqlalchemy import String, Text, Boolean, DateTime, ColumnElement
from datetime import datetime, timezone


def from_utc_naive(dt: datetime) -> datetime:
    """
    Adds UTC timezone to datetime object if it is missing timezone info.
    """

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def to_utc_naive(dt: datetime) -> datetime:
    """
    Normalizes timezone-aware time to naive UTC for storage
    """

    dt = dt.astimezone(timezone.utc)
    return dt.replace(tzinfo=None)

class Event(Base):
    __tablename__ = 'events'

    # Auto-generated fields
    id: Mapped[int] = mapped_column(primary_key=True)
    _created_at: Mapped[datetime] = mapped_column(
        'created_at',
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    _updated_at: Mapped[datetime] = mapped_column(
        'updated_at',
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Required fields
    title: Mapped[str] = mapped_column(String(200))
    _start_time: Mapped[datetime] = mapped_column('start_time', DateTime)
    _end_time: Mapped[datetime] = mapped_column('end_time', DateTime)

    # Optional fields
    description: Mapped[str | None] = mapped_column(Text, default=None)
    location: Mapped[str | None] = mapped_column(String(200), default=None)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)

    @hybrid_property
    def created_at(self) -> datetime:
        return from_utc_naive(self._created_at)

    @created_at.inplace.setter
    def _created_at_setter(self, value: datetime) -> None:
        self._created_at = to_utc_naive(value)

    @created_at.inplace.expression
    @classmethod
    def _created_at_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._created_at, DateTime)

    @hybrid_property
    def updated_at(self) -> datetime:
        return from_utc_naive(self._updated_at)

    @updated_at.inplace.setter
    def _updated_at_setter(self, value: datetime) -> None:
        self._updated_at = to_utc_naive(value)

    @updated_at.inplace.expression
    @classmethod
    def _updated_at_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._updated_at, DateTime)

    @hybrid_property
    def start_time(self) -> datetime:
        return from_utc_naive(self._start_time)

    @start_time.inplace.setter
    def _start_time_setter(self, value: datetime) -> None:
        self._start_time = to_utc_naive(value)

    @start_time.inplace.expression
    @classmethod
    def _start_time_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._start_time, DateTime)

    @hybrid_property
    def end_time(self) -> datetime:
        return from_utc_naive(self._end_time)

    @end_time.inplace.setter
    def _end_time_setter(self, value: datetime) -> None:
        self._end_time = to_utc_naive(value)

    @end_time.inplace.expression
    @classmethod
    def _end_time_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._end_time, DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'description': self.description,
            'location': self.location,
            'all_day': self.all_day
        }

    def __repr__(self):
        return f'<Event {self.id}: {self.title}>'


class Task(Base):
    __tablename__ = 'tasks'

    # Auto-generated fields
    id: Mapped[int] = mapped_column(primary_key=True)
    _created_at: Mapped[datetime] = mapped_column(
        'created_at',
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    _updated_at: Mapped[datetime] = mapped_column(
        'updated_at',
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Required fields
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)

    # Optional fields
    location: Mapped[str | None] = mapped_column(String(200), default=None)
    _due_datetime: Mapped[datetime | None] = mapped_column('due_datetime', DateTime, default=None)
    link: Mapped[str | None] = mapped_column(String(300), default=None)

    @hybrid_property
    def created_at(self) -> datetime:
        return from_utc_naive(self._created_at)

    @created_at.inplace.setter
    def _created_at_setter(self, value: datetime) -> None:
        self._created_at = to_utc_naive(value)

    @created_at.inplace.expression
    @classmethod
    def _created_at_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._created_at, DateTime)

    @hybrid_property
    def updated_at(self) -> datetime:
        return from_utc_naive(self._updated_at)

    @updated_at.inplace.setter
    def _updated_at_setter(self, value: datetime) -> None:
        self._updated_at = to_utc_naive(value)

    @updated_at.inplace.expression
    @classmethod
    def _updated_at_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._updated_at, DateTime)

    @hybrid_property
    def due_datetime(self) -> datetime | None:
        if self._due_datetime is None:
            return None
        else:
            return from_utc_naive(self._due_datetime)

    @due_datetime.inplace.setter
    def _due_datetime_setter(self, value: datetime | None) -> None:
        if value is None:
            self._due_datetime = None
        else:
            self._due_datetime = to_utc_naive(value)

    @due_datetime.inplace.expression
    @classmethod
    def _due_datetime_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._due_datetime, DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'due_datetime': self.due_datetime.isoformat() if self.due_datetime else None,
            'link': self.link
        }

    def __repr__(self):
        return f'<Event {self.id}: {self.title}>'