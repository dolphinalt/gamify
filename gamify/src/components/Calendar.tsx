const Calendar = () => {
  return (
    <div className="bg-light-gray rounded-2xl sm:rounded-3xl md:rounded-4xl p-3 sm:p-4 md:p-5 lg:p-6 h-full flex flex-col">
      <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-superdark-gray mb-1">
        Calendar
      </h3>
      <p className="text-xs sm:text-sm text-dark-gray mb-2 sm:mb-3 md:mb-4">
        10/5/2025
      </p>

      <div className="h-0.5 sm:h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mt-0 sm:mt-0 md:mt-0" />
    </div>
  );
};

export default Calendar;
