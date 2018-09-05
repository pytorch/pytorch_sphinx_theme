// Modified from https://stackoverflow.com/a/27078401
window.pyTorchThrottle = function(func, wait, options) {
  var context, args, result;
  var timeout = null;
  var previous = 0;
  if (!options) options = {};
  var later = function() {
    previous = options.leading === false ? 0 : Date.now();
    timeout = null;
    result = func.apply(context, args);
    if (!timeout) context = args = null;
  };
  return function() {
    var now = Date.now();
    if (!previous && options.leading === false) previous = now;
    var remaining = wait - (now - previous);
    context = this;
    args = arguments;
    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = now;
      result = func.apply(context, args);
      if (!timeout) context = args = null;
    } else if (!timeout && options.trailing !== false) {
      timeout = setTimeout(later, remaining);
    }
    return result;
  };
};

// Modified from https://stackoverflow.com/a/32396543
window.highlightNavigation = {
  navigationListItems: $(".pytorch-right-menu li"),
  sections: $(
    $(".pytorch-article .section")
      .get()
      .reverse()
  ),
  sectionIdTonavigationLink: {},

  bind: function() {
    // Don't show the "Shortcuts" text unless there are menu items
    if (highlightNavigation.navigationListItems.length > 1) {
      $(".pytorch-shortcuts-wrapper").show();
    }

    highlightNavigation.sections.each(function() {
      var id = $(this).attr("id");
      highlightNavigation.sectionIdTonavigationLink[id] = $(
        ".pytorch-right-menu li a[href='#" + id + "']"
      );
    });

    $(window).scroll(pyTorchThrottle(highlightNavigation.highlight, 500));
  },

  highlight: function() {
    var scrollPosition = $(window).scrollTop();
    var offset = $(".header-holder").height() + $(".pytorch-page-level-bar").height() + 25;

    highlightNavigation.sections.each(function() {
      var currentSection = $(this);
      var sectionTop = currentSection.offset().top;

      if (scrollPosition >= sectionTop - offset) {
        var id = currentSection.attr("id");
        var $navigationLink = highlightNavigation.sectionIdTonavigationLink[id];
        var $navigationListItem = $navigationLink.closest("li");

        if (!$navigationListItem.hasClass("active")) {
          highlightNavigation.navigationListItems.removeClass("active");
          $(".pytorch-right-menu-active-dot").remove();

          if ($navigationLink.is(":visible")) {
            $navigationListItem.addClass("active");
            $navigationListItem.prepend("<div class=\"pytorch-right-menu-active-dot\"></div>");
          }
        }

        return false;
      }
    });
  }
};
