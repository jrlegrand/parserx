import config from 'config';
import { authHeader, handleResponse } from '../_helpers';

export const userService = {
    login,
    logout,
    getAll
};

function getUserDetails(auth_token) {
    const requestOptions = {
        cache: 'no-store',
        method: 'GET',
        headers: { 'Authorization': 'Token ' + auth_token },
    };

    return fetch(`${config.apiUrl}/auth/users/me/`, requestOptions)
        .then(handleResponse)
        .then(user => { user.auth_token = auth_token; return user; });
}

function login(username, password) {
    const requestOptions = {
        cache: 'no-store',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    };

    return fetch(`${config.apiUrl}/auth/token/login/`, requestOptions)
        .then(handleResponse)
        .then(user => { return getUserDetails(user.auth_token) })
        .then(user => {
            // login successful if there's a user in the response
            if (user) {
                // store user details and basic auth credentials in local storage 
                // to keep user logged in between page refreshes
                // TODO: grab user ID too
                console.log(user)
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/auth/users/`, requestOptions).then(handleResponse);
}