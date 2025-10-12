interface CalendarViewProps {
  isCompact?: boolean;
}
const CalendarView = ({ isCompact = false }: CalendarViewProps) => {
  const hours = isCompact
    ? []
    : ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am"];

  if (isCompact) {
    return (
      <div className="bg-light-gray rounded-4xl p-6">
        <h3 className="text-xl font-bold text-superdark-gray mb-2">Calendar</h3>
        <p className="text-dark-gray mb-4">10/5/2025</p>
        <div className="h-2 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-4" />

        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-12 bg-gray rounded-2xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-superdark-gray mb-2">Sunday</h2>
      <p className="text-dark-gray mb-6">10/5/2025</p>

      <div className="h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-6" />

      <div className="space-y-4">
        {hours.map((hour) => (
          <div key={hour} className="text-xl font-bold text-superdark-gray">
            {hour}
          </div>
        ))}
      </div>

      <div className="mt-6 h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full" />

      <div className="mt-6 flex justify-between items-center">
        <button className="w-20 h-20 bg-gray rounded-full flex items-center justify-center text-dark-gray">
          <svg width="32" height="32" fill="currentColor" viewBox="0 0 24 24">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
          </svg>
        </button>
        <button className="w-20 h-20 bg-gray rounded-full flex items-center justify-center text-dark-gray">
          <svg width="48" height="48" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default CalendarView;
