function socialSignUp(platform) {
  let redirectUrl;

  switch (platform) {
    case "twitter":
      redirectUrl = "https://twitter.com/signup";
      break;
    case "google":
      redirectUrl = "https://accounts.google.com/signup";
      break;
    case "facebook":
      redirectUrl = "https://www.facebook.com/r.php";
      break;
    default:
      console.log("Invalid social platform");
      return;
  }

  window.location.href = redirectUrl;
}

/* Checkbox for Create page */
const checkbox = document.getElementById("checkbox");
const submitBtn = document.querySelector(".PostSubmitbtn");

submitBtn.addEventListener("click", () => {
  if (checkbox.checked) {
    console.log("Checkbox is checked");
  } else {
    console.log("Checkbox is not checked");
  }
});
