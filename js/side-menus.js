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
    var windowHeight = $(window).height();
    var topOfFooterRelativeToWindow = document.getElementsByClassName("docs-tutorials-resources")[0].getBoundingClientRect().top;

    var bottom = $(".pytorch-right-menu ul:first").offset().top + $(".pytorch-right-menu ul:first").height();
    var footerTop = $(".docs-tutorials-resources").offset().top;
    var headersHeight = $(".header-holder").height() + $(".pytorch-page-level-bar").height();
    var top = $(window).scrollTop();
    var initialTop = sideMenus.rightMenuInitialTop;

    if (top === 0) {
      $(".pytorch-right-menu").css({top: initialTop});
    } else {
      var stoppingPoint = headersHeight;

      if (top >= (initialTop - stoppingPoint)) {
        $(".pytorch-right-menu").css({top: stoppingPoint});
      } else {
        $(".pytorch-right-menu").css({top: initialTop - top});
      }
    }

    if (topOfFooterRelativeToWindow >= windowHeight) {
      $(".pytorch-right-menu").removeClass("fixed-to-bottom");
    } else if (bottom >= -40 + footerTop) {
      $(".pytorch-right-menu").addClass("fixed-to-bottom");
    }
  }
};
