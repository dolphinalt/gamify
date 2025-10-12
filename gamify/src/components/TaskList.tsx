const TaskList = () => {
  const tasks = [
    { name: "I&C GB: ZyBook", duration: "60m" },
    { name: "I&C GB: Reading Quiz", duration: "30m" },
    { name: "I&C GB: ICA", duration: "90m" },
  ];

  return (
    <div className="bg-light-gray rounded-4xl p-4 md:p-6">
      <h3 className="text-lg md:text-xl font-bold text-superdark-gray mb-2">
        Task List
      </h3>
      <p className="text-sm md:text-base text-dark-gray mb-3 md:mb-4">
        10/5/2025
      </p>
      <div className="h-1.5 md:h-2 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-4 md:mb-6" />

      <div className="space-y-2 md:space-y-3 mb-4 md:mb-6">
        {tasks.map((task, i) => (
          <div key={i} className="text-superdark-gray">
            <div className="font-medium text-sm md:text-base">{task.name}</div>
            <div className="text-xs md:text-sm text-dark-gray">
              {task.duration}
            </div>
          </div>
        ))}
      </div>

      <button className="w-full py-2.5 md:py-3 bg-gray rounded-2xl text-superdark-gray font-medium text-sm md:text-base">
        Generate
      </button>
    </div>
  );
};

export default TaskList;
