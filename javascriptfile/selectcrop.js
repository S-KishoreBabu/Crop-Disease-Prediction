
const clickableBoxes = document.querySelectorAll('.crop-box');

// Function to handle the click event
function handleBoxClick() {
    // The relative path to the other HTML file in the same directory
    const url = 'scanner.html';
    
    // Redirect to the new HTML file
    window.location.href = url;
}

// Add a click event listener to each div box
clickableBoxes.forEach(box => {
    box.addEventListener('click', handleBoxClick);
});