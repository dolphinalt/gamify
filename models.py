from extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, DateTime
from datetime import datetime, timezone

class Event(Base):
    __tablename__ = 'events'

    # Auto-generated fields
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Required fields
    title: Mapped[str] = mapped_column(String(200))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    # Optional fields
    description: Mapped[str] = mapped_column(Text, default='')
    location: Mapped[str] = mapped_column(String(200), default='')
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.add_utc(self.start_time).isoformat(),
            'end_time': self.add_utc(self.end_time).isoformat(),
            'location': self.location,
            'all_day': self.all_day,
            'created_at': self.add_utc(self.created_at).isoformat(),
            'updated_at': self.add_utc(self.updated_at).isoformat()
        }

    @staticmethod
    def add_utc(dt):
        """
        Ensure datetime has UTC timezone info.
        """

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def __repr__(self):
        return f'<Event {self.id}: {self.title}>'