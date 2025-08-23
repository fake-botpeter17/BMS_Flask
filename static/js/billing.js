// Sample database of items (in a real app, this would come from an API)
const itemDatabase = await fetch('/inventory/getItems');


// Current bill items
let billItems = [];
let billCounter = 1001;
let currentUser = "Admin";

// DOM Elements
const barcodeInput = document.getElementById('barcodeInput');
const scanBtn = document.getElementById('scanBtn');
const itemsTableBody = document.getElementById('itemsTableBody');
const totalAmount = document.getElementById('totalAmount');
const totalDiscount = document.getElementById('totalDiscount');
const netTotal = document.getElementById('netTotal');
const clearBillBtn = document.getElementById('clearBillBtn');
const printBillBtn = document.getElementById('printBillBtn');
const paymentModal = document.getElementById('paymentModal');
const closeModal = document.querySelector('.close');
const cashPaymentBtn = document.getElementById('cashPaymentBtn');
const upiPaymentBtn = document.getElementById('upiPaymentBtn');
const cashPaymentSection = document.getElementById('cashPaymentSection');
const upiPaymentSection = document.getElementById('upiPaymentSection');
const cashReceived = document.getElementById('cashReceived');
const balanceAmount = document.getElementById('balanceAmount');
const upiReceivedBtn = document.getElementById('upiReceivedBtn');
const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');
const cancelPaymentBtn = document.getElementById('cancelPaymentBtn');
const currentDate = document.getElementById('currentDate');
const currentTime = document.getElementById('currentTime');
const billNumber = document.getElementById('billNumber');
const logoutBtn = document.getElementById('logoutBtn');
const printSection = document.getElementById('printSection');

// Initialize the page
document.addEventListener('DOMContentLoaded', function () {
    updateDateTime();
    setInterval(updateDateTime, 1000);
    generateBillNumber();

    // Event listeners
    scanBtn.addEventListener('click', handleBarcodeScan);
    barcodeInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleBarcodeScan();
        }
    });

    clearBillBtn.addEventListener('click', clearBill);
    printBillBtn.addEventListener('click', openPaymentModal);
    closeModal.addEventListener('click', closePaymentModal);
    cashPaymentBtn.addEventListener('click', () => selectPaymentMode('cash'));
    upiPaymentBtn.addEventListener('click', () => selectPaymentMode('upi'));
    cashReceived.addEventListener('input', calculateBalance);
    upiReceivedBtn.addEventListener('click', confirmUPIPayment);
    confirmPaymentBtn.addEventListener('click', confirmAndPrint);
    cancelPaymentBtn.addEventListener('click', closePaymentModal);
    logoutBtn.addEventListener('click', logout);

    // Make sure the print button is disabled when there are no items
    updatePrintButtonState();
});

// Update current date and time
function updateDateTime() {
    const now = new Date();
    currentDate.textContent = now.toLocaleDateString();
    currentTime.textContent = now.toLocaleTimeString();
}

// Generate a new bill number
function generateBillNumber() {
    billNumber.textContent = `FP-${billCounter++}`;
}

// Handle barcode scanning
function handleBarcodeScan() {
    const barcode = barcodeInput.value.trim();
    if (!barcode) return;

    // Check if item exists in database
    if (itemDatabase[barcode]) {
        addItemToBill(barcode);
    } else {
        showToast('Item not found in database!', 'error');
    }

    barcodeInput.value = '';
    barcodeInput.focus();
}

// Add item to bill or increment quantity if already exists
function addItemToBill(barcode) {
    const item = itemDatabase[barcode];

    // Check if item already exists in bill
    const existingItemIndex = billItems.findIndex(i => i.barcode === barcode);

    if (existingItemIndex >= 0) {
        // Increment quantity
        billItems[existingItemIndex].quantity += 1;
        billItems[existingItemIndex].amount = calculateItemAmount(billItems[existingItemIndex]);
    } else {
        // Add new item
        const newItem = {
            barcode: barcode,
            name: item.name,
            rate: item.rate,
            quantity: 1,
            discountAmount: 0,
            discountPercent: item.discount,
            amount: item.rate * (1 - item.discount / 100)
        };
        billItems.push(newItem);
    }

    renderBillItems();
    updateTotals();
    updatePrintButtonState();
}

// Calculate item amount based on rate, quantity and discount
function calculateItemAmount(item) {
    // If discount amount is set, use that, otherwise use percentage
    if (item.discountAmount > 0) {
        const discountPerItem = item.discountAmount / item.quantity;
        return (item.rate - discountPerItem) * item.quantity;
    } else {
        return item.rate * item.quantity * (1 - item.discountPercent / 100);
    }
}

// Render bill items in the table
function renderBillItems() {
    itemsTableBody.innerHTML = '';

    billItems.forEach((item, index) => {
        const row = document.createElement('tr');
        row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';

        const discountAmount = item.discountAmount > 0 ?
            item.discountAmount :
            (item.rate * item.quantity * item.discountPercent / 100);

        row.innerHTML = `
            <td class="py-2 px-4">${index + 1}</td>
            <td class="py-2 px-4">${item.name}</td>
            <td class="py-2 px-4">₹${item.rate.toFixed(2)}</td>
            <td class="py-2 px-4">
                <input type="number" min="1" value="${item.quantity}" 
                       class="w-16 p-1 border rounded quantity-input" 
                       data-index="${index}">
            </td>
            <td class="py-2 px-4">
                <input type="number" min="0" max="${item.rate * item.quantity}" 
                       value="${discountAmount.toFixed(2)}" 
                       class="w-20 p-1 border rounded discount-amount-input" 
                       data-index="${index}">
            </td>
            <td class="py-2 px-4">
                <input type="number" min="0" max="100" value="${item.discountPercent}" 
                       class="w-16 p-1 border rounded discount-percent-input" 
                       data-index="${index}">
            </td>
            <td class="py-2 px-4">₹${item.amount.toFixed(2)}</td>
            <td class="py-2 px-4">
                <button class="text-red-500 hover:text-red-700 delete-item" data-index="${index}">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </td>
        `;

        itemsTableBody.appendChild(row);
    });

    // Add event listeners to dynamic inputs
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', handleQuantityChange);
    });

    document.querySelectorAll('.discount-amount-input').forEach(input => {
        input.addEventListener('change', handleDiscountAmountChange);
    });

    document.querySelectorAll('.discount-percent-input').forEach(input => {
        input.addEventListener('change', handleDiscountPercentChange);
    });

    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', handleDeleteItem);
    });
}

// Handle quantity change
function handleQuantityChange(e) {
    const index = e.target.dataset.index;
    const newQuantity = parseInt(e.target.value);

    if (newQuantity < 1) {
        e.target.value = 1;
        return;
    }

    billItems[index].quantity = newQuantity;

    // If discount was set as amount, keep the total discount same (per item discount changes)
    if (billItems[index].discountAmount > 0) {
        const discountPerItem = billItems[index].discountAmount / billItems[index].quantity;
        billItems[index].amount = (billItems[index].rate - discountPerItem) * newQuantity;
    } else {
        // If discount was percentage, recalculate amount
        billItems[index].amount = billItems[index].rate * newQuantity * (1 - billItems[index].discountPercent / 100);
    }

    renderBillItems();
    updateTotals();
}

// Handle discount amount change
function handleDiscountAmountChange(e) {
    const index = e.target.dataset.index;
    const discountAmount = parseFloat(e.target.value);
    const maxDiscount = billItems[index].rate * billItems[index].quantity;

    if (discountAmount < 0) {
        e.target.value = 0;
        billItems[index].discountAmount = 0;
    } else if (discountAmount > maxDiscount) {
        e.target.value = maxDiscount.toFixed(2);
        billItems[index].discountAmount = maxDiscount;
    } else {
        billItems[index].discountAmount = discountAmount;
    }

    // Calculate equivalent percentage
    billItems[index].discountPercent = (billItems[index].discountAmount / (billItems[index].rate * billItems[index].quantity)) * 100;

    // Calculate new amount
    const discountPerItem = billItems[index].discountAmount / billItems[index].quantity;
    billItems[index].amount = (billItems[index].rate - discountPerItem) * billItems[index].quantity;

    renderBillItems();
    updateTotals();
}

// Handle discount percentage change
function handleDiscountPercentChange(e) {
    const index = e.target.dataset.index;
    let discountPercent = parseFloat(e.target.value);

    if (discountPercent < 0) {
        e.target.value = 0;
        discountPercent = 0;
    } else if (discountPercent > 100) {
        e.target.value = 100;
        discountPercent = 100;
    }

    billItems[index].discountPercent = discountPercent;
    billItems[index].discountAmount = 0; // Reset discount amount when using percentage

    // Calculate new amount
    billItems[index].amount = billItems[index].rate * billItems[index].quantity * (1 - discountPercent / 100);

    renderBillItems();
    updateTotals();
}

// Handle item deletion
function handleDeleteItem(e) {
    const index = e.target.closest('button').dataset.index;
    billItems.splice(index, 1);
    renderBillItems();
    updateTotals();
    updatePrintButtonState();
}

// Update totals display
function updateTotals() {
    const total = billItems.reduce((sum, item) => sum + (item.rate * item.quantity), 0);
    const totalDiscountAmount = billItems.reduce((sum, item) => sum + (item.rate * item.quantity - item.amount), 0);
    const net = total - totalDiscountAmount;

    totalAmount.textContent = `₹${total.toFixed(2)}`;
    totalDiscount.textContent = `-₹${totalDiscountAmount.toFixed(2)}`;
    netTotal.textContent = `₹${net.toFixed(2)}`;
}

// Clear the current bill
function clearBill() {
    if (billItems.length === 0 || confirm('Are you sure you want to clear the current bill?')) {
        billItems = [];
        renderBillItems();
        updateTotals();
        generateBillNumber();
        updatePrintButtonState();
    }
}

// Update print button state based on items
function updatePrintButtonState() {
    printBillBtn.disabled = billItems.length === 0;
}

// Open payment modal
function openPaymentModal() {
    if (billItems.length === 0) return;

    // Reset payment modal
    cashPaymentSection.classList.add('hidden');
    upiPaymentSection.classList.add('hidden');
    cashReceived.value = '';
    balanceAmount.textContent = '₹0.00';

    // Set UPI amount
    const net = parseFloat(netTotal.textContent.replace('₹', ''));
    document.getElementById('upiAmount').textContent = netTotal.textContent;

    paymentModal.style.display = 'block';
}

// Close payment modal
function closePaymentModal() {
    paymentModal.style.display = 'none';
}

// Select payment mode
function selectPaymentMode(mode) {
    cashPaymentSection.classList.add('hidden');
    upiPaymentSection.classList.add('hidden');

    if (mode === 'cash') {
        cashPaymentSection.classList.remove('hidden');
        cashReceived.focus();
    } else if (mode === 'upi') {
        upiPaymentSection.classList.remove('hidden');
    }
}

// Calculate balance for cash payment
function calculateBalance() {
    const received = parseFloat(cashReceived.value) || 0;
    const net = parseFloat(netTotal.textContent.replace('₹', ''));
    const balance = received - net;

    balanceAmount.textContent = `₹${balance.toFixed(2)}`;
}

// Confirm UPI payment
function confirmUPIPayment() {
    showToast('UPI payment confirmed! Click "Confirm & Print" to complete the transaction.', 'success');
}

// Confirm and print the bill
function confirmAndPrint() {
    // Prepare print data
    preparePrintData();

    // Print the bill
    window.print();

    // In a real app, here you would send the ESCPOS commands to the printer
    // For this demo, we'll just log the print command
    console.log('Printing bill with ESCPOS commands...');

    // Reset for next bill
    setTimeout(() => {
        clearBill();
        closePaymentModal();
    }, 500);
}

// Prepare data for printing
function preparePrintData() {
    // Update print section with current data
    document.getElementById('printBillNo').textContent = billNumber.textContent;
    document.getElementById('printBilledBy').textContent = currentUser;

    const now = new Date();
    document.getElementById('printBillDate').textContent = now.toLocaleDateString('en-GB').replace(/\//g, '.');
    document.getElementById('printBillTime').textContent = now.toLocaleTimeString();

    // Add items to print
    const printItemsBody = document.getElementById('printItemsBody');
    printItemsBody.innerHTML = '';

    billItems.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="py-1">${index + 1}</td>
            <td class="py-1">${item.name}</td>
            <td class="py-1">₹${item.rate.toFixed(2)}</td>
            <td class="py-1">${item.quantity}</td>
            <td class="py-1">₹${item.amount.toFixed(2)}</td>
        `;
        printItemsBody.appendChild(row);
    });

    // Update totals
    document.getElementById('printTotal').textContent = totalAmount.textContent;
    document.getElementById('printDiscount').textContent = totalDiscount.textContent;
    document.getElementById('printNetTotal').textContent = netTotal.textContent;
}

// Show toast notification
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.getElementById('toastContainer').appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

// Logout function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // In a real app, this would redirect to login page
        showToast('Logged out successfully!', 'success');
    }
}

// Close modal if clicked outside
window.addEventListener('click', function (event) {
    if (event.target === paymentModal) {
        closePaymentModal();
    }
});
