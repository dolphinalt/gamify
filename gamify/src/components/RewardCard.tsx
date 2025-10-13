interface RewardCardProps {
  points: number;
  active: boolean;
}

const RewardCard = ({ points, active }: RewardCardProps) => {
  return (
    <>
      <div className={`flex flex-col justify-center items-center gap-2 p-7 rounded-4xl h-48 ${active ? "bg-gradient-to-r from-mango-orange to-strawberry-red transition-all duration-300 hover:scale-102 hover:drop-shadow-xl cursor-pointer" : "bg-light-gray"}`}>
        <div className="flex text-white text-6xl font-bold">
          {points}
        </div>
      </div>
    </>
  );
};

export default RewardCard;
