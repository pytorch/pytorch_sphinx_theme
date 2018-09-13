window.sideMenus = {
  displayRightMenu: document.querySelectorAll("#pytorch-right-menu li").length > 1,

  isFixedToBottom: false,

  bind: function() {
    sideMenus.handleLeftMenu();

    if (sideMenus.displayRightMenu) {
      // Show the right menu container
      document.getElementById("pytorch-content-right").classList.add("show");

      // Don't show the Shortcuts menu title text unless there are menu items
      document.getElementById("pytorch-shortcuts-wrapper").style.display = "block";

      // Remove superfluous titles unless there are more than one
      var titles = document.querySelectorAll("#pytorch-side-scroll-right > ul > li");

      if (titles.length === 1) {
        titles[0].querySelector("a.reference.internal").style.display = "none";
      }

      // Start the Shortcuts menu at the article's H1 position
      document.getElementById("pytorch-right-menu").style["margin-top"] = sideMenus.rightMenuInitialTop() + "px";

      sideMenus.handleRightMenu();
    }

    $(window).on('resize scroll', function(e) {
      sideMenus.handleLeftMenu();

      if (sideMenus.displayRightMenu) {
        sideMenus.handleRightMenu();
      }
    });
  },

  rightMenuInitialTop: function() {
    return utilities.headersHeight();
  },

  handleLeftMenu: function () {
    var windowHeight = window.innerHeight;
    var topOfFooterRelativeToWindow = document.getElementById("docs-tutorials-resources").getBoundingClientRect().top;

    if (topOfFooterRelativeToWindow >= windowHeight) {
      document.getElementById("pytorch-left-menu").style.height = "100%";
    } else {
      var howManyPixelsOfTheFooterAreInTheWindow = windowHeight - topOfFooterRelativeToWindow;
      var headerHeight = document.getElementById('header-holder').offsetHeight;
      var leftMenuDifference = howManyPixelsOfTheFooterAreInTheWindow + headerHeight;

      document.getElementById("pytorch-left-menu").style.height = (windowHeight - leftMenuDifference) + "px";
    }
  },

  handleRightMenu: function() {
    var rightMenu = document.getElementById("pytorch-right-menu");
    var scrollPos = utilities.scrollTop();

    if (scrollPos === 0) {
      rightMenu.style["margin-top"] = sideMenus.rightMenuInitialTop() + "px";
      return;
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
        rightMenu.style["margin-top"] = "auto";
        rightMenu.style.bottom = bottom + "px";
      } else {
        // If the footer is not on the screen, we want to break the side menu out of the bottom
        this.isFixedToBottom = false;
        rightMenu.style.height = (window.innerHeight - heightOfFooterOnScreen - utilities.headersHeight()) + "px";
        rightMenu.style["margin-top"] = sideMenus.rightMenuInitialTop() + "px";
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
        rightMenu.style["margin-top"] = "auto";
        rightMenu.style.bottom = bottom + "px";
      } else {
        rightMenu.style.height = (window.innerHeight - heightOfFooterOnScreen - utilities.headersHeight()) + "px";
        rightMenu.style["margin-top"] = sideMenus.rightMenuInitialTop() + "px";
        rightMenu.style.bottom = bottom;
      }
    } else {
      this.isFixedToBottom = false;
      rightMenu.style.height = (window.innerHeight - heightOfFooterOnScreen - utilities.headersHeight()) + "px";
      rightMenu.style["margin-top"] = sideMenus.rightMenuInitialTop() + "px";
      rightMenu.style.bottom = bottom;
    }
  }
};

function isElementInViewport(el) {
  var rect = el.getBoundingClientRect();

  return rect.bottom > 0 &&
    rect.right > 0 &&
    rect.left < (window.innerWidth || document.documentElement.clientWidth) &&
    rect.top < (window.innerHeight || document.documentElement.clientHeight);
}
