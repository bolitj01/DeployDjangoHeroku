import { useState, useEffect } from 'react';
import axios from 'axios';
import Todo from './Todo';
import CreateTodo from './CreateTodo';
import { useNavigate } from 'react-router-dom';

const TodoList = () => {

    const navigate = useNavigate();

    const [todos, setTodos] = useState([]);

    const logout = async () => {
        try {
            const response = await axios.get(
                '/api/user/logout/',
            );
            console.log('Logged out:', response.data);
            navigate('/login');
        }
        catch (error) {
            console.error('Failed to logout:', error);
        }
    }

    useEffect(() => {
        // Define the function to fetch todos
        const fetchTodos = async () => {
          try {
            const response = await axios.get('/api/todo/mv/todos/');
            console.log('Todos fetched:', response.data);
            setTodos(response.data); // Assuming the backend returns an array of todos
          } catch (error) {
            console.error('Error fetching todos:', error);
          }
        };
    
        // Call fetchTodos initially and set up the interval for repeating the call
        fetchTodos();
        const intervalId = setInterval(fetchTodos, 2000); // Fetch todos every 2 seconds
    
        // Clean up the interval on component unmount
        return () => clearInterval(intervalId);
      }, []);

    const deleteTodo = async (title) => {
        try {
            const response = await axios.delete(
                `/api/todo/mv/todos/${title}/`,
            );
            console.log('Todo deleted.');
            setTodos(todos.filter(todo => todo.title !== title));
        } catch (error) {
            console.error('Failed to delete todo:', error);
        }
    }

    const addTodo = (newTodo) => {
        setTodos([...todos, newTodo]);
    }

    const toggleCompleted = async (title) => {
        const todo = todos.find(todo => todo.title === title);
        const updatedTodo = { ...todo, completed: !todo.completed };
        try {
            const response = await axios.put(
                `/api/todo/toggle_completed/`,
                updatedTodo,
            );
            console.log('Todo updated: ', response.data);
            setTodos(todos.map(todo => todo.title === title ? updatedTodo : todo));
        } catch (error) {
            console.error('Failed to update todo:', error);
        }
    }

    return (
        <>
            <button onClick={logout}>Logout</button>
            <CreateTodo addTodo={addTodo}/>
            <div>
                <h2>Todo List</h2>
                {todos.map(todo =>
                        <Todo
                            key={todo.id}
                            title={todo.title}
                            description={todo.description}
                            completed={todo.completed}
                            toggleCompleted={toggleCompleted}
                            deleteTodo={deleteTodo}
                        />)}
            </div>
        </>
    );
};

export default TodoList;
