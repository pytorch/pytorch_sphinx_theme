document.addEventListener('DOMContentLoaded', function() {
  // Function to clean up search results
  function cleanSearchResults() {
    const searchResults = document.querySelectorAll('.search li p.context');
    if (searchResults.length > 0) {
      searchResults.forEach(function(result) {
        // More robust pattern matching for "Rate this Page" and stars
        const ratePageIndex = result.innerHTML.indexOf('Rate this Page');
        const starIndex = result.innerHTML.indexOf('★');

        // Use whichever comes first
        const cutIndex = Math.min(
          ratePageIndex !== -1 ? ratePageIndex : Infinity,
          starIndex !== -1 ? starIndex : Infinity
        );

        if (cutIndex !== Infinity) {
          result.innerHTML = result.innerHTML.substring(0, cutIndex);
        }
      });
    }
  }

  // Run on page load if we're on the search page
  if (window.location.pathname.includes('/search.html')) {
    cleanSearchResults();
  }

  // Set up a mutation observer to watch for search results being added to the DOM
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes.length && document.querySelector('.search li p.context')) {
        cleanSearchResults();
      }
    });
  });

  // Start observing the document body for changes
  observer.observe(document.body, { childList: true, subtree: true });
});
