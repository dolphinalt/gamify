interface CalendarViewProps {
  isCompact?: boolean;
}

const CalendarView = ({ isCompact = false }: CalendarViewProps) => {
  const hours = [
    "12am",
    "1am",
    "2am",
    "3am",
    "4am",
    "5am",
    "6am",
    "7am",
    "8am",
    "9am",
  ];

  return (
    <div className="bg-light-gray rounded-3xl p-6 h-full flex flex-col">
      <h2 className="text-2xl font-bold text-superdark-gray mb-1">Sunday</h2>
      <p className="text-sm text-dark-gray mb-4">10/5/2025</p>

      <div className="h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-6" />

      <div className="space-y-3 flex-1 overflow-y-auto">
        {hours.map((hour) => (
          <div key={hour} className="text-lg font-bold text-superdark-gray">
            {hour}
          </div>
        ))}
      </div>

      <div className="h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mt-6 mb-6" />

      <div className="flex justify-between items-center gap-4">
        <button className="w-14 h-14 bg-gray rounded-full flex items-center justify-center text-dark-gray hover:bg-dark-gray hover:text-white transition">
          <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
          </svg>
        </button>
        <button className="w-14 h-14 bg-gray rounded-full flex items-center justify-center text-dark-gray hover:bg-dark-gray hover:text-white transition">
          <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default CalendarView;
