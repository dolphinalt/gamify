const TaskList = () => {
  const tasks = [
    { name: "I&C 6B: ZyBook", duration: "60m" },
    { name: "I&C 6B: Reading Quiz", duration: "30m" },
    { name: "I&C 6B: ICA", duration: "90m" },
  ];

  return (
    <div className="bg-light-gray rounded-4xl p-6">
      <h3 className="text-xl font-bold text-superdark-gray mb-2">Task List</h3>
      <p className="text-dark-gray mb-4">10/5/2025</p>
      <div className="h-2 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-full mb-6" />

      <div className="space-y-3 mb-6">
        {tasks.map((task, i) => (
          <div key={i} className="text-superdark-gray">
            <div className="font-medium">{task.name}</div>
            <div className="text-sm text-dark-gray">{task.duration}</div>
          </div>
        ))}
      </div>

      <button className="w-full py-3 bg-gray rounded-2xl text-superdark-gray font-medium">
        Generate
      </button>
    </div>
  );
};

export default TaskList;
