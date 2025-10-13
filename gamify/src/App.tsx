/*import Card from "./components/Card";
import CardGrid from "./components/CardGrid";
import RewardCard from "./components/RewardCard";
import RewardCardGrid from "./components/RewardCardGrid";
*/
import { useState } from "react";
import Sidebar from "./components/Sidebar";
import DailyTasksCard from "./components/DailyTasksCard";
import CalendarView from "./components/CalendarView";
import TaskList from "./components/TaskList";
import Card from "./components/Card";
import RewardCard from "./components/RewardCard";

const App = () => {
  const [currentPoints] = useState(250);
  const [dailyProgress] = useState(54);
  const [activeView, setActiveView] = useState<"dashboard" | "calendar">(
    "dashboard"
  );

  return (
    <>
      <div className="flex h-screen gap-4 p-4">
        <div className="w-64 flex-shrink-0">
          <Sidebar
            currentPoints={currentPoints}
            activeView={activeView}
            setActiveView={setActiveView}
          />
        </div>
        <div className="flex-1 flex flex-col gap-4 overflow-hidden">
          <div className="flex-shrink-0">
            <DailyTasksCard progress={dailyProgress} />
          </div>
          {activeView === "calendar" && (
            <div className="bg-white rounded-xl p-4 h-16">
              <div className="flex-1 grid grid-cols-2 gap-4">
                <div className="bg-light-gray rounded-4xl p-4">
                  <CalendarView />
                </div>
                <div className="bg-light-gray rounded-4xl p-4">
                  <TaskList />
                </div>
              </div>
            </div>
          )}
          {activeView === "dashboard" && (
            <div className="flex-1 flex gap-4 min-h-0">
              <div className="flex-[2] min-w-0">
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-2">
                  <Card type="task" title="Assignment 1" description="This is the first assignment" points={10} />
                  <Card type="task" title="Assignment 2" description="This is the second assignment" points={20} />
                  <Card type="task" title="Assignment 3" description="This is the third assignment" points={30} />
                  <Card type="task" title="Assignment 3" description="This is the third assignment" points={30} />
                  <Card type="task" title="Assignment 3" description="This is the third assignment" points={30} />
                  <Card type="new"/>
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-2">
                  <RewardCard points={50} active={currentPoints >= 50} />
                  <RewardCard points={100} active={currentPoints >= 100} />
                  <RewardCard points={200} active={currentPoints >= 200} />
                  <RewardCard points={300} active={currentPoints >= 300} />
                  <RewardCard points={500} active={currentPoints >= 500} />
                  <RewardCard points={750} active={currentPoints >= 750} />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default App;