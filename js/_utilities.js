window.utilities = {
  scrollTop: function() {
    var supportPageOffset = window.pageXOffset !== undefined;
    var isCSS1Compat = ((document.compatMode || "") === "CSS1Compat");
    var scrollLeft = supportPageOffset ? window.pageXOffset : isCSS1Compat ? document.documentElement.scrollLeft : document.body.scrollLeft;
    return supportPageOffset ? window.pageYOffset : isCSS1Compat ? document.documentElement.scrollTop : document.body.scrollTop;
  },

  // Modified from https://stackoverflow.com/a/27078401
  throttle: function(func, wait, options) {
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
  },

  closest: function (el, selector) {
    var matchesFn;

    // find vendor prefix
    ['matches','webkitMatchesSelector','mozMatchesSelector','msMatchesSelector','oMatchesSelector'].some(function(fn) {
      if (typeof document.body[fn] == 'function') {
        matchesFn = fn;
        return true;
      }
      return false;
    });

    var parent;

    // traverse parents
    while (el) {
      parent = el.parentElement;
      if (parent && parent[matchesFn](selector)) {
        return parent;
      }
      el = parent;
    }

    return null;
  },

  // Modified from https://stackoverflow.com/a/18953277
  offset: function(elem) {
    if (!elem) {
      return;
    }

    rect = elem.getBoundingClientRect();

    // Make sure element is not hidden (display: none) or disconnected
    if (rect.width || rect.height || elem.getClientRects().length) {
      var doc = elem.ownerDocument;
      var docElem = doc.documentElement;

      return {
        top: rect.top + window.pageYOffset - docElem.clientTop,
        left: rect.left + window.pageXOffset - docElem.clientLeft
      };
    }
  },

  headersHeight: function() {
    if (document.getElementById("pytorch-left-menu").classList.contains("make-fixed")) {
      return document.getElementById("pytorch-page-level-bar").offsetHeight;
    } else {
      return document.getElementById("header-holder").offsetHeight +
             document.getElementById("pytorch-page-level-bar").offsetHeight;
    }
  },

  windowHeight: function() {
    return window.innerHeight ||
           document.documentElement.clientHeight ||
           document.body.clientHeight;
  },

  /**
   * Return the offset amount to deduct from the normal scroll position.
   * Modify as appropriate to allow for dynamic calculations
   */
  getFixedOffset: function() {
    var OFFSET_HEIGHT_PADDING = 20;
    // TODO: this is a little janky. We should try to not rely on JS for this
    return document.getElementById("sphinx-template-page-level-bar").offsetHeight + OFFSET_HEIGHT_PADDING;
  },

  findParent: function(item) {
    return $(item).parent().parent().siblings("a.reference.internal")
  },
  makeHighlight: function(item) {
    if ($(item).hasClass("title-link")) {
      return
    }
    $(item).addClass("side-scroll-highlight");
    var parent = utilities.findParent(item);
    if (~parent.hasClass("title-link")) {
      utilities.makeHighlight(parent)
    }
  }
}
