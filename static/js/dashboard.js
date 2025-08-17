document.addEventListener('DOMContentLoaded', () => {
  loadStats();
  loadRecentTransactions(10);
  // Optional: bind logout explicitly
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      alert('Logging out...');
      // window.location.href = '/login';
    });
  }
});

// Helpers
function formatINR(n) {
  if (typeof n !== 'number') n = Number(n) || 0;
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(n);
}
function escapeHTML(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error('Failed to fetch stats');
    const data = await res.json();
    // Update DOM
    if (document.getElementById('sales-today')) {
      document.getElementById('sales-today').textContent = formatINR(data.salesToday);
    }
    if (document.getElementById('new-customers')) {
      document.getElementById('new-customers').textContent = data.newCustomers;
    }
    if (document.getElementById('inventory-count')) {
      document.getElementById('inventory-count').textContent = data.inventoryCount + ' Items';
    }
  } catch (e) {
    console.error(e);
  }
}

async function loadRecentTransactions(limit = 10) {
  try {
    const res = await fetch('/api/transactions?limit=' + limit);
    if (!res.ok) throw new Error('Failed to fetch transactions');
    const data = await res.json();
    const tbody = document.getElementById('transactions-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    for (const t of data.transactions) {
      tbody.appendChild(createTransactionRow(t));
    }
  } catch (e) {
    console.error(e);
  }
}

function createTransactionRow(t) {
  // t = { invoice, customer, date, time, amount, status }
  const tr = document.createElement('tr');
  const dateStr = t.date ? new Date(t.date).toLocaleDateString() : '';
  const timeStr = t.time ?? '';
  const amountStr = formatINR(t.amount ?? 0);

  tr.innerHTML = `
    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${escapeHTML(t.invoice)}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${escapeHTML(t.customer)}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${dateStr} ${timeStr}</td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${amountStr}</td>
    <td class="px-6 py-4 whitespace-nowrap">
      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        t.status === 'Paid' ? 'bg-green-100 text-green-800' :
        t.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
        'bg-gray-100 text-gray-800'
      }">${escapeHTML(t.status)}</span>
    </td>
  `;
  return tr;
}