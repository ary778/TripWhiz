document.addEventListener('DOMContentLoaded', function() {
    // Read the base path for images from the hidden div in the HTML
    const imagesPath = document.getElementById('static-data').dataset.imagesPath;

    // Build image URLs using the local static path for 100% reliability
    const sourceCities = [
        { name: 'Ahmedabad', iata: 'AMD', imageUrl: `${imagesPath}ahmedabad.jpg` },
        { name: 'Mumbai', iata: 'BOM', imageUrl: `${imagesPath}mumbai.jpg` },
        { name: 'Delhi', iata: 'DEL', imageUrl: `${imagesPath}delhi.jpg` }
    ];

    const sourceContainer = document.getElementById('source-container');

    function displaySourceCities() {
        if (!sourceContainer) return;
        sourceContainer.innerHTML = ''; 
        sourceCities.forEach(city => {
            // Clicking these cards will now search by the reliable IATA code
            const cityResultsUrl = `/results?source=${city.iata}`;
            const card = `
                <a href="${cityResultsUrl}" class="source-card">
                    <img src="${city.imageUrl}" alt="Image of ${city.name}">
                    <div class="card-content">
                        <h3>${city.name}</h3>
                    </div>
                </a>
            `;
            sourceContainer.insertAdjacentHTML('beforeend', card);
        });
    }

    displaySourceCities();
});