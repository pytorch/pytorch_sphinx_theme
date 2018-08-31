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

    $(window).on("scroll", function() {
      highlightNavigation.throttle(highlightNavigation.highlight, 100);
    });
  },

  throttle: function(fn, interval) {
    var lastCall, timeoutId;
    var now = new Date().getTime();

    if (lastCall && now < lastCall + interval) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(function() {
        lastCall = now;
        fn();
      }, interval - (now - lastCall));
    } else {
      lastCall = now;
      fn();
    }
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
