
import {Route, Routes} from "react-router-dom"


import Layout from "./components/Layout";
import HomePage from "./components/HomePage";
import Login from "./components/Login";
import Register from "./components/Register";
import Protected from "./components/Protected";
import Admin from "./components/Admin";
import NotFound from "./components/NotFound";
import NewCar from "./components/NewCar";
import RequireAuthentication from "./components/RequireAuthentication";

function App() {  

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="login" element={<Login/>} />
        <Route path="register" element={<Register/>} />

        <Route element={<RequireAuthentication />}>
          <Route path="protected" element={<Protected/>} />
          <Route path="admin" element={<Admin/>} />
          <Route path="/new" element={<NewCar/>} />
          <Route path="*" element={<NotFound/>} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
