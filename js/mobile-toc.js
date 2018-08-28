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
