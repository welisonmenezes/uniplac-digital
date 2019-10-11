$(".slideshow").slick({
    lazyLoad: 'ondemand',
    arrows: false,
    autoplay: true,
    autoplaySpeed: 4000,
    infinite: true,
    fade: false,
    pauseOnHover: false,
    pauseOnFocus: false
});

$(".carousel").slick({
    lazyLoad: 'ondemand',
    autoplay: true,
    autoplaySpeed: 4000,
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
    ]
});




(function ($) {
    'use strict';
    $(function () {
        var current = location.pathname;

        function addActiveClass(element) {
            console.log(current)
            if (current.includes(element.attr('href'))) {
                if (!element.parent().hasClass('first')) {
                    element.parent().addClass('active');
                } else {
                    if (current === '/') {
                        element.parent().addClass('active');
                    }
                }
            }
        }

        //var current = location.pathname.split("/").slice(-1)[0].replace(/^\/|\/$/g, '');
        var ls = location.pathname.split("/");
        //var current = ls[1] + '/' + ls[2];
        //console.log(ls);
        $('.navbar-nav li a').each(function () {
            var $this = $(this);
            addActiveClass($this);
        })

    });
})(jQuery);