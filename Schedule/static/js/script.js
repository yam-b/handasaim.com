(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function () {
            (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
    a = s.createElement(o),
        m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-97745233-1', 'auto');
ga('send', 'pageview');
$('#test').on('mousemove', function (e) {
    $("#img-tooltip").css({top: e.pageY, left: e.pageX});
    $('[data-toggle="tooltip1"]').tooltip('show')
});

$('#test').on('mouseleave', function (e) {
    $('[data-toggle="tooltip1"]').tooltip('hide')
});

$('#error').on('mousemove', function (e) {
    $('#err-tooltip').css({top: e.pageY, left: e.pageX});
    $('[data-toggle="tooltip2"]').tooltip('show')
});

$('#error').on('mouseleave', function (e) {
    $('[data-toggle="tooltip2"]').tooltip('hide')
});

window.onload = function () {
    $('.selectpicker').selectpicker();

    // scrollYou
    $('.scrollMe .dropdown-menu').scrollyou();

    prettyPrint();
};
/**
 * Created by yamya on 22/04/2017.
 */
