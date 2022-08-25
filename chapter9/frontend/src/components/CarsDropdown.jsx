import React from "react";

const CarsDropdown = ({ selectHandler, allCars, elValue }) => {
  const carBrands = [
    "Fiat",
    "Opel",
    "Renault",
    "Peugeot",
    "VW",
    "Ford",
    "Honda",
    "Toyota",
  ];
  return (
    <select
      onChange={selectHandler}
      className="px-2 py-1 my-2 mx-2 rounded-lg form-select md:w-1/6"
      value={elValue}
    >
      {allCars && <option value="">All brands</option>}
      {carBrands.map((brand) => {
        return (
          <option value={brand} key={brand}>
            {brand}
          </option>
        );
      })}
    </select>
  );
};

CarsDropdown.defaultProps = {
  allCars: false,
  elValue: "",
};
export default CarsDropdown;
