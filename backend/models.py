from extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import type_coerce
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, ColumnElement
from datetime import datetime, timezone
from typing import List


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


class RecurrenceRule(Base):
    """
    Recurrence rule for recurring events.
    Based on iCalendar RFC 5545 recurrence rule specification.
    """
    __tablename__ = 'recurrence_rules'

    # Auto-generated fields
    id: Mapped[int] = mapped_column(primary_key=True)
    _created_at: Mapped[datetime] = mapped_column(
        'created_at',
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Required fields
    freq: Mapped[str] = mapped_column(String(20))  # 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'
    _dtstart: Mapped[datetime] = mapped_column('dtstart', DateTime)  # Start date of recurrence

    # Optional fields
    interval: Mapped[int] = mapped_column(default=1)  # Repeat every N periods
    _until: Mapped[datetime | None] = mapped_column('until', DateTime, default=None)  # End date
    count: Mapped[int | None] = mapped_column(default=None)  # Number of occurrences
    byday: Mapped[str | None] = mapped_column(String(50), default=None)  # Days of week: 'MO,WE,FR'
    bymonthday: Mapped[str | None] = mapped_column(String(100), default=None)  # Days of month: '1,15'
    bymonth: Mapped[str | None] = mapped_column(String(50), default=None)  # Months: '1,6,12'

    # Relationship to events
    events: Mapped[List["Event"]] = relationship(back_populates="recurrence_rule", cascade="all, delete-orphan")

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
    def dtstart(self) -> datetime:
        return from_utc_naive(self._dtstart)

    @dtstart.inplace.setter
    def _dtstart_setter(self, value: datetime) -> None:
        self._dtstart = to_utc_naive(value)

    @dtstart.inplace.expression
    @classmethod
    def _dtstart_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._dtstart, DateTime)

    @hybrid_property
    def until(self) -> datetime | None:
        if self._until is None:
            return None
        return from_utc_naive(self._until)

    @until.inplace.setter
    def _until_setter(self, value: datetime | None) -> None:
        if value is None:
            self._until = None
        else:
            self._until = to_utc_naive(value)

    @until.inplace.expression
    @classmethod
    def _until_expression(cls) -> ColumnElement[datetime]:
        return type_coerce(cls._until, DateTime)

    def generate_occurrences(self, start: datetime, end: datetime) -> List[datetime]:
        """
        Generate occurrence datetimes within the specified range.

        Args:
            start: Start of the range to generate occurrences
            end: End of the range to generate occurrences

        Returns:
            List of datetime objects representing occurrences
        """
        from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY, MO, TU, WE, TH, FR, SA, SU

        # Map frequency strings to constants
        freq_map = {
            'DAILY': DAILY,
            'WEEKLY': WEEKLY,
            'MONTHLY': MONTHLY,
            'YEARLY': YEARLY
        }

        # Map weekday strings to constants
        weekday_map = {
            'MO': MO, 'TU': TU, 'WE': WE, 'TH': TH,
            'FR': FR, 'SA': SA, 'SU': SU
        }

        freq_const = freq_map.get(self.freq)
        if not freq_const:
            return []

        # Parse byday parameter
        byweekday = None
        if self.byday:
            days = [d.strip().upper() for d in self.byday.split(',')]
            byweekday = [weekday_map[d] for d in days if d in weekday_map]

        # Parse bymonthday parameter
        bymonthday_list = None
        if self.bymonthday:
            bymonthday_list = [int(d.strip()) for d in self.bymonthday.split(',')]

        # Parse bymonth parameter
        bymonth_list = None
        if self.bymonth:
            bymonth_list = [int(m.strip()) for m in self.bymonth.split(',')]

        # Create rrule
        rule_params = {
            'freq': freq_const,
            'interval': self.interval,
            'dtstart': self.dtstart.replace(tzinfo=None),  # rrule needs naive datetime
        }

        if self.until:
            rule_params['until'] = self.until.replace(tzinfo=None)
        if self.count:
            rule_params['count'] = self.count
        if byweekday:
            rule_params['byweekday'] = byweekday
        if bymonthday_list:
            rule_params['bymonthday'] = bymonthday_list
        if bymonth_list:
            rule_params['bymonth'] = bymonth_list

        rule = rrule(**rule_params)

        # Get occurrences in the range
        # rrule.between is inclusive on start, exclusive on end
        occurrences = rule.between(
            start.replace(tzinfo=None),
            end.replace(tzinfo=None),
            inc=True
        )

        # Convert back to UTC aware datetimes
        return [dt.replace(tzinfo=timezone.utc) for dt in occurrences]

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'freq': self.freq,
            'dtstart': self.dtstart.isoformat(),
            'interval': self.interval,
            'until': self.until.isoformat() if self.until else None,
            'count': self.count,
            'byday': self.byday,
            'bymonthday': self.bymonthday,
            'bymonth': self.bymonth
        }

    def __repr__(self):
        return f'<RecurrenceRule {self.id}: {self.freq} every {self.interval}>'


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

    # Recurrence relationship
    recurrence_rule_id: Mapped[int | None] = mapped_column(ForeignKey('recurrence_rules.id'), default=None)
    recurrence_rule: Mapped["RecurrenceRule | None"] = relationship(back_populates="events")

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
            'all_day': self.all_day,
            'recurrence_rule': self.recurrence_rule.to_dict() if self.recurrence_rule else None
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