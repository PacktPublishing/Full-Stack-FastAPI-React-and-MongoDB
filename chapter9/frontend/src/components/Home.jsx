// fetcher for SWR
import { useState } from "react";
import useSWR from "swr";
import Card from "./Card";
import CarsDropdown from "./CarsDropdown";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

const Home = () => {
  const [pageIndex, setPageIndex] = useState(1);
  const [brand, setBrand] = useState("");

  const { nextData, nextError } = useSWR(
    `${process.env.REACT_APP_API_URL}/cars/all?page=${
      pageIndex + 1
    }&brand=${brand}`,
    fetcher
  );

  const { data, error } = useSWR(
    `${process.env.REACT_APP_API_URL}/cars/all?page=${pageIndex}&brand=${brand}`,
    fetcher
  );

  if (error) return <div>`failed to load {process.env.REACT_APP_API_URL}`</div>;
  if (!data) return <div>loading...</div>;

  return (
    <div className="w-full p-8 my-10">
      <h1 className="font-bold text-lg text-center p-8 border border-gray-500">
        Explore Cars
      </h1>
      <div className="hidden">
        {JSON.stringify(nextData)} {JSON.stringify(nextError)}
      </div>

      <div className="flex flex-col lg:flex-row justify-between my-3">
        <CarsDropdown
          selectHandler={(event) => {
            setBrand(event.target.value);
            setPageIndex(1);
          }}
          allCars={true}
          elValue={brand}
        />
        <div className="">
          {pageIndex > 1 ? (
            <button
              className=" bg-red-800 text-white font-bold p-3 m-1 rounded-md w-36 md:w-40"
              onClick={() => setPageIndex(pageIndex - 1)}
            >
              Previous
            </button>
          ) : (
            <></>
          )}
          {pageIndex < data.pages ? (
            <button
              className=" bg-red-800 text-white font-bold p-3 m-1 rounded-md w-36 md:w-48"
              onClick={() => setPageIndex(pageIndex + 1)}
            >
              Next
            </button>
          ) : (
            <></>
          )}
        </div>
        <div className="flex flex-row justify-center items-center">
          Brand:
          <span className=" font-bold text-lg mx-2 text-gray-500">
            {brand ? brand : "All brands"}
          </span>
          Page:
          <span className=" font-bold text-lg mx-2 text-gray-500">
            {pageIndex} of {data.pages}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-4 md:grid-cols-5 gap-4">
        {data.results.map((car) => (
          <Card car={car} key={car._id} />
        ))}
      </div>
    </div>
  );
};

export default Home;
