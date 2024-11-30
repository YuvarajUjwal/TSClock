$(".partners-slider").owlCarousel({
    loop: true,
    autoplay: true,
    autoplayTimeout: 3000,
    margin: 10,
    nav: true,
    navText: [
      "<i class='fa-solid fa-arrow-left'></i>",
      "<i class='fa-solid fa-arrow-right'></i>"
    ],
    responsive: {
      0: {
        items: 1
      },
      500: {
        items: 2
      },
      700: {
        items: 3
      },
      1000: {
        items: 5
      }
    }
  });