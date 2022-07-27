import React from "react";

const Card = ({ car }) => {
  let { brand, price, make, year, km, cm3 } = car;
  return (
    <div className="card card-compact w-full bg-base-100 shadow-xl hover:scale-105 transition-transform">
      <figure>
        <img src="https://api.lorem.space/image/car?w=400&h=225" alt="Shoes" />
      </figure>
      <div className="card-body">
        <h2 className="card-title">
          {brand} {make}
        </h2>
        <div className="flex flex-col justify-between items-center">
          <div className="my-1">
            Year: {year} / Cm3: {cm3} / Km: {km}
          </div>
          <div className="my-1">
            Price: <span className="text-primary font-extrabold">{price}</span>{" "}
            EURO
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card;
