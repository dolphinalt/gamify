import Dropdown from "./Dropdown";

const CategorySelection = () => {
  return (
    <div className="pt-6 pl-4 flex flex-col gap-1">
      <div className="text-dark-gray font-bold text-sm">CATEGORY</div>
      <Dropdown items={["I&C SCI 6B", "I&C SCI H32", "WRITING 60", "SOCIOL 1", "All"]} />
      <hr className="w-full h-2 rounded-full bg-gray border-0 font-extralight"></hr>
    </div>
  );
};

export default CategorySelection;
