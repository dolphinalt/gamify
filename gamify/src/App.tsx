/*import Card from "./components/Card";
import CardGrid from "./components/CardGrid";
import RewardCard from "./components/RewardCard";
import RewardCardGrid from "./components/RewardCardGrid";
*/
import DailyTasksCard from "./components/DailyTasksCard";
import CalendarView from "./components/CalendarView";
import TaskList from "./components/TaskList";
import Sidebar from "./components/Sidebar";
import { useState } from "react";

const App = () => {
  const [currentPoints] = useState(100);
  const [dailyProgress] = useState(10);

  return (
    <div className="flex flex-row p-7 min-h-screen bg-white gap-4">
      <Sidebar currentPoints={currentPoints} />

      <div className="flex-1 flex flex-col gap-4">
        <DailyTasksCard progress={dailyProgress} />

        <div className="flex-1 bg-light-gray rounded-4xl p-8">
          <CalendarView />
        </div>
      </div>

      <div className="w-96 flex flex-col gap-4">
        <CalendarView isCompact />
        <TaskList />
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
