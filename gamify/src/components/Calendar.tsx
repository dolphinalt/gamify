import { useState, useMemo } from "react";

interface CalendarEvent {
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  location?: string;
  all_day?: boolean;
}

interface CalendarProps {
  events?: CalendarEvent[];
  selectedDate?: Date;
  onDateSelect?: (date: Date) => void;
}

interface CalendarDay {
  date: Date;
  isCurrentMonth: boolean;
  isToday: boolean;
  isSelected: boolean;
  eventCount: number;
}

const Calendar = ({
  events = [],
  selectedDate,
  onDateSelect,
}: CalendarProps) => {
  const [currentDate, setCurrentDate] = useState(new Date(2025, 9, 16));
  const [selected, setSelected] = useState<Date | null>(
    selectedDate || new Date(2025, 9, 16)
  );

  // Utility functions
  const isSameDay = (date1: Date, date2: Date): boolean => {
    return (
      date1.getFullYear() === date2.getFullYear() &&
      date1.getMonth() === date2.getMonth() &&
      date1.getDate() === date2.getDate()
    );
  };

  const parseEventDate = (isoString: string): Date => {
    return new Date(isoString);
  };

  const getEventsForDay = (date: Date): CalendarEvent[] => {
    return events.filter((event) => {
      const eventStart = parseEventDate(event.start_time);
      return isSameDay(eventStart, date);
    });
  };

  const getFirstDayOfMonth = (date: Date): number => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const getDaysInMonth = (date: Date): number => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getDaysInPrevMonth = (date: Date): number => {
    return new Date(date.getFullYear(), date.getMonth(), 0).getDate();
  };

  // Generate calendar days
  const calendarDays = useMemo((): CalendarDay[] => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = getFirstDayOfMonth(currentDate);
    const daysInMonth = getDaysInMonth(currentDate);
    const daysInPrevMonth = getDaysInPrevMonth(currentDate);
    const today = new Date();

    const days: CalendarDay[] = [];

    // Previous month's days
    for (let i = firstDay - 1; i >= 0; i--) {
      const date = new Date(year, month - 1, daysInPrevMonth - i);
      days.push({
        date,
        isCurrentMonth: false,
        isToday: isSameDay(date, today),
        isSelected: selected ? isSameDay(date, selected) : false,
        eventCount: getEventsForDay(date).length,
      });
    }

    // Current month's days
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(year, month, i);
      days.push({
        date,
        isCurrentMonth: true,
        isToday: isSameDay(date, today),
        isSelected: selected ? isSameDay(date, selected) : false,
        eventCount: getEventsForDay(date).length,
      });
    }

    const remainingDays = 42 - days.length;
    for (let i = 1; i <= remainingDays; i++) {
      const date = new Date(year, month + 1, i);
      days.push({
        date,
        isCurrentMonth: false,
        isToday: isSameDay(date, today),
        isSelected: selected ? isSameDay(date, selected) : false,
        eventCount: getEventsForDay(date).length,
      });
    }

    return days;
  }, [currentDate, selected, events]);

  // Navigation handlers
  const goToPreviousMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1)
    );
  };

  const goToNextMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1)
    );
  };

  const handleDayClick = (day: CalendarDay) => {
    setSelected(day.date);
    setCurrentDate(
      new Date(day.date.getFullYear(), day.date.getMonth(), day.date.getDate())
    );
    onDateSelect?.(day.date);
  };

  const monthYear = currentDate.toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return (
    <div className="bg-light-gray rounded-2xl sm:rounded-3xl md:rounded-4xl p-2 sm:p-3 md:p-4 lg:p-6 flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-superdark-gray">
            Calendar
          </h3>
          <p className="text-xs sm:text-sm text-dark-gray">
            {selected
              ? selected.toLocaleDateString("en-US", {
                  month: "2-digit",
                  day: "2-digit",
                  year: "numeric",
                })
              : "10/05/2025"}
          </p>
        </div>

        {/* Month/Year Display */}
        <div className="text-sm sm:text-base md:text-lg font-semibold text-superdark-gray">
          {monthYear}
        </div>
      </div>

      {/* Gradient line with navigation buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={goToPreviousMonth}
          className="w-6 h-6 sm:w-7 sm:h-7 bg-gray rounded-full flex items-center justify-center text-white hover:bg-dark-gray transition-colors flex-shrink-0"
          aria-label="Previous month"
        >
          <svg
            width="12"
            height="12"
            className="sm:w-4 sm:h-4"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
          </svg>
        </button>

        <div className="flex-1 h-0.5 sm:h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full" />

        <button
          onClick={goToNextMonth}
          className="w-6 h-6 sm:w-7 sm:h-7 bg-gray rounded-full flex items-center justify-center text-white hover:bg-dark-gray transition-colors flex-shrink-0"
          aria-label="Next month"
        >
          <svg
            width="12"
            height="12"
            className="sm:w-4 sm:h-4"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
          </svg>
        </button>
      </div>

      {/* Calendar Grid */}
      <div className="flex-1 flex flex-col min-h-0 ">
        {/* Weekday Headers */}
        <div className="grid grid-cols-7 gap-0.5 mb-1">
          {weekDays.map((day) => (
            <div
              key={day}
              className="text-center text-[10px] sm:text-xs font-semibold text-dark-gray py-0.5"
            >
              {day}
            </div>
          ))}
        </div>

        {/* Calendar Days Grid */}
        <div className="grid grid-cols-7 gap-0.5 sm:gap-1">
          {calendarDays.map((day, index) => (
            <DayCell
              key={index}
              day={day}
              onClick={() => handleDayClick(day)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

// DayCell Component
interface DayCellProps {
  day: CalendarDay;
  onClick: () => void;
}

const DayCell = ({ day, onClick }: DayCellProps) => {
  const { date, isCurrentMonth, isToday, isSelected } = day;
  const dayNumber = date.getDate();

  // Determine styling
  const baseClasses =
    "relative flex flex-col items-center justify-center rounded-md sm:rounded-lg cursor-pointer transition-all duration-200 aspect-square";

  let bgClasses = "bg-white hover:bg-gray";
  let textClasses = "text-superdark-gray";

  if (!isCurrentMonth) {
    textClasses = "text-dark-gray opacity-40";
  }

  if (isSelected) {
    bgClasses =
      "bg-gradient-to-r from-mango-orange to-strawberry-red hover:opacity-90";
    textClasses = "text-white font-bold";
  } else if (isToday) {
    bgClasses = "bg-gray hover:bg-dark-gray";
    textClasses = "text-white font-bold";
  }

  return (
    <div className={`${baseClasses} ${bgClasses}`} onClick={onClick}>
      {/* Day Number */}
      <span className={`text-[10px] sm:text-xs ${textClasses}`}>
        {dayNumber}
      </span>
    </div>
  );
};

// Demo with sample events
const CalendarEventList = () => {
  const sampleEvents: CalendarEvent[] = [
    {
      title: "Team Meeting",
      start_time: "2025-10-05T10:00:00",
      end_time: "2025-10-05T11:00:00",
      description: "Weekly team sync",
      location: "Conference Room A",
    },
  ];

  const handleDateSelect = (date: Date) => {
    console.log("Selected date:", date.toLocaleDateString());
  };

  return <Calendar events={sampleEvents} onDateSelect={handleDateSelect} />;
};

export default CalendarEventList;
