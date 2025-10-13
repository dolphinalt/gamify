interface CardProps {
  type: "task" | "new";
  title?: string;
  description?: string;
  points?: number;
}

const Card = ({ type, title, description, points }: CardProps) => {
  return (
    <>
    { type === "task" && (
      <div className="flex flex-col gap-2 p-7 rounded-4xl bg-light-gray h-48">
        <div>
          <div className="flex text-2xl font-bold text-left text-superdark-gray">
            {title}
          </div>
          <div className="flex italic text-left superdark-gray-500">
            {points}
          </div>
        </div>
        <hr className="w-full h-1 bg-gradient-to-r from-mango-orange to-strawberry-red border-0"></hr>
        <div className="text-dark-gray">{description}</div>
      </div>
    )}
    { type === "new" && (
      <div className="flex flex-col justify-center items-center gap-2 p-7 rounded-4xl bg-vapor-gray h-48 text-hollow-gray cursor-pointer">
        <div className="text-4xl font-bold">+</div>
        <div className="text-lg font-semibold">Add New Task</div>
      </div>
    )}
    </>
  );
};

export default Card;
