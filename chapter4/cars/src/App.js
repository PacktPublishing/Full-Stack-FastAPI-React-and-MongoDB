import Header from "./components/Header";
import Card from "./components/Card";
import {useState} from 'react'

function App() {

  const data = [
    {brand:"Fiat", color:"green", model:"500L", price:7000, "year":2020,"id":1},
    {brand:"Peugeot", color:"red", model:"5008", price:8000, "year":2018,"id":2},
    {brand:"Volkswagen", color:"white", model:"Golf 7", price:8500, "year":2019,"id":3},
    {brand:"Fiat", color:"green", model:"Tipo", price:10000, "year":2019,"id":4},
    {brand:"Kia", color:"black", model:"Ceed", price:6000, "year":2010,"id":5},
    {brand:"Volkswagen", color:"white", model:"Golf 7", price:8500, "year":2019,"id":15},
    {brand:"Fiat", color:"gray", model:"Ritmo", price:300, "year":1990,"id":21}
  ]

  const [budget, setBudget] = useState(4000)
  const onChangeHandler = event=>setBudget(event.target.value)

  return (
    <div className="App max-w-3xl mx-auto h-full">
     <Header/>
     <div className="border-2 border-yellow-500 my-5 p-3">Your current budget is: <span className="">{budget}</span></div>
      <div className="grid grid-cols-3 my-3 gap-3">
        {data.map(
          (el)=>{
            
            return (
              (el.price<budget)&&<Card key={el.id} car = {el} />
               )
          }
        )}
      </div>
      <div className="bg-gray-300 rounded-md p-3">
        <label htmlFor="budget">Budget:</label>
        <input type="number" onChange={onChangeHandler} id="budget" name="budget" min="300" max="10000" step="100" value={budget}></input>
      </div>   
    </div>
  );
}
export default App;
