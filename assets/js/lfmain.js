// // Get the current page URL
// var currentURL = window.location.href;

// // Get all the navigation links
// var navLinks = document.querySelectorAll('nav ul li a');

// // Loop through the navigation links and add the 'active-link' class to the appropriate one
// navLinks.forEach(function(link) {
//   if (link.href === currentURL) {
//     link.classList.add('active-link');
//   } else {
//     link.classList.remove('active-link');
//   }
// });

// // Get the main content element
// const mainContent = document.querySelector('.main-content');

// // Get all the navbar items
// const navbarItems = document.querySelectorAll('.navbar-item');

// // Get all the items
// const dashboard = document.getElementById("dashboard");
// const aiTutor = document.getElementById("ai-tutor");
// const studyPlans = document.getElementById("study-plans");
// const practiceGen = document.getElementById("practice-generator");
// const statistics = document.getElementById("statistics");
// const settings = document.getElementById("settings") 
// const logOut = document.getElementById("log-out")

// // Define the content for each button
// const content = {
//   dashboard: '<h2>Dashboard Content</h2><p>This is the dashboard content.</p>',
//   aiTutor: '<h2>AI Tutor Content</h2><p>This is the AI Tutor content.</p>',
//   studyPlans: '<h2>Study Plans Content</h2><p>This is the Study Plans content.</p>',
//   practiceGenerator: '<h2>Practice Problem Generator Content</h2><p>This is the Practice Problem Generator content.</p>',
//   statistics: '<h2>Statistics Content</h2><p>This is the Statistics content.</p>',
//   settings: '<h2>Settings Content</h2><p>This is the Settings content.</p>',
//   logOut: '<h2>Log Out Content</h2><p>This is the Log Out content.</p>'
// };

// // Add event listeners to the navbar items
// navbarItems.forEach(item => {
//   item.addEventListener('click', () => {
//     const target = item.dataset.target;
//     mainContent.innerHTML = content[target];
//   });
// });

// Get all the navigation links
const navLinks = document.querySelectorAll('navbar-item');
const learnFlowContent = document.getElementById('main-content');

// Add click event listeners to the navigation links
navLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    const linkId = event.target.id;

    // Update the LearnFlow content and title based on the clicked link
    updateLearnFlowContent(linkId);
  });
});

function updateLearnFlowContent(linkId) {
  // Clear the previous content
  learnFlowContent.innerHTML = '';

  // Update the LearnFlow title
  learnFlowTitle.textContent = capitalizeFirstLetter(linkId.replace('-', ' '));

  // Dynamically generate the content based on the selected link
  switch (linkId) {
    case 'dashboard':
      // Add content for the Dashboard
      learnFlowContent.innerHTML = '<p>This is the Dashboard content.</p>';
      break;
    case 'ai-tutor':
      // Add content for the AI Tutor
      learnFlowContent.innerHTML = '<p>This is the AI Tutor content.</p>';
      break;
    // Add more cases for the other navigation links
    default:
      learnFlowContent.innerHTML = '<p>No content available for the selected item.</p>';
  }
}

function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}