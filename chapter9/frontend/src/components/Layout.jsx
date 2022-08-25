import Header from "./Header";
import Footer from "./Footer";

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex-1 flex flex-row justify-center items-start mx-auto container my-10">
        {children}
      </div>
      <Footer />
    </div>
  );
};
export default Layout;
