import { useState } from "react";
import Sidebar from "./components/Sidebar";
import DailyTasksCard from "./components/DailyTasksCard";
import CalendarView from "./components/CalendarView";
import Calendar from "./components/Calendar";
import TaskList from "./components/TaskList";
import Card from "./components/Card";
import RewardCard from "./components/RewardCard";
import NewTask from "./components/NewTask";
import CategorySelection from "./components/CategorySelection";
import Header from "./components/Header";

const App = () => {
  const [currentPoints] = useState(250);
  const [dailyProgress] = useState(54);
  const [activeView, setActiveView] = useState<"dashboard" | "calendar">(
    "dashboard"
  );
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [popupActive] = useState<false | true>(true);

  const changeDisplay = (newView: "dashboard" | "calendar") => {
    if (newView !== activeView) {
      setIsTransitioning(true);
      setTimeout(() => {
        setActiveView(newView);
        setIsTransitioning(false);
      }, 150);
    }
  };

  return (
    <body className="overscroll-none">
      <div className="flex h-screen bg-white gap-2 md:gap-3 lg:gap-4 p-2 md:p-3 lg:p-4">
        {/* Sidebar */}
        <div className="w-48 sm:w-56 md:w-64 flex-shrink-0">
          <Sidebar
            currentPoints={currentPoints}
            activeView={activeView}
            setActiveView={changeDisplay}
          />
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col gap-4 overflow-hidden">
          {/* Daily Tasks Card */}
          <div className="flex-shrink-0 px-2 md:px-0">
            <DailyTasksCard progress={dailyProgress} />
          </div>

          {/* Content Area */}
          <div
            className={`flex-1 flex transition-opacity duration-300 overflow-hidden gap-1 md:gap-2 lg:gap-3 ${
              isTransitioning ? "opacity-0" : "opacity-100"
            }`}
          >
            {activeView === "calendar" && (
              <>
                {/* Left Column - CalendarView */}
                <div className="flex-[1.4] min-w-0">
                  <CalendarView />
                </div>

                {/* Right Column - Calendar and TaskList stacked */}
                <div className="flex-[1] min-w-0 flex flex-col space-y-2 md:space-y-3 lg:space-y-4">
                  <div className="flex-[1] min-h-0 min-w-0 overflow-scroll">
                    <Calendar />
                  </div>

                  <div className="flex-[0.5] min-h-0 min-w-0">
                    <TaskList />
                  </div>
                </div>
              </>
            )}

            {activeView === "dashboard" && (
              <div className="flex-1 flex flex-col">
                <div className="flex gap-2 md:gap-3 lg:gap-4 mb-2 md:mb-3 lg:mb-4 flex-shrink-0">
                  <div className="flex-[2] min-w-0 pr-2">
                    <CategorySelection />
                  </div>
                  <div className="flex-[1] min-w-0 pr-2">
                    <Header />
                  </div>
                </div>
                <div className="flex-1 flex gap-4 min-h-0 overflow-hidden">
                  {/* Tasks Grid */}
                  <div className="flex-[2] min-w-0 pr-1 md:pr-2 overflow-y-auto overflow-x-visible">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4 lg:gap-6 p-2 md:p-3 lg:p-4 pb-6 md:pb-8">
                      <Card
                        type="task"
                        title="Assignment 1"
                        description="This is the first assignment"
                        points={10}
                      />
                      <Card
                        type="task"
                        title="Assignment 2"
                        description="This is the second assignment"
                        points={20}
                      />
                      <Card
                        type="task"
                        title="Assignment 3"
                        description="This is the third assignment"
                        points={30}
                      />
                      <Card
                        type="task"
                        title="Assignment 4"
                        description="This is the fourth assignment"
                        points={40}
                      />
                      <Card
                        type="task"
                        title="Assignment 5"
                        description="This is the fifth assignment"
                        points={50}
                      />
                      <Card
                        type="task"
                        title="Assignment 6"
                        description="This is the sixth assignment"
                        points={50}
                      />
                      <Card
                        type="task"
                        title="Assignment 7"
                        description="This is the seventh assignment"
                        points={50}
                      />
                      <Card
                        type="task"
                        title="Assignment 8"
                        description="This is the eighth assignment"
                        points={50}
                      />
                      <Card
                        type="task"
                        title="Assignment 9"
                        description="This is the ninth assignment"
                        points={50}
                      />
                      <Card
                        type="task"
                        title="Assignment 10"
                        description="This is the tenth assignment"
                        points={50}
                      />
                      <Card type="new" />
                    </div>
                  </div>

                  {/* Rewards Grid */}
                  <div className="flex-1 min-w-0 hidden md:flex md:flex-col">
                    <div className="grid grid-cols-2 gap-3 md:gap-4 lg:gap-6 p-2 md:p-3 lg:p-4 pb-6 md:pb-8">
                      <RewardCard points={50} active={currentPoints >= 50} />
                      <RewardCard points={100} active={currentPoints >= 100} />
                      <RewardCard points={200} active={currentPoints >= 200} />
                      <RewardCard points={300} active={currentPoints >= 300} />
                      <RewardCard points={500} active={currentPoints >= 500} />
                      <RewardCard points={750} active={currentPoints >= 750} />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </body>
  );
};

export default App;
