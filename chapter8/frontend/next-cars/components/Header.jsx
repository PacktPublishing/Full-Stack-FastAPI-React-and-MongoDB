import Link from "next/link";
import useAuth from "../hooks/useAuth";
import { useEffect } from "react";

const Header = () => {
  const { user, setUser, loading, setLoading } = useAuth();
  useEffect(() => {
    (async () => {
      const userData = await fetch("/api/user");
      try {
        const user = await userData.json();

        setUser(user);
      } catch (error) {
        // if error: set user to null, destroy the cookie
        setUser(null);
      }
    })();
  }, []);
  return (
    <div className=" text-orange-600 py-2 font-bold flex flex-row justify-between items-center">
      <div>
        {loading ? <span>Loading...</span> : ""}
        <Link href="/">
          <a>
            FARM Cars
            {user ? (
              <span className="mx-2 text-gray-500">
                {user.username} ({user.role})
              </span>
            ) : (
              ""
            )}
          </a>
        </Link>
      </div>
      <ul className="flex flex-row space-x-4 ">
        <li>
          <Link href="/cars">
            <a>Cars</a>
          </Link>
        </li>
        {user && user.role === "ADMIN" ? (
          <li>
            <Link href="/cars/add">
              <a>Add Car</a>
            </Link>
          </li>
        ) : (
          ""
        )}

        {!user ? (
          <>
            <li>
              <Link href="/account/register">
                <a>Register</a>
              </Link>
            </li>
            <li>
              <Link href="/account/login">
                <a>Login</a>
              </Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link href="/account/logout">
                <a>Log out {user.username}</a>
              </Link>
            </li>
          </>
        )}
      </ul>
    </div>
  );
};
export default Header;
