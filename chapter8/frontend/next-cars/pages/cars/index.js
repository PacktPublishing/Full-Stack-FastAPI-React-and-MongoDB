import Card from "../../components/Card"

export const getServerSideProps = async () => {


 
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/cars/`);
  const cars = await res.json();

  return {
    props: {
      cars,
      revalidate: 10,
    },
  };
};

const Cars = ({ cars }) => {
 
  return (
    <div className="flex flex-col justify-center items-center w-full">
      <h1 className=" text-orange-600 font-bold text-3xl my-5">Available Cars</h1>

      <div className="grid lg:grid-cols-4 grid-cols-3 gap-3">
        {cars.map((car) => {
         const {_id, brand, make, picture, year, km, cm3, price} = car
          return (
            
              <Card
                key={_id}
                brand={brand}
                id={_id}
                make={make}
                url={picture}
                year={year} 
                km={km}
                cm3={cm3}
                price={price}
                />
            
          );
        })}
      </div>
    </div>
  );
};

export default Cars;
