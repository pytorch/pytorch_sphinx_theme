(function() {
    if (window.starRatingInitialized) return;
    window.starRatingInitialized = true;

    let lastRating = 0;
    let debounceTimer;
    let isProcessing = false;
    const pageTitle = document.querySelector('h1')?.textContent || document.title;

    document.addEventListener('click', function(e) {
        if (!e.target.matches('.star[data-behavior="tutorial-rating"]') || isProcessing) return;

        const value = parseInt(e.target.dataset.count || e.target.dataset.value);
        const allStars = document.querySelectorAll('.star');

        allStars.forEach(s => {
            s.classList.toggle('active', parseInt(s.dataset.count || s.dataset.value) <= value);
        });

        isProcessing = true;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (value !== lastRating) {
                console.log(`Sending rating for ${pageTitle} after 2.5s: ${value} (previous: ${lastRating})`);
                // Push to dataLayer for GTM
                if (window.dataLayer) {
                    window.dataLayer.push({
                        'event': 'star_rating',
                        'Rating': value,
                        'page_title': pageTitle
                    });
                }

                // Direct GA4 event
                if (typeof gtag == 'function') {
                    gtag('event', 'star_rating', {
                        'Rating': value,
                        'page_title': pageTitle
                    });
                }

                lastRating = value;
            }
            isProcessing = false;
        }, 1500);
    });
})();
