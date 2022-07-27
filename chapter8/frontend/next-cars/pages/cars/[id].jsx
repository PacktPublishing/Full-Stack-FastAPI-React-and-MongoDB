import Image from "next/image";
export const getStaticPaths = async () => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/cars`);
  const cars = await res.json();

  const paths = cars.map((car) => ({
    params: { id: car._id },
  }));

  return { paths, fallback: "blocking" };
};

export const getStaticProps = async ({ params: { id } }) => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/cars/${id}`);
  const car = await res.json();

  return {
    props: { car },
    revalidate: 10,
  };
};

const CarById = ({ car }) => {
  return (
    <div className="flex flex-col justify-center items-center min-h-full">
      <h1 className="text-xl font-bold text-gray-700">
        {car.brand} - {car.make}
      </h1>
      <div className=" bg-white p-5 shadow-md rounded-lg">
        <Image src={car.picture} width={700} height={400} />
      </div>
      <div className=" text-gray-500 m-5">{`This fine car was manufactured in ${car.year}, it made just ${car.km} km and it sports a ${car.cm3} cm3 engine.`}</div>

      <div className="text-gray-500 font-bold">Price: {car.price} eur</div>
    </div>
  );
};

export default CarById;
