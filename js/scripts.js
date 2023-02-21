// method:GET check user info
const nav_login = document.getElementById("nav_login");
const nav_logout = document.getElementById("nav_logout");
fetch("/api/user")
  .then(res => res.json())
  // .then(data => console.log(data["data"]))
  .then((data) => {
    // console.log("method:GET:", data)
    console.log("user info:", data["data"])

    if (data["data"] != null) {
      nav_login.style.display = "none";
      nav_logout.style.display = "block";
      nav_logo.innerHTML = data["data"]["name"]
      nav_logo.style.display = "block";
    } else {
      // location.href = "/";
    }
  })


// method:DELETE log out
nav_logout.addEventListener("click", function () {
  fetch("/api/user", {
    method: "DELETE",
    headers: { "content-type": "application/json" },
  })
    .then(res => res.json())
    .then(data => {
      console.log("method:DELETE", data);
      location.reload();
    })
})