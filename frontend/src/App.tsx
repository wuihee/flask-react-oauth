import { useState } from "react";

type UserInfo = { id: string; name: string; email: string };

const App = () => {
  const [userInfo, setUserInfo] = useState<UserInfo>();

  const handleLogin = (): void => {
    window.location.href = "http://localhost:5000/api/login";
    getUserInfo();
  };

  const getUserInfo = async (): Promise<void> => {
    try {
      const response = await fetch("/api/user");
      setUserInfo(await response.json());
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <h1>Homepage</h1>
      {userInfo && <h2>Welcome {userInfo.name}</h2>}
      <button onClick={handleLogin}>Login</button>
    </>
  );
};

export default App;
