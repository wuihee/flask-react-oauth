import { useEffect, useState } from "react";

type UserInfo = { id: string; name: string; email: string };

const App = () => {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  useEffect(() => {
    console.log("Updating user info...");
    const getUserInfo = async (): Promise<void> => {
      try {
        const response = await fetch("/api/user");
        const data = await response.json();
        setUserInfo(data);
      } catch (error) {
        console.error(error);
      }
    };
    getUserInfo();
  }, []);

  const handleLogin = (): void => {
    window.location.href = "http://localhost:5001/api/login";
  };

  const handleLogout = async (): Promise<void> => {
    try {
      const response = await fetch("/api/logout");
      setUserInfo(null);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <h1>Homepage</h1>
      {userInfo && <h2>Welcome {userInfo.name}</h2>}
      <button onClick={handleLogin}>Login</button>
      {userInfo && <button onClick={handleLogout}>Log Out</button>}
    </>
  );
};

export default App;
