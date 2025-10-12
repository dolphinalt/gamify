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

const App = () => {
  const [currentPoints] = useState(250);
  const [dailyProgress] = useState(54);
  const [activeView, setActiveView] = useState<"dashboard" | "calendar">(
    "calendar"
  );

  return (
    <div className="flex flex-col p-4 md:p-7 min-h-screen bg-white gap-4">
      <DailyTasksCard progress={dailyProgress} />

      <div className="flex flex-col lg:flex-row gap-4">
        <div className="w-full lg:w-64">
          <Sidebar
            currentPoints={currentPoints}
            activeView={activeView}
            setActiveView={setActiveView}
          />
        </div>

        {activeView === "calendar" && (
          <>
            <div className="flex-1 flex flex-col gap-4 min-w-0">
              <div className="flex-1 bg-light-gray rounded-4xl p-4 md:p-8">
                <CalendarView />
              </div>
            </div>

            <div className="w-full lg:w-96 flex flex-col gap-4">
              <CalendarView isCompact />
              <TaskList />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default App;

/*
const App = () => {
  const [currentPoints] = useState(250);
  return (
    <>
      <div className="flex flex-row p-7 min-h-screen">
        <Sidebar currentPoints={currentPoints} />
        <CardGrid>
          <Card
            title="Assignment 1"
            description="This is the first assignment"
            points={10}
          />
          <Card
            title="Assignment 2"
            description="This is the second assignment"
            points={20}
          />
          <Card
            title="Assignment 3"
            description="This is the third assignment"
            points={30}
          />
          <Card
            title="Assignment 3"
            description="This is the third assignment"
            points={30}
          />
          <Card
            title="Assignment 3"
            description="This is the third assignment"
            points={30}
          />
        </CardGrid>
        <RewardCardGrid>
          <RewardCard title="Reward 1" description="Reward 1" points={100} />
          <RewardCard title="Reward 2" description="Reward 2" points={200} />
          <RewardCard title="Reward 3" description="Reward 3" points={300} />
          <RewardCard title="Reward 3" description="Reward 3" points={300} />
          <RewardCard title="Reward 3" description="Reward 3" points={300} />
          <RewardCard title="Reward 3" description="Reward 3" points={300} />
        </RewardCardGrid>
      </div>
    </>
  );
};

export default App;
*/
