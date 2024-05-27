// Get the timeout message container
const timeoutMessage = document.getElementById('timeout-message');

// Track the time since the page was loaded
let startTime = new Date().getTime();

// Check the time every second
setInterval(() => {
  const elapsedTime = new Date().getTime() - startTime;
  const twoMinutes = 2 * 60 * 1000; // 2 minutes in milliseconds

  if (elapsedTime >= twoMinutes) {
    timeoutMessage.textContent = 'Your session has timed out. Please log in again.';
    timeoutMessage.classList.remove('hidden');
  }
}, 1000);