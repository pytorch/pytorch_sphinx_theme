var cookieBanner = {
  init: function() {
    cookieBanner.bind();

    var cookieExists = cookieBanner.cookieExists();

    if (!cookieExists) {
      cookieBanner.showCookieNotice();
    }
  },

  bind: function() {
    // Selector covers both the new <button class="close-button"> (accessible)
    // and the legacy <img class="close-button"> in case of cached templates.
    $(".close-button").on("click", function() {
      cookieBanner.hideCookieNotice();
      cookieBanner.setCookie(); // Set the cookie or local storage item when the banner is closed
    });
  },

  cookieExists: function() {
    return localStorage.getItem("returningPytorchUser") !== null;
  },

  setCookie: function() {
    localStorage.setItem("returningPytorchUser", true);
  },

  showCookieNotice: function() {
    $(".cookie-banner-wrapper").addClass("is-visible");
  },

  hideCookieNotice: function() {
    $(".cookie-banner-wrapper").removeClass("is-visible");
  }
};

$(function() {
  cookieBanner.init();
});
