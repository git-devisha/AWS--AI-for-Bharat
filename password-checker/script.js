// Get DOM elements
const billAmountInput = document.getElementById('billAmount');
const tipPercentInput = document.getElementById('tipPercent');
const numPeopleInput = document.getElementById('numPeople');
const tipButtons = document.querySelectorAll('.tip-btn');
const decreaseBtn = document.getElementById('decreasePeople');
const increaseBtn = document.getElementById('increasePeople');

const tipAmountDisplay = document.getElementById('tipAmount');
const totalBillDisplay = document.getElementById('totalBill');
const perPersonDisplay = document.getElementById('perPerson');

// Default tip percentage
let currentTip = 18;

// Initialize
updateCalculations();

// Event listeners
billAmountInput.addEventListener('input', updateCalculations);
tipPercentInput.addEventListener('input', handleCustomTip);
numPeopleInput.addEventListener('input', updateCalculations);

tipButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        tipButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTip = parseInt(btn.dataset.tip);
        tipPercentInput.value = '';
        updateCalculations();
    });
});

decreaseBtn.addEventListener('click', () => {
    const current = parseInt(numPeopleInput.value) || 1;
    if (current > 1) {
        numPeopleInput.value = current - 1;
        updateCalculations();
    }
});

increaseBtn.addEventListener('click', () => {
    const current = parseInt(numPeopleInput.value) || 1;
    if (current < 50) {
        numPeopleInput.value = current + 1;
        updateCalculations();
    }
});

function handleCustomTip() {
    const customTip = parseFloat(tipPercentInput.value);
    if (!isNaN(customTip) && customTip >= 0) {
        tipButtons.forEach(b => b.classList.remove('active'));
        currentTip = customTip;
        updateCalculations();
    }
}

function updateCalculations() {
    const billAmount = parseFloat(billAmountInput.value) || 0;
    const numPeople = parseInt(numPeopleInput.value) || 1;
    
    // Get active tip
    const activeTip = tipPercentInput.value ? parseFloat(tipPercentInput.value) : currentTip;
    
    // Calculate
    const tipAmount = billAmount * (activeTip / 100);
    const totalBill = billAmount + tipAmount;
    const perPerson = totalBill / numPeople;
    
    // Update display
    tipAmountDisplay.textContent = formatCurrency(tipAmount);
    totalBillDisplay.textContent = formatCurrency(totalBill);
    perPersonDisplay.textContent = formatCurrency(perPerson);
}

function formatCurrency(amount) {
    return '$' + amount.toFixed(2);
}

// Prevent invalid input
numPeopleInput.addEventListener('blur', () => {
    const value = parseInt(numPeopleInput.value);
    if (isNaN(value) || value < 1) {
        numPeopleInput.value = 1;
        updateCalculations();
    }
});
