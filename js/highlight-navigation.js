// Modified from https://stackoverflow.com/a/32396543

window.highlightNavigation = {
  navigationLinks: $(".pytorch-right-menu li a"),
  sections: $(
    $(".pytorch-article .section")
      .get()
      .reverse()
  ),
  sectionIdTonavigationLink: {},

  bind: function() {
    // Sphinx automatically tags the first menu item with just a "#" href, which brings
    // you to the top of the page. We want to instead give this an href of the first content
    // section so that it highlights like every other menu item.
    var $firstNavItem = $(".pytorch-right-menu li a:first");

    if ($firstNavItem.attr("href") === "#") {
      var firstSectionId = $(".pytorch-article .section")
        .first()
        .attr("id");
      $firstNavItem.attr("href", "#" + firstSectionId);
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
    var offset = $(".header-holder").height() + 25;

    highlightNavigation.sections.each(function() {
      var currentSection = $(this);
      var sectionTop = currentSection.offset().top;

      if (scrollPosition >= sectionTop - offset) {
        var id = currentSection.attr("id");
        var $navigationLink = highlightNavigation.sectionIdTonavigationLink[id];

        if (!$navigationLink.hasClass("active")) {
          highlightNavigation.navigationLinks.removeClass("active");
          $navigationLink.addClass("active");
        }

        return false;
      }
    });
  }
};
