var cardWidth = $(".carousel-item").width();

var upWidth = $(".up_inner")[0].scrollWidth;
var upscrollPosition = 0;

var regWidth = $(".reg_inner")[0].scrollWidth;
var regscrollPosition = 0;

var consWidth = $(".cons_inner")[0].scrollWidth;
var consscrollPosition = 0;

$(".up_next_btn").on("click", function () {
    if (upscrollPosition <= (upWidth - cardWidth * 2)) { //check if you can go any further
        upscrollPosition += cardWidth;  //update scroll position
        $(".up_inner").animate({ scrollLeft: upscrollPosition },600); //scroll left
    }
});
$(".reg_next_btn").on("click", function () {
    if (regscrollPosition <= (regWidth - cardWidth * 2)) { //check if you can go any further
        regscrollPosition += cardWidth;  //update scroll position
        $(".reg_inner").animate({ scrollLeft: regscrollPosition },600); //scroll left
    }
});
$(".cons_next_btn").on("click", function () {
    if (scrollPosition <= (carouselWidth - cardWidth * 2)) { //check if you can go any further
        scrollPosition += cardWidth;  //update scroll position
        $(".cons_inner").animate({ scrollLeft: scrollPosition },600); //scroll left
    }
});

// previous card buttons 
$(".up_prev_btn").on("click", function () {
    if (upscrollPosition > 0) {
        upscrollPosition -= cardWidth;
        $(".up_inner").animate(
        { scrollLeft: upscrollPosition },
        600
        );
    }
});
$(".reg_prev_btn").on("click", function () {
    if (regscrollPosition > 0) {
        regscrollPosition -= cardWidth;
        $(".reg_inner").animate(
        { scrollLeft: regscrollPosition },
        600
        );
    }
});
$(".cons_prev_btn").on("click", function () {
    if (scrollPosition > 0) {
        scrollPosition -= cardWidth;
        $(".cons_inner").animate(
        { scrollLeft: scrollPosition },
        600
        );
    }
});