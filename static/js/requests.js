async function getPublicKey() {
    const response = await fetch('/auth/tmpKey', {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    KID = data.kid;
    PUBLIC_KEY = data.public_key;
}


function pemToArrayBuffer(pem) {
    // Remove the BEGIN/END lines and newlines
    const b64 = pem
        .replace(/-----BEGIN PUBLIC KEY-----/, '')
        .replace(/-----END PUBLIC KEY-----/, '')
        .replace(/\s+/g, '');
    const binary = atob(b64);
    const len = binary.length;
    const buffer = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        buffer[i] = binary.charCodeAt(i);
    }
    return buffer.buffer;
}

async function importPublicKey(pem) {
    const arrayBuffer = pemToArrayBuffer(pem);
    return await crypto.subtle.importKey(
        "spki",                   // Public key format
        arrayBuffer,              // Key data
        { name: "RSA-OAEP", hash: "SHA-256" }, // Algorithm
        false,                    // Not extractable
        ["encrypt"]               // Only for encryption
    );
}

async function apiFetch(url, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers["Authorization"] = `Bearer ${sessionStorage.access}`;
    let res = await fetch(url, options);

    if (res.status === 401) {
        // Access token expired → try refresh
        const refreshed = await refreshAccessToken();
        if (!refreshed) {
            // Refresh failed → force login
            window.location.href = "/auth/login";
            return;
        }

        // Retry request with new token
        options.headers["Authorization"] = `Bearer ${sessionStorage.access}`;
        res = await fetch(url, options);
    }

    return res.json();
}


async function refreshAccessToken() {
    try {
        const res = await fetch("/auth/refresh", {
            method: "POST",
            credentials: "include" // VERY important so cookies are sent
        });

        if (res.status >= 400) return false;

        const data = await res.json();
        sessionStorage.setItem("access",data.access_token);
        sessionStorage.setItem("accessTokenExpiry", Date.now() + (data.expires_in * 1000));
        return true;
    } catch (e) {
        console.error("Failed to refresh token", e);
        return false;
    }
}


async function encryptCredentials(publicKey, credentialsObj) {
    const encoder = new TextEncoder();
    const encoded = encoder.encode(JSON.stringify(credentialsObj));
    const encrypted = await crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        publicKey,
        encoded
    );
    return btoa(String.fromCharCode(...new Uint8Array(encrypted))); // Base64 encode
}

