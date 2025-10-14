interface DailyTasksCardProps {
  progress: number;
}

const DailyTasksCard = ({ progress }: DailyTasksCardProps) => {
  return (
    <div className="bg-light-gray rounded-4xl p-4 md:p-6">
      <div className="flex items-center gap-2 mb-3 md:mb-4">
        <div className="w-6 h-6 md:w-8 md:h-8 bg-dark-gray rounded-full" />
        <h2 className="text-lg md:text-xl font-bold text-superdark-gray">
          Daily Tasks
        </h2>
      </div>

      <div className="flex items-center gap-2 sm:gap-3 md:gap-4">
        <div className="flex-1 h-3 md:h-4 bg-gray rounded-full overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-mango-orange to-strawberry-red transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-base sm:text-lg md:text-xl font-bold text-superdark-gray whitespace-nowrap">
          {progress}%
        </span>
      </div>
    </div>
  );
};

export default DailyTasksCard;
