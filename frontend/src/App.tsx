const App = () => {
  const handleLogin = (): void => {
    window.location.href = "http://localhost:5000/api/login";
  };

  return (
    <>
      <h1>Homepage</h1>
      <button onClick={handleLogin}>Login</button>
    </>
  );
};

export default App;
