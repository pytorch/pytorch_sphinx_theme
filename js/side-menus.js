window.sideMenus = {
  rightMenuInitialTop: $(".pytorch-article h1:first").offset().top,

  bind: function() {
    // Start the Shortcuts menu at the article's H1 position
    $(".pytorch-right-menu").css({top: sideMenus.rightMenuInitialTop});

    $(window).on('load resize scroll', function(e) {
      sideMenus.handleLeftMenu();
      sideMenus.handleRightMenu();
    });
  },

  handleLeftMenu: function () {
    var windowHeight = $(window).height();
    var topOfFooterRelativeToWindow = document.getElementsByClassName("docs-tutorials-resources")[0].getBoundingClientRect().top;

    if (topOfFooterRelativeToWindow >= windowHeight) {
      $(".pytorch-left-menu").css({height: "100%"});
    } else {
      var howManyPixelsOfTheFooterAreInTheWindow = windowHeight - topOfFooterRelativeToWindow;
      var headerHeight = $('.header-holder').height();
      var leftMenuDifference = howManyPixelsOfTheFooterAreInTheWindow + headerHeight;

      $(".pytorch-left-menu").css({height: windowHeight - leftMenuDifference});
    }
  },

  handleRightMenu: function() {
    var scrollPos = $(window).scrollTop();
    var $rightMenu = $(".pytorch-right-menu");
    var initialTop = sideMenus.rightMenuInitialTop;

    if (scrollPos === 0) {
      $rightMenu.css({top: initialTop});
      return;
    }

    var $rightMenuList = $(".pytorch-right-menu ul:first");
    var windowHeight = $(window).height();
    var topOfFooterRelativeToWindow = document.getElementsByClassName("docs-tutorials-resources")[0].getBoundingClientRect().top;
    var bottom = $rightMenuList.offset().top + $rightMenuList.height();
    var footerTop = $(".docs-tutorials-resources").offset().top;
    var stoppingPoint = $(".header-holder").height() + $(".pytorch-page-level-bar").height();
    var PADDING_BETWEEN_MENU_AND_FOOTER = 40;

    // if: the right menu is fixed to the bottom and the site footer is not in the window
    // else if: the bottom position of the right menu matches or is past the top position
    //          of the footer minus padding

    if ($rightMenu.hasClass("fixed-to-bottom") && topOfFooterRelativeToWindow >= windowHeight) {
      $rightMenu.removeClass("fixed-to-bottom").css({top: stoppingPoint});
    } else if (bottom >= -PADDING_BETWEEN_MENU_AND_FOOTER + footerTop) {
      $rightMenu.addClass("fixed-to-bottom").css({top: "auto"});
    } else {
      var top = scrollPos >= (initialTop - stoppingPoint)
                  ? stoppingPoint
                  : initialTop - scrollPos;

      $rightMenu.css({top: top});
    }
  }
};
