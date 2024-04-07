import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import TodoList from './TodoList';
import { useCheckLogin } from './hooks/useCheckLogin';

function App() {

  const { isLoggedIn, isLoading } = useCheckLogin();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={isLoggedIn ? <TodoList /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
