// Replace this with your monitoring app's domain
const MONITOR_APP_URL = 'https://overview-u84a.onrender.com/';

function recordPageVisit() {
    // Get the current page URL
    const currentPage = encodeURIComponent(window.location.href);
    
    // Create the tracking URL
    const trackingUrl = `${MONITOR_APP_URL}/record_visit?page=${currentPage}`;
    
    // Send the tracking request
    fetch(trackingUrl)
        .then(response => response.json())
        .catch(error => console.error('Tracking error:', error));
}

// Record the visit when the page loads
window.addEventListener('load', recordPageVisit);
