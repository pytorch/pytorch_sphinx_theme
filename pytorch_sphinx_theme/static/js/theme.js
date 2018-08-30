require=(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
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

},{}],2:[function(require,module,exports){
window.mobileMenu = {
  bind: function() {
    $("[data-behavior='open-mobile-menu']").on('click', function(e) {
      e.preventDefault();
      $(".mobile-main-menu").addClass("open");
      $("body").addClass('no-scroll');

      mobileMenu.listenForResize();
    });

    $("[data-behavior='close-mobile-menu']").on('click', function(e) {
      e.preventDefault();
      mobileMenu.close();
    });
  },

  listenForResize: function() {
    $(window).on('resize.ForMobileMenu', function() {
      if ($(this).width() > 768) {
        mobileMenu.close();
      }
    });
  },

  close: function() {
    $(".mobile-main-menu").removeClass("open");
    $("body").removeClass('no-scroll');
    $(window).off('resize.ForMobileMenu');
  }
};

$(window).on('resize', function(e) {
  handleLeftMenu();
  handleRightMenu();
});

$(window).on('scroll', function(e) {
  handleLeftMenu();
  handleRightMenu();
});

$(window).on('load', function() {
  handleLeftMenu();
  handleRightMenu();
});

function handleLeftMenu() {
  var windowHeight = $(window).height();
  var topOfFooterRelativeToWindow = document.getElementsByClassName("docs-tutorials-resources")[0].getBoundingClientRect().top;

  if (topOfFooterRelativeToWindow >= windowHeight) {
    $(".pytorch-left-menu").css({height: "100%"});
    // $(".pytorch-right-menu").removeClass("fixed-to-bottom");
  } else {
    var howManyPixelsOfTheFooterAreInTheWindow = windowHeight - topOfFooterRelativeToWindow
    var headerHeight = $('.header-holder').height();
    var leftMenuDifference = howManyPixelsOfTheFooterAreInTheWindow + headerHeight;

    $(".pytorch-left-menu").css({height: windowHeight - leftMenuDifference});
  }
}

function handleRightMenu() {
  // if (topOfFooterRelativeToWindow >= windowHeight) {
  // if the bottom of the right menu is <= 20px from the top of the footer
  var windowHeight = $(window).height();
  var topOfFooterRelativeToWindow = document.getElementsByClassName("docs-tutorials-resources")[0].getBoundingClientRect().top;

  var bottom = $(".pytorch-right-menu ul:first").offset().top + $(".pytorch-right-menu ul:first").height();
  var footerTop = $(".docs-tutorials-resources").offset().top;

  if (topOfFooterRelativeToWindow >= windowHeight) {
    $(".pytorch-right-menu").removeClass("fixed-to-bottom");
  } else if (bottom >= -40 + footerTop) {
    $(".pytorch-right-menu").addClass("fixed-to-bottom");
  }
}

},{}],3:[function(require,module,exports){
window.mobileTOC = {
  bind: function() {
    $("[data-behavior='open-table-of-contents']").on("click", function(e) {
      e.preventDefault();
      $("body").addClass("no-scroll");
      $(".pytorch-left-menu").addClass("open-mobile");

      mobileTOC.listenForResize();
    });

    $("[data-behavior='close-table-of-contents']").on("click", function(e) {
      e.preventDefault();
      mobileTOC.close();
    });
  },

  listenForResize: function() {
    $(window).on('resize.ForMobileTOC', function() {
      if ($(this).width() > 768) {
        mobileTOC.close();
      }
    });
  },

  close: function() {
    $(".pytorch-left-menu").removeClass("open-mobile");
    $("body").removeClass('no-scroll');
    $(window).off('resize.ForMobileTOC');
  }
}

},{}],4:[function(require,module,exports){
window.pytorchAnchors = {
  bind: function() {
    // Replace Sphinx-generated anchors with anchorjs ones
    $(".headerlink").text("");

    window.anchors.add(".pytorch-article .headerlink");

    $(".anchorjs-link").each(function() {
      var $headerLink = $(this).closest(".headerlink");
      var href = $headerLink.attr("href");
      var clone = this.outerHTML;

      $clone = $(clone).attr("href", href);
      $headerLink.before($clone);
      $headerLink.remove();
    });
  }
};

},{}],5:[function(require,module,exports){
// Modified from https://stackoverflow.com/a/13067009
// Going for a JS solution to scrolling to an anchor so we can benefit from
// less hacky css and smooth scrolling.

window.scrollToAnchor = {
  bind: function() {
    var document = window.document;
    var history = window.history;
    var location = window.location
    var HISTORY_SUPPORT = !!(history && history.pushState);

    var anchorScrolls = {
      ANCHOR_REGEX: /^#[^ ]+$/,
      offsetHeightPx: function() {
        return $(".header-holder").height() + 20;
      },

      /**
       * Establish events, and fix initial scroll position if a hash is provided.
       */
      init: function() {
        this.scrollToCurrent();
        $(window).on('hashchange', $.proxy(this, 'scrollToCurrent'));
        $('body').on('click', 'a', $.proxy(this, 'delegateAnchors'));
      },

      /**
       * Return the offset amount to deduct from the normal scroll position.
       * Modify as appropriate to allow for dynamic calculations
       */
      getFixedOffset: function() {
        return this.offsetHeightPx();
      },

      /**
       * If the provided href is an anchor which resolves to an element on the
       * page, scroll to it.
       * @param  {String} href
       * @return {Boolean} - Was the href an anchor.
       */
      scrollIfAnchor: function(href, pushToHistory) {
        var match, anchorOffset;

        if(!this.ANCHOR_REGEX.test(href)) {
          return false;
        }

        match = document.getElementById(href.slice(1));

        if(match) {
          anchorOffset = $(match).offset().top - this.getFixedOffset();
          $('html, body').scrollTop(anchorOffset);

          // Add the state to history as-per normal anchor links
          if(HISTORY_SUPPORT && pushToHistory) {
            history.pushState({}, document.title, location.pathname + href);
          }
        }

        return !!match;
      },

      /**
       * Attempt to scroll to the current location's hash.
       */
      scrollToCurrent: function(e) {
        if(this.scrollIfAnchor(window.location.hash) && e) {
          e.preventDefault();
        }
      },

      /**
       * If the click event's target was an anchor, fix the scroll position.
       */
      delegateAnchors: function(e) {
        var elem = e.target;

        if(this.scrollIfAnchor(elem.getAttribute('href'), true)) {
          e.preventDefault();
        }
      }
    };

    $(document).ready($.proxy(anchorScrolls, 'init'));
  }
};

},{}],"pytorch-sphinx-theme":[function(require,module,exports){
var jQuery = (typeof(window) != 'undefined') ? window.jQuery : require('jquery');

// Sphinx theme nav state
function ThemeNav () {

    var nav = {
        navBar: null,
        win: null,
        winScroll: false,
        winResize: false,
        linkScroll: false,
        winPosition: 0,
        winHeight: null,
        docHeight: null,
        isRunning: false
    };

    nav.enable = function (withStickyNav) {
        var self = this;

        // TODO this can likely be removed once the theme javascript is broken
        // out from the RTD assets. This just ensures old projects that are
        // calling `enable()` get the sticky menu on by default. All other cals
        // to `enable` should include an argument for enabling the sticky menu.
        if (typeof(withStickyNav) == 'undefined') {
            withStickyNav = true;
        }

        if (self.isRunning) {
            // Only allow enabling nav logic once
            return;
        }

        self.isRunning = true;
        jQuery(function ($) {
            self.init($);

            self.reset();
            self.win.on('hashchange', self.reset);

            if (withStickyNav) {
                // Set scroll monitor
                self.win.on('scroll', function () {
                    if (!self.linkScroll) {
                        if (!self.winScroll) {
                            self.winScroll = true;
                            requestAnimationFrame(function() { self.onScroll(); });
                        }
                    }
                });
            }

            // Set resize monitor
            self.win.on('resize', function () {
                if (!self.winResize) {
                    self.winResize = true;
                    requestAnimationFrame(function() { self.onResize(); });
                }
            });

            self.onResize();
        });

    };

    // TODO remove this with a split in theme and Read the Docs JS logic as
    // well, it's only here to support 0.3.0 installs of our theme.
    nav.enableSticky = function() {
        this.enable(true);
    };

    nav.init = function ($) {
        var doc = $(document),
            self = this;

        this.navBar = $('div.pytorch-side-scroll:first');
        this.win = $(window);

        // Set up javascript UX bits
        $(document)
            // Shift nav in mobile when clicking the menu.
            .on('click', "[data-toggle='pytorch-left-menu-nav-top']", function() {
                $("[data-toggle='wy-nav-shift']").toggleClass("shift");
                $("[data-toggle='rst-versions']").toggleClass("shift");
            })

            // Nav menu link click operations
            .on('click', ".pytorch-menu-vertical .current ul li a", function() {
                var target = $(this);
                // Close menu when you click a link.
                $("[data-toggle='wy-nav-shift']").removeClass("shift");
                $("[data-toggle='rst-versions']").toggleClass("shift");
                // Handle dynamic display of l3 and l4 nav lists
                self.toggleCurrent(target);
                self.hashChange();
            })
            .on('click', "[data-toggle='rst-current-version']", function() {
                $("[data-toggle='rst-versions']").toggleClass("shift-up");
            })

        // Make tables responsive
        $("table.docutils:not(.field-list,.footnote,.citation)")
            .wrap("<div class='wy-table-responsive'></div>");

        // Add extra class to responsive tables that contain
        // footnotes or citations so that we can target them for styling
        $("table.docutils.footnote")
            .wrap("<div class='wy-table-responsive footnote'></div>");
        $("table.docutils.citation")
            .wrap("<div class='wy-table-responsive citation'></div>");

        // Add expand links to all parents of nested ul
        $('.pytorch-menu-vertical ul').not('.simple').siblings('a').each(function () {
            var link = $(this);
                expand = $('<span class="toctree-expand"></span>');
            expand.on('click', function (ev) {
                self.toggleCurrent(link);
                ev.stopPropagation();
                return false;
            });
            link.prepend(expand);
        });
    };

    nav.reset = function () {
        // Get anchor from URL and open up nested nav
        var anchor = encodeURI(window.location.hash) || '#';

        try {
            var vmenu = $('.pytorch-menu-vertical');
            var link = vmenu.find('[href="' + anchor + '"]');
            if (link.length === 0) {
                // this link was not found in the sidebar.
                // Find associated id element, then its closest section
                // in the document and try with that one.
                var id_elt = $('.document [id="' + anchor.substring(1) + '"]');
                var closest_section = id_elt.closest('div.section');
                link = vmenu.find('[href="#' + closest_section.attr("id") + '"]');
                if (link.length === 0) {
                    // still not found in the sidebar. fall back to main section
                    link = vmenu.find('[href="#"]');
                }
            }
            // If we found a matching link then reset current and re-apply
            // otherwise retain the existing match
            if (link.length > 0) {
                $('.pytorch-menu-vertical .current').removeClass('current');
                link.addClass('current');
                link.closest('li.toctree-l1').addClass('current');
                link.closest('li.toctree-l1').parent().addClass('current');
                link.closest('li.toctree-l1').addClass('current');
                link.closest('li.toctree-l2').addClass('current');
                link.closest('li.toctree-l3').addClass('current');
                link.closest('li.toctree-l4').addClass('current');
            }
        }
        catch (err) {
            console.log("Error expanding nav for anchor", err);
        }

    };

    nav.onScroll = function () {
        this.winScroll = false;
        var newWinPosition = this.win.scrollTop(),
            winBottom = newWinPosition + this.winHeight,
            navPosition = this.navBar.scrollTop(),
            newNavPosition = navPosition + (newWinPosition - this.winPosition);
        if (newWinPosition < 0 || winBottom > this.docHeight) {
            return;
        }
        this.navBar.scrollTop(newNavPosition);
        this.winPosition = newWinPosition;
    };

    nav.onResize = function () {
        this.winResize = false;
        this.winHeight = this.win.height();
        this.docHeight = $(document).height();
    };

    nav.hashChange = function () {
        this.linkScroll = true;
        this.win.one('hashchange', function () {
            this.linkScroll = false;
        });
    };

    nav.toggleCurrent = function (elem) {
        var parent_li = elem.closest('li');
        parent_li.siblings('li.current').removeClass('current');
        parent_li.siblings().find('li.current').removeClass('current');
        parent_li.find('> ul li.current').removeClass('current');
        parent_li.toggleClass('current');
    }

    return nav;
};

module.exports.ThemeNav = ThemeNav();

if (typeof(window) != 'undefined') {
    window.SphinxRtdTheme = {
        Navigation: module.exports.ThemeNav,
        // TODO remove this once static assets are split up between the theme
        // and Read the Docs. For now, this patches 0.3.0 to be backwards
        // compatible with a pre-0.3.0 layout.html
        StickyNav: module.exports.ThemeNav,
    };
}


// requestAnimationFrame polyfill by Erik Möller. fixes from Paul Irish and Tino Zijdel
// https://gist.github.com/paulirish/1579671
// MIT license

(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

$(".sphx-glr-thumbcontainer").removeAttr("tooltip");

},{"jquery":"jquery"}]},{},[1,2,3,4,5,"pytorch-sphinx-theme"]);
