let PUBLIC_KEY = "";
let KID = "";


function setEyeIcon(passwordInput, eyeIcon) {
    if (passwordInput.type === 'password') {
        // Slashed eye for hidden password
        eyeIcon.innerHTML = `
            <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 
            001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 
            14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 
            4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 
            1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
            <path d="M12.454 16.697L9.75 13.992a4 4 0 
            01-3.742-3.741L2.335 6.578A9.98 9.98 0 
            00.458 10c1.274 4.057 5.065 7 9.542 
            7 .847 0 1.669-.105 2.454-.303z" />
        `;
    } else {
        // Open eye for visible password
        eyeIcon.innerHTML = `
            <path d="M10 12a2 2 0 100-4 2 2 0 
            000 4z" />
            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 
            5.522 3 10 3s8.268 2.943 9.542 7c-1.274 
            4.057-5.064 7-9.542 7S1.732 14.057.458 
            10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
        `;
    }
}

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eye-icon');
    passwordInput.type = (passwordInput.type === 'password') ? 'text' : 'password';
    setEyeIcon(passwordInput, eyeIcon);
}


async function login(username, password) {
    const importedKey = await importPublicKey(PUBLIC_KEY);

    const credentials = {
        username: username,
        password: password,
        timestamp: Date.now()
    }

    const encryptedData = await encryptCredentials(importedKey, credentials);

    const response = await fetch('/auth', {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            kid: KID,
            encrypted_data: encryptedData
        })
    });

    return response.json()

}


document.addEventListener('DOMContentLoaded', async function () {
    await getPublicKey();  // fetch key on page load

    const refreshed = await refreshAccessToken();
    if (refreshed) {
        // Already logged in → redirect
        window.location.href = "/billing/";
        return;
    }

    const loginForm = document.getElementById('loginForm');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eye-icon');

    setEyeIcon(passwordInput, eyeIcon);

    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) { // <-- async here
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = passwordInput.value;

            if (username.trim() === '' || password.trim() === '') {
                alert('Please enter both username and password');
                return;
            }

            const loginCard = document.querySelector('.transform');
            loginCard.classList.add('animate-pulse');

            const res_json = await login(username, password); // <-- now works
            loginCard.classList.remove('animate-pulse');

            if (res_json.success) {
                sessionStorage.setItem("access",res_json.access_token);
                sessionStorage.setItem("userID", res_json.user.uid);
                sessionStorage.setItem("userDesignation", res_json.designation);
                sessionStorage.setItem("userName", res_json.user.name);
                window.location.href = '/billing/';
            } else if (res_json.expired) {
                await getPublicKey();

            }
            else {
                alert("Wrong Username or Password!");
            }
        });
    }
});

