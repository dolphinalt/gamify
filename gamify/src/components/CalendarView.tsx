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
    <div className="bg-light-gray rounded-2xl sm:rounded-3xl md:rounded-4xl p-3 sm:p-4 md:p-5 lg:p-6 h-full flex flex-col">
      <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-superdark-gray mb-1">
        Sunday
      </h2>
      <p className="text-xs sm:text-sm text-dark-gray mb-2 sm:mb-3 md:mb-4">
        10/5/2025
      </p>

      <div className="h-0.5 sm:h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-3 sm:mb-4 md:mb-6" />

      <div className="space-y-2 sm:space-y-2.5 md:space-y-3 flex-1 overflow-y-auto">
        {hours.map((hour) => (
          <div
            key={hour}
            className="text-sm sm:text-base md:text-lg font-bold text-superdark-gray"
          >
            {hour}
          </div>
        ))}
      </div>

      <div className="h-0.5 sm:h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mt-3 sm:mt-4 md:mt-6 mb-3 sm:mb-4 md:mb-6" />

      <div className="flex justify-between items-center gap-2 sm:gap-3 md:gap-4">
        <button className="w-10 sm:w-12 md:w-14 h-10 sm:h-12 md:h-14 bg-gray rounded-full flex items-center justify-center text-dark-gray hover:bg-dark-gray hover:text-white transition">
          <svg
            width="16"
            height="16"
            className="sm:w-5 sm:h-5 md:w-6 md:h-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
          </svg>
        </button>
        <button className="w-10 sm:w-12 md:w-14 h-10 sm:h-12 md:h-14 bg-gray rounded-full flex items-center justify-center text-dark-gray hover:bg-dark-gray hover:text-white transition">
          <svg
            width="16"
            height="16"
            className="sm:w-5 sm:h-5 md:w-6 md:h-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default CalendarView;
