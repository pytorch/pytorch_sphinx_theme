window.sideMenus = {
  rightMenuIsOnScreen: function() {
    return document.getElementById("pytorch-content-right").offsetParent !== null;
  },

  isFixedToBottom: false,

  bind: function() {
    sideMenus.handleLeftMenu();

    var rightMenuHasLinks = document.querySelectorAll("#pytorch-right-menu li").length > 1;

    if (rightMenuHasLinks) {
      // We are hiding the titles of the pages in the right side menu but there are a few
      // pages that include other pages in the right side menu (see 'torch.nn' in the docs)
      // so if we exclude those it looks confusing. Here we add a 'title-link' class to these
      // links so we can exclude them from normal right side menu link operations
      var titleLinks = document.querySelectorAll(
        "#pytorch-right-menu #pytorch-side-scroll-right \
         > ul > li > a.reference.internal"
      );

      for (var i = 0; i < titleLinks.length; i++) {
        var link = titleLinks[i];

        link.classList.add("title-link");

        if (
          link.nextElementSibling &&
          link.nextElementSibling.tagName === "UL" &&
          link.nextElementSibling.children.length > 0
        ) {
          link.classList.add("has-children");
        }
      }

      // Add + expansion signifiers to normal right menu links that have sub menus
      var menuLinks = document.querySelectorAll(
        "#pytorch-right-menu ul li ul li a.reference.internal"
      );

      for (var i = 0; i < menuLinks.length; i++) {
        if (
          menuLinks[i].nextElementSibling &&
          menuLinks[i].nextElementSibling.tagName === "UL"
        ) {
          menuLinks[i].classList.add("not-expanded");
        }
      }

      // If a hash is present on page load recursively expand menu items leading to selected item
      var linkWithHash =
        document.querySelector(
          "#pytorch-right-menu a[href=\"" + window.location.hash + "\"]"
        );

      if (linkWithHash) {
        // Expand immediate sibling list if present
        if (
          linkWithHash.nextElementSibling &&
          linkWithHash.nextElementSibling.tagName === "UL" &&
          linkWithHash.nextElementSibling.children.length > 0
        ) {
          linkWithHash.nextElementSibling.style.display = "block";
          linkWithHash.classList.add("expanded");
        }

        // Expand ancestor lists if any
        sideMenus.expandClosestUnexpandedParentList(linkWithHash);
      }

      // Bind click events on right menu links
      $("#pytorch-right-menu a.reference.internal").on("click", function() {
        if (this.classList.contains("expanded")) {
          this.nextElementSibling.style.display = "none";
          this.classList.remove("expanded");
          this.classList.add("not-expanded");
        } else if (this.classList.contains("not-expanded")) {
          this.nextElementSibling.style.display = "block";
          this.classList.remove("not-expanded");
          this.classList.add("expanded");
        }
      });

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

  expandClosestUnexpandedParentList: function (el) {
    var closestParentList = utilities.closest(el, "ul");

    if (closestParentList) {
      var closestParentLink = closestParentList.previousElementSibling;
      var closestParentLinkExists = closestParentLink &&
                                    closestParentLink.tagName === "A" &&
                                    closestParentLink.classList.contains("reference");

      if (closestParentLinkExists) {
        // Don't add expansion class to any title links
         if (closestParentLink.classList.contains("title-link")) {
           return;
         }

        closestParentList.style.display = "block";
        closestParentLink.classList.remove("not-expanded");
        closestParentLink.classList.add("expanded");
        sideMenus.expandClosestUnexpandedParentList(closestParentLink);
      }
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
