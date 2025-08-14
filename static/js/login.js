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

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eye-icon');

    // Ensure correct eye icon is shown on load
    setEyeIcon(passwordInput, eyeIcon);

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = passwordInput.value;
            
            if (username.trim() === '' || password.trim() === '') {
                alert('Please enter both username and password');
                return;
            }
            
            const loginCard = document.querySelector('.transform');
            loginCard.classList.add('animate-pulse');
            
            setTimeout(() => {
                loginCard.classList.remove('animate-pulse');
                alert('Login successful! (This is a demo)');
            }, 1000);
        });
    }

    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            const svg = this.parentElement.querySelector('svg');
            if (svg) {
                svg.classList.add('text-[#e9a985]');
                svg.classList.remove('text-gray-300');
            }
        });
        
        input.addEventListener('blur', function() {
            const svg = this.parentElement.querySelector('svg');
            if (svg) {
                svg.classList.remove('text-[#e9a985]');
                svg.classList.add('text-gray-300');
            }
        });
    });
});
