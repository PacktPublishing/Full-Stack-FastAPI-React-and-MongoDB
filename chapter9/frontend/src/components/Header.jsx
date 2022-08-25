import { NavLink } from "react-router-dom";
const Header = () => {
  return (
    <div className="bg-white w-full py-2">
      <div className="flex flex-row justify-center space-x-4 h-10 items-center text-red-800 font-bold text-lg">
        <NavLink
          className={({ isActive }) => (isActive ? "active menu" : "menu")}
          to="/"
        >
          Cars
        </NavLink>
        <NavLink
          className={({ isActive }) => (isActive ? "active menu" : "menu")}
          to="/dashboard"
        >
          Dashboard
        </NavLink>
        <NavLink
          className={({ isActive }) => (isActive ? "active menu" : "menu")}
          to="/report"
        >
          Report
        </NavLink>
      </div>
    </div>
  );
};
export default Header;
