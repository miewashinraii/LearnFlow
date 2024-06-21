function login() {
  const usernameOrEmail = document.getElementById('username-email').value;
  const password = document.getElementById('password').value;

  // Send the login data to the server-side script using AJAX or Fetch API
  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ usernameOrEmail, password })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        // Redirect the user to the dashboard or homepage
        window.location.href = '/Ulearndash.html';
      } else {
        // Display an error message
        alert(data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    });
  }
  
  function signInWithUTPID() {
    // Implement sign-in with UTP ID functionality
    console.log('Attempting to sign in with UTP ID');
  }
  
  function accessAsGuest() {
    // Implement guest access functionality
    console.log('Accessing as a guest');
  }
  
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