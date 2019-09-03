$(".slideshow").slick({
    arrows: false,
    autoplay: true,
    autoplaySpeed: 100,
    infinite: true,
    fade: true
  });

  $(".carousel").slick({
    lazyLoad: 'ondemand',
    autoplay: true,
    autoplaySpeed: 500,
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1
  });