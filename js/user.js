// method:GET check user info
let login_user_name = document.getElementById("login_user_name")
let login_user_box = document.getElementById("login_user_box")
let sign_page = document.getElementById("sign_page")
fetch("/api/user")
  .then(res => res.json())
  .then((data) => {
    console.log("user info:", data["data"])

    if (data["data"]["level"] == 1) {
      location.href = "/user/admin";
    } else if (data["data"]["level"] == 0) {
      location.href = "/user/staff";
    }
  })


// method:PATCH login in
let loginButton = document.getElementById("log_in_button")
loginButton.addEventListener("click", function () {
  let password = document.getElementById("login_password").value;
  let phone_number = document.getElementById("login_phone_number").value;
  let login_fail = document.getElementById("login_fail");
  console.log(phone_number, password);
  fetch("/api/user", {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(
      {
        "phone_number": phone_number,
        "password": password
      }
    )
  })
    .then(res => res.json())
    .then((data) => {
      console.log("method:PATCH", data);
      if (data["ok"] == true) {
        if (data["level"] == 1) {
          location.href = "/user/admin";
        } else {
          location.href = "/user/staff";
        }

      } else {
        console.log("message", data["message"])
        login_fail.style.display = "block";
        login_fail.textContent = data["message"]
      }
    })
})