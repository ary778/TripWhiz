document.addEventListener('DOMContentLoaded', function() {
    const resultsContainer = document.getElementById('results-container');
    const resultsTitle = document.getElementById('results-title');
    const resultsSubtitle = document.getElementById('results-subtitle');
    const loader = document.getElementById('loader');
    
    // Read all parameters from the URL, including the new category
    const urlParams = new URLSearchParams(window.location.search);
    const sourceCity = urlParams.get('source');
    const maxBudget = urlParams.get('budget');
    const category = urlParams.get('category'); // NEW: Get category from URL
    const apiUrl = '/api/deals/';

    if (sourceCity) {
        resultsTitle.textContent = `Trips from ${sourceCity}`;
        loader.style.display = 'block';
        
        // Build the final API URL with all parameters
        let fetchUrl = `${apiUrl}?source=${sourceCity}&budget=${maxBudget}`;
        if (category) { // Add category to the URL if it was selected
            fetchUrl += `&category=${category}`;
        }

        fetch(fetchUrl)
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error fetching API data:', error);
                resultsSubtitle.textContent = 'Sorry, we could not load trip data.';
                loader.style.display = 'none';
            });
    }

    // REMOVED: All the frontend filter button logic is gone

    // This function simply displays the results from the API
    function displayResults(trips) {
        loader.style.display = 'none';
        resultsContainer.innerHTML = '';

        if (trips.length === 0) {
            resultsContainer.innerHTML = `<p class="section-subtitle">Sorry, no trips found for your criteria.</p>`;
            return;
        }

        resultsSubtitle.textContent = `Here are the top ${trips.length} destinations we found for you!`;

        trips.forEach(trip => {
            const cityName = trip.destination.name;
            const totalPrice = trip.total_price;
            const imageUrl = trip.imageUrl;

            const card = `
                <div class="result-card">
                    <img src="${imageUrl}" alt="Image of ${cityName}">
                    <div class="card-content">
                        <h3>${cityName}</h3>
                        <p class="price">₹${totalPrice.toLocaleString('en-IN')}</p>
                    </div>
                </div>
            `;
            resultsContainer.insertAdjacentHTML('beforeend', card);
        });
    }
});