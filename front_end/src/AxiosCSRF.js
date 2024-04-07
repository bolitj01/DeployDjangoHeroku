import axios from 'axios';

// Create an Axios instance
const axiosCSRF = axios.create();

// Function to get CSRF token from cookies
const getCsrfToken = () => {
    let csrfToken = '';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmedCookie = cookie.trim();
        if (trimmedCookie.startsWith('csrftoken=')) {
            csrfToken = trimmedCookie.substring('csrftoken='.length);
            break;
        }
    }
    return csrfToken;
};

// Set up request interceptor
axiosCSRF.interceptors.request.use(config => {
    config.headers['X-CSRFToken'] = getCsrfToken();
    // Ensure credentials are sent with each request
    config.withCredentials = true;
    return config;
}, error => {
    return Promise.reject(error);
});

export default axiosCSRF;
