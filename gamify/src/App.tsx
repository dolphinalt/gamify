import Card from "./components/Card";
import CardGrid from "./components/CardGrid";
import RewardCard from "./components/RewardCard";
import RewardCardGrid from "./components/RewardCardGrid";
import Sidebar from "./components/Sidebar";

const App = () => {
  return (
    <>
      <div className="flex flex-row p-7 min-h-screen">
        <Sidebar />
        <CardGrid>
          <Card title="Assignment 1" description="This is the first assignment" points={10} />
          <Card title="Assignment 2" description="This is the second assignment" points={20} />
          <Card title="Assignment 3" description="This is the third assignment" points={30} />
          <Card title="Assignment 3" description="This is the third assignment" points={30} />
          <Card title="Assignment 3" description="This is the third assignment" points={30} />
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