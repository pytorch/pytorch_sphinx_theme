function getWebappJSPathFromHtml(webappPage) {
  // For production environment
  var webappJSPath = (/"(\/static\/js\/main\.[\da-z]+\.js)"/.exec(webappPage) || [])[1];
  if (webappJSPath) {
    return webappJSPath;
  }
  // For local environment
  return (/"(\/static\/js\/bundle\.js)"/.exec(webappPage) || [])[1];
}

(function() {
  // Using the user's homepage because this way it won't break
  // if we replace the homepage with webflow or WP
  fetch("/injectwebapp")
    // the sphinx JS bundler isn't configured to handle async function
    .then(function(response) { return response.text() })
    .then(function(webappPage) {
      var webappJSPath = getWebappJSPathFromHtml(webappPage);

      if (!webappJSPath) {
        console.error("cannot load webapp bundle");
        // TODO: fallback to the WP header and footer
        return;
      }

      var script = document.createElement("script");
      script.src = webappJSPath;
      script.defer = true;
      document.head.appendChild(script);
    });
})();
