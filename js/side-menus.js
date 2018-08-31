window.sideMenus = {
  rightMenuInitialTop: parseInt($(".pytorch-right-menu").css("top"), 10),

  bind: function() {
    $(window).on('load resize scroll', function(e) {
      sideMenus.handleLeftMenu();
      sideMenus.handleRightMenu();
    });

    $(window).on("load resize", function() {
      var leftMenuWidth = $(".pytorch-left-menu").width();
      var contentRightLeftOffset = $(".pytorch-content-right").offset().left;
      var pageLevelPaddingLeft = parseInt($(".pytorch-page-level-bar").css("padding-left"), 10);
      $(".pytorch-right-menu").css({left: contentRightLeftOffset});
      $(".pytorch-shortcuts-wrapper").css({left: contentRightLeftOffset - leftMenuWidth - pageLevelPaddingLeft});
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
      $rightMenu.removeClass("fixed-to-bottom").css({top: stoppingPoint, left: ""});
    } else if (bottom >= -PADDING_BETWEEN_MENU_AND_FOOTER + footerTop) {
      $rightMenu.addClass("fixed-to-bottom").css({top: "auto", left: 0});
    } else {
      var top = scrollPos >= (initialTop - stoppingPoint)
                  ? stoppingPoint
                  : initialTop - scrollPos;

      $rightMenu.css({top: top});
    }
  }
};
