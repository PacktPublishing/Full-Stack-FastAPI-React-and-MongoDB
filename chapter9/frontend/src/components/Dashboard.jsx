import BrandCount from "./BrandCount";
import ModelCount from "./ModelCount";
import BrandValue from "./BrandValue";

const Dashboard = () => {
  return (
    <div className=" w-full p-8 my-10">
      <h1 className="font-bold text-lg text-center p-8 border border-gray-500">
        DashBoard
      </h1>
      <div className="grid 2xl:grid-cols-2 gap-2">
        <BrandValue val={"price"} />
        <BrandValue val={"km"} />
        <BrandValue val={"cm3"} />
        <BrandValue val={"year"} />
        <BrandCount />
        <ModelCount />
      </div>
    </div>
  );
};

export default Dashboard;
