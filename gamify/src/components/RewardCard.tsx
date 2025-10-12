interface RewardCardProps {
  title: string;
  description: string;
  points: number;
}

const RewardCard = ({ title, description, points }: RewardCardProps) => {
  return (
    <>
      <div className="flex flex-col gap-2 p-7 rounded-4xl bg-gradient-to-r from-mango-orange to-strawberry-red h-48">
        <div>
          <div className="flex text-2xl font-bold text-left text-superdark-gray">
            {title}
          </div>
          <div className="flex italic text-left superdark-gray-500">
            {points}
          </div>
        </div>
        <div className="">{description}</div>
      </div>
    </>
  );
};

export default RewardCard;
