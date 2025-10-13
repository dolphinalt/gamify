import { useState } from "react";

interface DropdownProps {
  items: string[];
}

function Dropdown({ items }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(items[items.length - 1]);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (value: string) => {
    setSelectedValue(value);
    setIsOpen(false);
  };

  return (
    <div className="relative inline-block w-48 text-left">
      <button
        onClick={toggleDropdown}
        className="rounded-md hover:bg-gray-50 font-bold"
      >
        {selectedValue}
      </button>

      {isOpen && (
        <ul className="absolute top-full left-0 mt-1 w-full rounded-md z-50 max-h-60 overflow-auto">
          {items.map((item) => (
            <li
              key={item}
              onClick={() => handleOptionClick(item)}
              className="py-2 bg-white cursor-pointer text-superdark-gray first:rounded-t-md last:rounded-b-md"
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Dropdown;
