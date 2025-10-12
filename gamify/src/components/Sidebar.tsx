import { useState, useEffect } from "react";

interface SidebarProps {
  currentPoints: number;
}

const Sidebar = ({ currentPoints }: SidebarProps) => {
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
    <div className="w-full flex flex-row lg:flex-col gap-4 overflow-x-auto lg:overflow-x-visible">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:p-6 bg-light-gray rounded-4xl min-w-fit lg:min-w-0">
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

      {/* Navigation */}
      <div className="flex flex-row lg:flex-col gap-2 min-w-fit lg:min-w-0">
        <button className="text-left px-4 md:px-6 py-2 md:py-3 text-superdark-gray font-medium whitespace-nowrap">
          Dashboard
        </button>
        <button className="text-left px-4 md:px-6 py-3 md:py-4 bg-gradient-to-r from-mango-orange to-strawberry-red rounded-4xl text-white font-bold whitespace-nowrap">
          Calendar
        </button>
      </div>

      {/* Timer */}
      <div className="bg-light-gray rounded-4xl p-4 md:p-6 flex flex-col items-center gap-3 md:gap-4 min-w-fit lg:min-w-0">
        <div className="text-4xl md:text-6xl font-bold text-dark-gray">
          {formatTime(time)}
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className="px-4 md:px-6 py-2 bg-gray rounded-2xl text-white font-medium text-sm md:text-base"
          >
            {isRunning ? "stop" : "start"}
          </button>
        </div>
      </div>

      {/* User Profile */}
      <div className="bg-light-gray rounded-4xl p-3 md:p-4 flex items-center gap-2 md:gap-3 min-w-fit lg:min-w-0">
        <div className="w-10 h-10 md:w-12 md:h-12 bg-gray rounded-full flex items-center justify-center">
          <svg
            width="20"
            height="20"
            className="md:w-6 md:h-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
        </div>
        <span className="text-sm md:text-base text-superdark-gray font-medium">
          Ethan
        </span>
      </div>

      {/* Points Display */}
      <div className="bg-gradient-to-br from-mango-orange to-strawberry-red rounded-4xl p-6 md:p-8 flex items-center justify-center min-w-fit lg:min-w-0">
        <span className="text-5xl md:text-7xl font-bold text-white">
          {currentPoints}
        </span>
      </div>
    </div>
  );
};

export default Sidebar;
