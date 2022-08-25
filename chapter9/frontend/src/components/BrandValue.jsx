import { useState } from "react";
import useSWR from "swr";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import CarsDropdown from "./CarsDropdown";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = (val) => {
  let optObj = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: `Average ${val} of car models by brand`,
      },
    },
  };
  if (val === "year") {
    optObj["scales"] = {
      y: {
        min: 1980,
      },
    };
  }
  return optObj;
};

const fetcher = (...args) => fetch(...args).then((res) => res.json());

const BrandValue = ({ val }) => {
  const queryStr = `avg_${val}`;

  const [brand, setBrand] = useState("Fiat");

  const { data, error } = useSWR(
    `${process.env.REACT_APP_API_URL}/cars/brand/${val}/${brand}`,
    fetcher
  );

  if (error) return <div>failed to load</div>;
  if (!data) return <div>loading...</div>;

  const chartData = {
    labels: data.map((item) => {
      return item["_id"]["model"];
    }),
    datasets: [
      {
        label: brand,
        data: data.map((item) => Math.round(item[queryStr])),
        hoverBackgroundColor: ["#B91C1C"],
      },
    ],
  };

  return (
    <div className="w-full shadow-md my-5">
      <h1 className=" text-red-700 font-bold text-center">
        {val.toUpperCase()} by model for a given brand - {brand}
      </h1>

      <div className=" w-full text-center">
        <CarsDropdown
          selectHandler={(event) => setBrand(event.target.value)}
          elValue={brand}
        />
      </div>
      <div className="p-5 min-w-full">
        <Bar options={options(val)} data={chartData} />
      </div>
    </div>
  );
};

export default BrandValue;
