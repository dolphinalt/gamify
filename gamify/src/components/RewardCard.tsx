interface RewardCardProps {
  points: number;
  active: boolean;
}

const RewardCard = ({ points, active }: RewardCardProps) => {
  const rewardClick = () => {
    alert("Open reward menu");
  };

  return (
    <>
      <div
        className={`flex flex-col justify-center items-center gap-2 p-4 sm:p-5 md:p-6 lg:p-7 rounded-2xl sm:rounded-3xl md:rounded-4xl h-32 sm:h-40 md:h-48 ${
          active
            ? "bg-gradient-to-r from-mango-orange to-strawberry-red transition-all duration-300 hover:scale-102 hover:drop-shadow-xl cursor-pointer"
            : "bg-light-gray"
        }`}
        onClick={rewardClick}
      >
        <div className="flex text-white text-3xl sm:text-5xl md:text-6xl font-bold">
          {points}
        </div>
      </div>
    </>
  );
};

export default RewardCard;
