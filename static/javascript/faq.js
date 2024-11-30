var acc = document.getElementsByClassName("question");
  var i;

  for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
      this.classList.toggle("active");
      this.parentElement.classList.toggle("active");

      var pannel = this.nextElementSibling;
      var arrowUp = this.querySelector(".arrow-up");
      var arrowDown = this.querySelector(".fa-chevron-down");

      if (pannel.style.display === "block") {
        pannel.style.display = "none";
        arrowUp.style.display = "none";
        arrowDown.style.display = "block";
      } else {
        pannel.style.display = "block";
        arrowUp.style.display = "block";
        arrowDown.style.display = "none";
      }
    });
  }