interface DailyTasksCardProps {
  progress: number;
}

const DailyTasksCard = ({ progress }: DailyTasksCardProps) => {
  return (
    <div className="bg-light-gray rounded-4xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 bg-dark-gray rounded-full" />
        <h2 className="text-xl font-bold text-superdark-gray">Daily Tasks</h2>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex-1 h-4 bg-gray rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-mango-orange to-strawberry-red transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-xl font-bold text-superdark-gray">
          {progress}%
        </span>
      </div>
    </div>
  );
};

export default DailyTasksCard;
