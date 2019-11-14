$('.slideshow').slick({
    lazyLoad: 'ondemand',
    arrows: false,
    autoplay: true,
    autoplaySpeed: 4000,
    infinite: true,
    fade: false,
    pauseOnHover: false,
    pauseOnFocus: false,
    dots: false
});

$('.carousel').on('init', function (event, slick) {
    autoHeight();
});
$('.carousel').slick({
    lazyLoad: 'ondemand',
    autoplay: false,
    autoplaySpeed: 4000,
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    pauseOnHover: false,
    pauseOnFocus: false,
    arrows: false,
    dots: false,
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

function autoHeight() {
    $('.auto-height').each(function () {
        var t = $(this);
        var w = t.width();
        t.css({
            height: (w / 2) + 'px'
        })
    });
}

$(window).on('resize', function () {
    autoHeight();
});



(function ($) {
    'use strict';
    $(function () {
        var current = location.pathname;

        function addActiveClass(element) {
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


function _scrollToTop(scrollDuration) {
    var scrollStep = -window.scrollY / (scrollDuration / 15),
        scrollInterval = setInterval(function () {
            if (window.scrollY != 0) {
                window.scrollBy(0, scrollStep);
            }
            else clearInterval(scrollInterval);
        }, 15);
}

function onBackToTop() {
    var element = document.getElementById('on-back-to-top');
    if (element) {
        element.addEventListener('click', function (event) {
            _scrollToTop(600);
        });
    }
}
onBackToTop();

function showHideBackToTopButton() {
    var element = document.getElementById('on-back-to-top');
    if (element) {
        window.onscroll = function () {
            var nVScroll = document.documentElement.scrollTop || document.body.scrollTop;
            if (nVScroll > 300) {
                element.classList.add('show');
            } else {
                element.classList.remove('show');
            }
        }
    }
}
showHideBackToTopButton();



$('.author-search-field').on('change', function () {
    $('.author-search-form').submit();
});


$('.open-mbl-search-form').on('click', function () {
    var row = $('.mbl-hided-row');
    if (row.hasClass('opened')) {
        row.removeClass('opened');
    } else {
        row.addClass('opened');
    }
});

$('.go-to-form-search').on('click', function () {
    var form = $('.search-form');
    $('html, body').stop().animate({
        scrollTop: form.offset().top - 100
    }, 600, function () {
        var row = $('.mbl-hided-row');
        row.addClass('opened');
    });
});