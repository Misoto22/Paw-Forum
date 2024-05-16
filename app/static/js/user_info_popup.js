document.addEventListener("DOMContentLoaded", function () {
  const userElements = document.querySelectorAll(".user");
  const popup = document.getElementById("user-info-popup");
  const closePopup = document.querySelector(".close-popup");

  userElements.forEach((user) => {
    user.addEventListener("click", function () {
      const name = user.getAttribute("data-name");
      const gender = user.getAttribute("data-gender");
      const postcode = user.getAttribute("data-postcode");
      const email = user.getAttribute("data-email");
      const phone = user.getAttribute("data-phone");
      const pettype = user.getAttribute("data-pettype");

      document.getElementById("popup-name").innerText = name;
      document.getElementById("popup-gender").innerText = gender;
      document.getElementById("popup-postcode").innerText = postcode;
      document.getElementById("popup-email").innerText = email;
      document.getElementById("popup-phone").innerText = phone;
      document.getElementById("popup-pettype").innerText = pettype;

      // Ensure the popup is fully rendered before calculating its dimensions
      popup.style.display = "block";

      const popupHeight = popup.offsetHeight;
      const popupWidth = popup.offsetWidth;
      const windowHeight = window.innerHeight;
      const windowWidth = window.innerWidth;

      const topPosition = (windowHeight - popupHeight) / 2;
      const leftPosition = (windowWidth - popupWidth) / 2;

      popup.style.top = `${topPosition}px`;
      popup.style.left = `${leftPosition}px`;
    });
  });

  closePopup.addEventListener("click", function () {
    popup.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === popup) {
      popup.style.display = "none";
    }
  });
});
