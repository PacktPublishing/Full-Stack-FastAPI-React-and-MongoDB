import useSWR from "swr";

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";

import { schemePastel1 } from "d3-scale-chromatic";

const colors = schemePastel1;

ChartJS.register(ArcElement, Tooltip, Legend);

const fetcher = (...args) => fetch(...args).then((res) => res.json());

const BrandCount = () => {
  const { data, error } = useSWR(
    `${process.env.REACT_APP_API_URL}/cars/brand/count`,
    fetcher
  );
  if (error) return <div>failed to load</div>;
  if (!data) return <div>loading...</div>;

  const chartData = {
    labels: data.map((item) => {
      return item["_id"];
    }),
    datasets: [
      {
        data: data.map((item) => item.count),
        backgroundColor: data.map((item, index) => colors[index]),
        borderWidth: 3,
      },
    ],
  };

  return (
    <div className="w-full my-5 shadow-md">
      <h1 className=" text-red-700 font-bold text-center">
        Vehicle Count by Brand
      </h1>

      <div className="p-5 min-w-full">
        <Pie data={chartData} />
      </div>
    </div>
  );
};

export default BrandCount;
