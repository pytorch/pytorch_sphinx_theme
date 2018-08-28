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
