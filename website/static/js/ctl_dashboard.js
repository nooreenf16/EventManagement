var cardWidth = $(".carousel-item").width();

var myeventWidth = $(".myeve_inner")[0].scrollWidth;
var myeventscrollPosition = 0;

var myconsWidth = $(".mycons_inner")[0].scrollWidth;
var myconsscrollPosition = 0;

$(".mycons_next_btn").on("click", function () {
    if (myconsscrollPosition < (myconsWidth - cardWidth * 2)) { //check if you can go any further
        myconsscrollPosition += cardWidth;  //update scroll position
        $(".mycons_inner").animate({ scrollLeft: myconsscrollPosition },600); //scroll left
    }
});

$(".myeve_next_btn").on("click", function () {
    if (myeventscrollPosition < (myeventWidth - cardWidth * 2)) { //check if you can go any further
        myeventscrollPosition += cardWidth;  //update scroll position
        $(".myeve_inner").animate({ scrollLeft: myeventscrollPosition },600); //scroll left
    }
});

$(".mycons_prev_btn").on("click", function () {
    if (scrollPosition > 0) {
        scrollPosition -= cardWidth;
        $(".cons_inner").animate(
        { scrollLeft: scrollPosition },
        600
        );
    }
});
$(".myeve_prev_btn").on("click", function () {
    if (upscrollPosition > 0) {
        upscrollPosition -= cardWidth;
        $(".up_inner").animate(
        { scrollLeft: upscrollPosition },
        600
        );
    }
});