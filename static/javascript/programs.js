// var video = $(this).find(".course-video")[0];
var autoplayTimeout;
$(document).ready(function () {
  $(".read-more").click(function (event) {
    event.preventDefault();
    var fullDetails = $(this)
      .closest(".course-card")
      .find(".full-details")
      .html();
    $("#fullCourseDetails").html(fullDetails);
    $("#courseModal").css("display", "block");
  });

  $(".close").click(function () {
    $("#courseModal").css("display", "none");
  });

  $(document).click(function (event) {
    if (event.target.id == "courseModal") {
      $("#courseModal").css("display", "none");
    }
  });
  $(".course-card").hover(
    function () {
      var iframe = $(this).find(".course-video");
      var src = iframe.attr("src");
      iframe.attr("src", src + "&autoplay=1&muted=1");
      $(this).find(".video-container").show();
      $(this).find(".course-image").hide();
      clearTimeout(autoplayTimeout);
    },
    function () {
      var iframe = $(this).find(".course-video");
      var src = iframe.attr("src");
      src = src.replace("&autoplay=1&muted=1", "");
      iframe.attr("src", src);
      $(this).find(".video-container").hide();
      $(this).find(".course-image").show();
      autoplayTimeout = setTimeout(function () {
        iframe.attr("src", src);
      }, 0);
    }
  );


  $(".playlist-details-banner").hover(
    function () {
      var iframe = $(this).find(".course-video");
      var src = iframe.attr("src");
      iframe.attr("src", src + "&autoplay=1&muted=1");
      $(this).find(".video-container").show();
      $(this).find(".course-image").hide();
      clearTimeout(autoplayTimeout);
    },
    function () {
      var iframe = $(this).find(".course-video");
      var src = iframe.attr("src");
      src = src.replace("&autoplay=1&muted=1", "");
      iframe.attr("src", src);
      $(this).find(".video-container").hide();
      $(this).find(".course-image").show();
      autoplayTimeout = setTimeout(function () {
        iframe.attr("src", src);
      }, 0);
    }
  );

  
  function showPopup() {
    document.getElementById("mobilePopup").style.display = "block";
}

function closePopup() {
    document.getElementById("mobilePopup").style.display = "none";
}

// Function to detect if the device is mobile
function isMobileDevice() {
    return /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
}

// Function to set the popup message based on device type
function setPopupMessage() {
    var popupMessage = document.querySelector(".popup-content");
    if (isMobileDevice()) {
        popupMessage.textContent = "Tap on the card to play the video.";
    } else {
        popupMessage.textContent = "Hover over the card to play the video.";
    }
}

// Call showPopup() function when the page loads
$(document).ready(function() {
    setPopupMessage();
    // showPopup();
    
    // Close popup when the close button is clicked
    $(".close").on("click", function() {
        closePopup();
    });

    // Close popup when clicking outside the modal
    $(document).click(function(event) {
        if (event.target.id == "mobilePopup") {
            closePopup();
        }
    });
});

});
