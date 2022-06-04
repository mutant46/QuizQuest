$(document).ready(function () {
  // owl carousel
  $(".responsive").slick({
    dots: false,
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 2,
    prevArrow : '<button type="button" class="slick-prev"> < </button>',
    nextArrow : '<button type="button" class="slick-next"> > </button>',
    variableWidth: true,
    responsive: [
      {
        breakpoint: 1160,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
          infinite: true,
        },
      },
      {
        breakpoint: 880,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        },
      },
      {
        breakpoint: 620,
        settings: {
          centerMode: true,
          centerPadding: "20px",
          slidesToShow: 1,
        },
      },
    ],
  });
  // navbar onClick function
  $("#hamburger").click(() => {
    $('body').toggleClass('overflow-hidden');
    $("#mynavbar").toggleClass("navbar-menu-open");
  });

  // closing navbar on click outside
  $(document).click(({ target }) => {
    var _opened = $("#mynavbar").hasClass("navbar-menu-open");
    if (_opened && !$(target).is("#hamburger")) {
      $("#mynavbar").removeClass("navbar-menu-open");
      $("body").removeClass("overflow-hidden");
    }
  });
});
