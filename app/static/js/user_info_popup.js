document.addEventListener("DOMContentLoaded", function () {
  const userListContainer = document.querySelector(".user-list");
  const popup = document.getElementById("user-info-popup");
  const closePopup = document.querySelector(".close-popup");

  userListContainer.addEventListener("click", function (event) {
    const userElement = event.target.closest(".user");
    if (userElement) {
      const username = userElement.getAttribute("username");

      fetch(`/get_user_info/${username}`)
        .then((response) => response.json())
        .then((userData) => {
          document.getElementById("popup-username").innerText = userData.username;
          document.getElementById("popup-email").innerText = userData.email;
          document.getElementById("popup-phone").innerText = userData.phone;
          document.getElementById("popup-gender").innerText = userData.gender;
          document.getElementById("popup-postcode").innerText = userData.postcode;

          popup.style.display = "block";
        });
    }
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