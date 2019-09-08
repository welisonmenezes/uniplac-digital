$(".slideshow").slick({
    arrows: false,
    autoplay: true,
    autoplaySpeed: 100,
    infinite: true,
    fade: true,
    pauseOnHover: false,
    pauseOnFocus: false
  });

  $(".carousel").slick({
    lazyLoad: 'ondemand',
    autoplay: true,
    autoplaySpeed: 1500,
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    pauseOnHover: false,
    pauseOnFocus: false,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: true,
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });