import config from 'config';
import { authHeader, handleResponse } from '../_helpers';

export const sigService = {
    postSig,
    getSigs,
    createSigReviewed,
    updateSigReviewed
};

function postSig(sig_text) {
    const requestOptions = {
        cache: 'no-store',
        method: 'POST',
        headers: authHeader(),
        body: JSON.stringify({"sig_text": sig_text})
    };

    return fetch(`${config.apiUrl}/sig/`, requestOptions)
            .then(handleResponse)
            .then(sig => {
                return sig;
            });
    
}


function getSigs(page) {
    const urlParams = new URLSearchParams(window.location.search);
    const pageOptions = page ? 'page=' + page : '';
    let requestParams = (urlParams.toString() != '' ? '?' : '') + urlParams.toString() + (urlParams.toString() != '' ? '&' : '?') + pageOptions;
    const requestOptions = {
        cache: 'no-store',
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/sig/${requestParams}`, requestOptions).then(handleResponse);
}

function createSigReviewed(sig_reviewed, user) {
    sig_reviewed.owner = user.id

    const requestOptions = {
        cache: 'no-store',
        method: 'POST',
        headers: authHeader(),
        body: JSON.stringify(sig_reviewed)
    };

    return fetch(`${config.apiUrl}/sig_reviewed/`, requestOptions)
        .then(handleResponse)
        .then(sig_reviewed => {
            return sig_reviewed;
        });
}

function updateSigReviewed(sig_reviewed, user) {
    sig_reviewed.owner = user.id

    const requestOptions = {
        cache: 'no-store',
        method: 'PUT',
        headers: authHeader(),
        body: JSON.stringify(sig_reviewed)
    };

    return fetch(`${config.apiUrl}/sig_reviewed/${sig_reviewed.id}/`, requestOptions)
        .then(handleResponse)
        .then(sig_reviewed => {
            return sig_reviewed;
        });
}