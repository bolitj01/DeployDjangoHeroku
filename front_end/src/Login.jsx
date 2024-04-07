import { useState } from 'react';
import axiosCSRF from './AxiosCSRF.js';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {

    const navigate = useNavigate();

    const [loginData, setLoginData] = useState({
        username: '',
        password: '',
    });

    const handleChange = (e) => {
        setLoginData({ ...loginData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log('Logging in user', loginData);
            const response = await axiosCSRF.post(
                '/api/user/login/',
                loginData
            );
            console.log('Login successful', response.data);
            navigate('/');
        } catch (error) {
            console.error('Login failed', error);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit}>
                <h2>Login</h2>
                <input
                    type="text"
                    name="username"
                    value={loginData.username}
                    onChange={handleChange}
                    placeholder="Username"
                    required
                />
                <input
                    type="password"
                    name="password"
                    value={loginData.password}
                    onChange={handleChange}
                    placeholder="Password"
                    required
                />
                <button type="submit">Login</button>
            </form>
            <Link to="/register">Register</Link>
        </>
    );
};

export default Login;
