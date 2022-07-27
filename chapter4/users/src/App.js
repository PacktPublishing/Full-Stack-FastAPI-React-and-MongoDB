import Header from "./components/Header";
import {useState, useEffect} from 'react'

function App() {

  let [users, setUsers] = useState([])
  let [page, setPage] = useState(1)
  
  useEffect(()=>{
    fetch(`https://reqres.in/api/users?page=${page}`)
    .then(response=>response.json())
    .then(json=>setUsers(json['data']))
    },[page])


  return (
    <div className="App max-w-3xl mx-auto h-full">
     <Header/>
     <button className="border border-gray-500 rounded-md p-2 m-5" onClick={()=>{page===1?setPage(2):setPage(1)}}>Toggle users</button>
      <ul>
        {users&&users.map(el=>{
        return (
          <li key={el.id}>{el.email}</li>
          )
        })}
  </ul>
    </div>
  );
}
export default App;