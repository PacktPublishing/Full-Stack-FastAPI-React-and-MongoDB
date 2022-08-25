import React from "react";

const Card = ({ car }) => {
  const { make, brand, km, cm3, price, year } = car;

  return (
    <div className="shadow-md rounded-md flex flex-col justify-center p-2 bg-red-100 items-center hover:scale-105 transition-transform duration-150">
      <div className="font-bold">
        {brand} - {make} ({cm3}cm3)
      </div>
      <div>
        {km} Km / Year: {year}
      </div>
      <div>Price: {price} eur</div>
    </div>
  );
};

export default Card;
