import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const RequireAuthentication = () => {
  const { auth } = useAuth();

  return auth?.username ? <Outlet /> : <Navigate to="/login" />;
};

export default RequireAuthentication;
