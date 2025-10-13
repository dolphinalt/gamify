const TaskList = () => {
  const tasks = [
    { name: "I&C 6B: ZyBook", duration: "60m" },
    { name: "I&C 6B: Reading Quiz", duration: "30m" },
    { name: "I&C 6B: ICA", duration: "90m" },
  ];

  return (
    <div className="bg-light-gray rounded-3xl p-6 h-full flex flex-col">
      <h3 className="text-2xl font-bold text-superdark-gray mb-1">Task List</h3>
      <p className="text-sm text-dark-gray mb-4">10/5/2025</p>
      <div className="h-1 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-6" />

      <div className="space-y-4 flex-1 mb-6">
        {tasks.map((task, i) => (
          <div key={i} className="text-superdark-gray">
            <div className="font-semibold text-base">{task.name}</div>
            <div className="text-sm text-dark-gray">{task.duration}</div>
          </div>
        ))}
      </div>

      <button className="w-full py-3 bg-gray rounded-2xl text-superdark-gray font-semibold text-base hover:bg-dark-gray hover:text-white transition">
        Generate
      </button>
    </div>
  );
};

export default TaskList;
