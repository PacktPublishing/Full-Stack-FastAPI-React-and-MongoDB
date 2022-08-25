import { useState } from "react";

const Report = () => {
  const [email, setEmail] = useState("");
  const [carsNum, setCarsNum] = useState(10);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleForm = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await fetch(`${process.env.REACT_APP_API_URL}/cars/email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, cars_num: carsNum }),
    });

    if (res.ok) {
      setLoading(false);
      setMessage(`Report with ${carsNum} cars sent to ${email}!`);
    }
  };

  return (
    <div className="w-full p-8 my-10">
      <h1 className="font-bold text-lg text-center p-8 border border-gray-500 w-full ">
        Generate Report
      </h1>
      <div className="flex flex-col justify-center items-center h-full py-5">
        {loading && (
          <div className="border border-green-600 w-2/3 p-10 text-center font-thin my-4 text-lg animate-pulse">
            Generating and sending report in the background...
          </div>
        )}

        {message && (
          <div className="border border-green-600 w-2/3 p-10 text-center font-thin my-4 text-lg animate-pulse">
            {message}
          </div>
        )}

        {!loading && !message && (
          <form className="flex flex-col justify-center" onSubmit={handleForm}>
            <label htmlFor="email">Email</label>
            <input
              type="text"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="px-2 py-1 my-2 rounded-full"
            />
            <label htmlFor="carsNum">Number of cars</label>
            <input
              type="number"
              id="carsNum"
              name="carsNum"
              max={50}
              min={5}
              value={carsNum}
              onChange={(e) => setCarsNum(e.target.value)}
              className="p-2 py-1 my-2 rounded-full"
            />
            <button
              type="submit"
              className="block rounded-md bg-green-600 text-white px-3 py-1 m-4 text-lg hover:bg-green-500 transition-colors duration-300"
            >
              Send report
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default Report;
