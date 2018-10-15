window.sideMenus = {
  rightMenuIsOnScreen: function() {
    return document.getElementById("pytorch-content-right").offsetParent !== null;
  },

  isFixedToBottom: false,

  bind: function() {
    sideMenus.handleLeftMenu();

    var rightMenuHasLinks = document.querySelectorAll("#pytorch-right-menu li").length > 1;

    if (rightMenuHasLinks) {
      // Don't show the Shortcuts menu title text unless there are menu items
      document.getElementById("pytorch-shortcuts-wrapper").style.display = "block";

      // Remove superfluous titles unless there are more than one
      var titles = document.querySelectorAll("#pytorch-side-scroll-right > ul > li");

      if (titles.length === 1) {
        titles[0].querySelector("a.reference.internal").style.display = "none";
      }

      sideMenus.handleRightMenu();
    }

    $(window).on('resize scroll', function(e) {
      sideMenus.handleNavBar();

      sideMenus.handleLeftMenu();

      if (sideMenus.rightMenuIsOnScreen()) {
        sideMenus.handleRightMenu();
      }
    });
  },

  leftMenuIsFixed: function() {
    return document.getElementById("pytorch-left-menu").classList.contains("make-fixed");
  },

  handleNavBar: function() {
    var mainHeaderHeight = document.getElementById('header-holder').offsetHeight;

    // If we are scrolled past the main navigation header fix the sub menu bar to top of page
    if (utilities.scrollTop() >= mainHeaderHeight) {
      document.getElementById("pytorch-left-menu").classList.add("make-fixed");
      document.getElementById("pytorch-page-level-bar").classList.add("left-menu-is-fixed");
    } else {
      document.getElementById("pytorch-left-menu").classList.remove("make-fixed");
      document.getElementById("pytorch-page-level-bar").classList.remove("left-menu-is-fixed");
    }
  },

  handleLeftMenu: function () {
    var windowHeight = window.innerHeight;
    var topOfFooterRelativeToWindow = document.getElementById("docs-tutorials-resources").getBoundingClientRect().top;

    if (topOfFooterRelativeToWindow >= windowHeight) {
      document.getElementById("pytorch-left-menu").style.height = "100%";
    } else {
      var howManyPixelsOfTheFooterAreInTheWindow = windowHeight - topOfFooterRelativeToWindow;
      var leftMenuDifference = howManyPixelsOfTheFooterAreInTheWindow;
      document.getElementById("pytorch-left-menu").style.height = (windowHeight - leftMenuDifference) + "px";
    }
  },

  handleRightMenu: function() {
    var rightMenu = document.getElementById("pytorch-right-menu");

    // If left menu is fixed, fix the right menu
    if (sideMenus.leftMenuIsFixed()) {
      rightMenu.classList.add("make-fixed");
    } else {
      rightMenu.classList.remove("make-fixed");
    }

    var rightMenuList = rightMenu.getElementsByTagName("ul")[0];
    var rightMenuBottom = utilities.offset(rightMenuList).top + rightMenuList.offsetHeight;
    var footerTop = utilities.offset(document.getElementById("docs-tutorials-resources")).top;
    var isBottomOfMenuPastOrCloseToFooter = rightMenuBottom >= footerTop  || footerTop - rightMenuBottom <= 40
    var heightOfFooterOnScreen = $(window).height() - document.getElementById("docs-tutorials-resources").getBoundingClientRect().top;

    if (heightOfFooterOnScreen < 0) {
      heightOfFooterOnScreen = 0;
    }

    // If the right menu is already fixed to the bottom
    if (this.isFixedToBottom) {
      var isFooterOnScreen = isElementInViewport(document.getElementById("docs-tutorials-resources"));

      // If the footer is still on the screen, we want to keep the menu where it is
      if (isFooterOnScreen) {
        bottom = heightOfFooterOnScreen;
        rightMenu.style.bottom = bottom + "px";
      } else {
        // If the footer is not on the screen, we want to break the side menu out of the bottom
        this.isFixedToBottom = false;
        rightMenu.style.height = getRightMenuHeight(heightOfFooterOnScreen);
        rightMenu.style.bottom = bottom;
      }

    // If the side menu is past the footer's top or close to it (by 40 pixels)
    // we fix the menu to the bottom
    } else if (isBottomOfMenuPastOrCloseToFooter) {
      var isFooterOnScreen = isElementInViewport(document.getElementById("docs-tutorials-resources"));
      var bottom = 0;

      this.isFixedToBottom = true;

      if (isFooterOnScreen) {
        bottom = heightOfFooterOnScreen;
        rightMenu.style.bottom = bottom + "px";
      } else {
        rightMenu.style.height = getRightMenuHeight(heightOfFooterOnScreen);
        rightMenu.style.bottom = bottom;
      }
    } else {
      this.isFixedToBottom = false;
      rightMenu.style.height = getRightMenuHeight(heightOfFooterOnScreen);
      rightMenu.style.bottom = bottom;
    }
  }
};

function getRightMenuHeight(heightOfFooterOnScreen) {
  if (!sideMenus.leftMenuIsFixed()) {
    return "100%";
  }

  return (window.innerHeight - heightOfFooterOnScreen - utilities.headersHeight()) + "px";
}

function isElementInViewport(el) {
  var rect = el.getBoundingClientRect();

  return rect.bottom > 0 &&
    rect.right > 0 &&
    rect.left < (window.innerWidth || document.documentElement.clientWidth) &&
    rect.top < (window.innerHeight || document.documentElement.clientHeight);
}
