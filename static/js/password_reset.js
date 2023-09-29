document.addEventListener("DOMContentLoaded", function() {
    var resetButtons = document.querySelectorAll(".reset-button");

    resetButtons.forEach(function(button) {
      var updatedDate = new Date(button.getAttribute("data-updated"));
      var currentDate = new Date();

      // Calculate the difference in milliseconds
      var timeDifference = currentDate - updatedDate;
      console.log(timeDifference)

      // Calculate the difference in days
      var daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      console.log(daysDifference)

      if (daysDifference > 80) {
        button.style.display = "inline-block";
        button.addEventListener()
      } else {
        button.style.display = "none";
      }
    });
  });