const TaskList = () => {
  const tasks = [
    { name: "I&C 6B: ZyBook", duration: "60m" },
    { name: "I&C 6B: Reading Quiz", duration: "30m" },
  ];

  return (
    <div className="bg-light-gray rounded-2xl sm:rounded-3xl md:rounded-4xl p-3 sm:p-4 md:p-5 lg:p-6 h-full flex flex-col">
      <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-superdark-gray mb-1">
        Task List
      </h3>
      <p className="text-xs sm:text-sm text-dark-gray mb-2 sm:mb-3 md:mb-4">
        10/5/2025
      </p>
      <div className="h-0.5 sm:h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-3 sm:mb-4 md:mb-6" />

      <div className="space-y-2 sm:space-y-3 md:space-y-4 flex-1 mb-3 sm:mb-4 md:mb-6">
        {tasks.map((task, i) => (
          <div key={i} className="text-superdark-gray">
            <div className="font-semibold text-sm sm:text-base">
              {task.name}
            </div>
            <div className="text-xs sm:text-sm text-dark-gray">
              {task.duration}
            </div>
          </div>
        ))}
      </div>

      <button className="w-full py-2 sm:py-2.5 md:py-3 bg-gray rounded-xl sm:rounded-2xl text-superdark-gray font-semibold text-sm sm:text-base hover:bg-dark-gray hover:text-white transition">
        Generate
      </button>
    </div>
  );
};

export default TaskList;
