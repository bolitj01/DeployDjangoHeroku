import { useState, useEffect } from 'react';
import axiosCSRF from '../AxiosCSRF.js';

export const useCheckLogin = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isLoading, setIsLoading] = useState(true); // Track loading state

    useEffect(() => {
        const checkLoginStatus = async () => {
            try {
                const response = await axiosCSRF.get('/api/user/is_logged_in/');
                setIsLoggedIn(response.data.is_logged_in); // Assuming the backend sends this structure
                console.log('Login status:', response.data);
            } catch (error) {
                console.error('Error checking login status:', error);
            } finally {
                setIsLoading(false); // Ensure loading is set to false after the check
            }
        };

        checkLoginStatus();
    }, []);

    return { isLoggedIn, isLoading };
};
