const App = () => {
  ping();
  return (
    <>
      <h1>Hello, World!</h1>
    </>
  );
};

const ping = async (): Promise<void> => {
  try {
    const response = await fetch("/api/ping");
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
};

export default App;
