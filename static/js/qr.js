// DOM Elements
const qrContainer = document.getElementById('qrContainer');
const welcomeState = document.getElementById('welcomeState');
const qrState = document.getElementById('qrState');
const expiredState = document.getElementById('expiredState');
const successState = document.getElementById('successState');
const successIcon = document.getElementById('successIcon');
const qrCodeElement = document.getElementById('qrCode');
const timerText = document.getElementById('timerText');
const timerPath = document.getElementById('timerPath');
const amountDisplay = document.getElementById('amountDisplay');

// Variables
let qrCode = null;
let countdown = null;
let remainingTime = 0;
let totalTime = 0;

// Initialize Socket.IO connection
const socket = io();

// Listen for QR code updates
socket.on('set_qr', (data) => {
    const { qrData, duration, amount } = data;
    showQRCode(qrData, duration, amount);
});

socket.on('payment_success', () => {
    showSuccessState();
});

// Show QR code with countdown
function showQRCode(qrData, duration, amount) {
    // Update amount display
    amountDisplay.textContent = `₹${amount}`;
    // Clear any existing countdown
    if (countdown) {
        clearInterval(countdown);
    }
    
    // Update UI states
    welcomeState.classList.add('hidden');
    expiredState.classList.add('hidden');
    qrState.classList.remove('hidden');
    
    // Generate or update QR code
    qrCodeElement.innerHTML = "";

    const img = document.createElement("img");
    img.src = `data:image/png;base64,${qrData}`;  // if backend sends only raw base64
    img.alt = "QR Code";
    img.style.width = Math.min(window.innerWidth * 0.7, 350) + "px";
    img.style.height = "auto";
    qrCodeElement.appendChild(img);
    
    
    // Start countdown
    remainingTime = duration;
    totalTime = duration;
    updateTimerDisplay();
    
    countdown = setInterval(() => {
        remainingTime--;
        updateTimerDisplay();
        
        if (remainingTime <= 0) {
            clearInterval(countdown);
            showExpiredState();
        }
    }, 1000);
}

// Update timer display
function updateTimerDisplay() {
    timerText.textContent = remainingTime;
    
    // Calculate the stroke dash offset for the timer ring
    const circumference = 283; // 2 * π * r (r = 45)
    const offset = circumference - (remainingTime / totalTime) * circumference;
    timerPath.style.strokeDashoffset = offset;
    
    // Change color when time is running low
    if (remainingTime <= 10) {
        timerPath.style.stroke = '#ef4444';
        timerText.classList.remove('text-indigo-600');
        timerText.classList.add('text-red-500');
    } else {
        timerPath.style.stroke = '#4f46e5';
        timerText.classList.remove('text-red-500');
        timerText.classList.add('text-indigo-600');
    }
}

// Show expired state
function showExpiredState() {
    qrState.classList.add('hidden');
    expiredState.classList.remove('hidden');
}

// Reset to welcome state
function showSuccessState() {
    if (qrCodeElement.innerHTML === "") {
        return;
    }
    if (countdown) {
        clearInterval(countdown);
    }
    
    // Hide QR state and show success animation
    qrState.classList.add('hidden');
    successState.classList.remove('hidden');
    successIcon.classList.remove('scale-0');
    successIcon.classList.add('scale-100');
    
    // Auto reset after 5 seconds
    setTimeout(resetToWelcome, 5000);
}

function resetToWelcome() {
    if (countdown) {
        clearInterval(countdown);
    }
    
    expiredState.classList.add('hidden');
    qrState.classList.add('hidden');
    successState.classList.add('hidden');
    successIcon.classList.remove('scale-100');
    successIcon.classList.add('scale-0');
    welcomeState.classList.remove('hidden');
}

// Initial setup
document.addEventListener('DOMContentLoaded', () => {
    // Small animation for the welcome state
    setTimeout(() => {
        welcomeState.querySelector('svg').classList.add('transition-transform', 'duration-500');
        welcomeState.querySelector('svg').style.transform = 'rotate(90deg)';
    }, 1000);
});