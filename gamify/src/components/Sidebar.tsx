import { useState, useEffect } from "react";

interface SidebarProps {
  currentPoints: number;
  activeView: "dashboard" | "calendar";
  setActiveView: (view: "dashboard" | "calendar") => void;
}

const Sidebar = ({
  currentPoints,
  activeView,
  setActiveView,
}: SidebarProps) => {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let interval: number;
    if (isRunning) {
      interval = setInterval(() => {
        setTime((prevTime) => prevTime + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-full h-full flex flex-col gap-4 lg:gap-6 bg-light-gray rounded-4xl p-4 md:p-6">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:p-6 bg-dark-gray-4xl">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 md:w-8 md:h-8 bg-dark-gray rounded-full" />
          <span className="text-lg md:text-xl font-bold text-superdark-gray">
            GAMIFY
          </span>
        </div>
        <button className="text-dark-gray">
          <svg
            width="20"
            height="20"
            className="md:w-6 md:h-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <circle cx="12" cy="6" r="1.5" />
            <circle cx="12" cy="12" r="1.5" />
            <circle cx="12" cy="18" r="1.5" />
          </svg>
        </button>
      </div>

      <div className="flex-1 flex flex-col justify-evenly">
        {/* Navigation */}
        <div className="flex flex-col gap-2">
          <button
            onClick={() => setActiveView("dashboard")}
            className={`text-center px-4 md:px-6 py-2 md:py-3 font-bold rounded-4xl ${
              activeView === "dashboard"
                ? "bg-gradient-to-r from-mango-orange to-strawberry-red text-white font-bold"
                : "text-superdark-gray"
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setActiveView("calendar")}
            className={`text-center px-4 md:px-6 py-3 md:py-4 font-bold rounded-4xl ${
              activeView === "calendar"
                ? "bg-gradient-to-r from-mango-orange to-strawberry-red text-white"
                : "text-superdark-gray"
            }`}
          >
            Calendar
          </button>
        </div>

        {/* Timer */}
        <div className="bg-#5a5a5a-4xl p-6 md:p-8 flex flex-col items-center gap-3 md:gap-4">
          <div className="text-5xl md:text-6xl font-bold text-black">
            {formatTime(time)}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsRunning(true)}
              className="px-5 md:px-6 py-2 bg-gray rounded-2xl text-white font-medium text-sm md:text-base transition-all duration-300 hover:scale-102 hover:drop-shadow-md cursor-pointer"
            >
              start
            </button>
            <button
              onClick={() => setIsRunning(false)}
              className="px-5 md:px-6 py-2 bg-gray rounded-2xl text-white font-medium text-sm md:text-base transition-all duration-300 hover:scale-102 hover:drop-shadow-md cursor-pointer"
            >
              stop
            </button>
          </div>
        </div>

        {/* User Profile */}
        <div className="bg-#5a5a5a-4xl p-4 md:p-5 flex items-center gap-3">
          <div className="w-12 h-12 md:w-14 md:h-14 bg-gray rounded-full flex items-center justify-center">
            <svg
              width="24"
              height="24"
              className="md:w-7 md:h-7"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
            </svg>
          </div>
          <span className="text-base md:text-lg text-superdark-gray font-medium">
            EIK
          </span>
        </div>
      </div>

      {/* Points Display */}
      <div className="mt-auto bg-gradient-to-br from-mango-orange to-strawberry-red rounded-4xl p-10 md:p-12 flex items-center justify-center">
        <span className="text-6xl md:text-6xl font-bold text-white">
          {currentPoints}
        </span>
      </div>
    </div>
  );
};

export default Sidebar;
