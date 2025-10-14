interface CardProps {
  type: "task" | "new";
  title?: string;
  description?: string;
  points?: number;
}

const Card = ({ type, title, description, points }: CardProps) => {
  const taskClick = () => {
    alert("Open task menu");
  };

  const newClick = () => {
    alert("New task menu");
  };

  return (
    <>
      {type === "task" && (
        <div
          className="flex flex-col gap-1 sm:gap-2 p-4 sm:p-5 md:p-6 lg:p-7 rounded-2xl sm:rounded-3xl md:rounded-4xl bg-light-gray h-32 sm:h-40 md:h-48 transition-all duration-300 hover:scale-102 hover:drop-shadow-xl cursor-pointer"
          onClick={taskClick}
        >
          <div>
            <div className="flex text-lg sm:text-xl md:text-2xl font-bold text-left text-superdark-gray">
              {title}
            </div>
            <div className="flex italic text-left superdark-gray-500 font-extralight">
              {points}
            </div>
          </div>
          <hr className="w-full h-2 rounded-full bg-gradient-to-r from-mango-orange to-strawberry-red border-0 font-extralight"></hr>
          <div className="text-xs sm:text-sm md:text-base text-dark-gray">
            {description}
          </div>
        </div>
      )}
      {type === "new" && (
        <div
          className="flex flex-col justify-center items-center gap-1 sm:gap-2 p-4 sm:p-5 md:p-6 lg:p-7 rounded-2xl sm:rounded-3xl md:rounded-4xl bg-vapor-gray h-32 sm:h-40 md:h-48 text-hollow-gray cursor-pointer transition-all duration-300 hover:scale-102 hover:drop-shadow-xl"
          onClick={newClick}
        >
          <div className="text-2xl sm:text-3xl md:text-4xl font-bold">+</div>
          <div className="text-sm sm:text-base md:text-lg font-semibold">
            Add New Task
          </div>
        </div>
      )}
    </>
  );
};

export default Card;
