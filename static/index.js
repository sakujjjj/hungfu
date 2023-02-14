
// method:GET check user info
let login_user_name = document.getElementById("login_user_name")
let login_user_box = document.getElementById("login_user_box")
fetch("api/user")
    .then(res => res.json())
    // .then(data => console.log(data["data"]))
    .then((data) => {
        // console.log("method:GET:", data)
        console.log("user info:", data["data"])

        if (data["data"] == null) {
            login_user_box.style.display = "none";


        } else {
            login_user_box.style.display = "block";
            login_user_name.innerHTML = data["data"]["name"]
            // console.log(login_user_name)
            // console.log(data["data"]["name"])
        }
    })

// method:POST sign up
let sign_up_button = document.getElementById("sign_up_button");
sign_up_button.addEventListener("click", function () {
    let sign_up_user_name = document.getElementById("sign_up_user_name").value
    let sign_up_password = document.getElementById("sign_up_password").value;
    let sign_up_phone_number = document.getElementById("sign_up_phone_number").value;
    let sign_up_email = document.getElementById("sign_up_email").value
    let sign_up_tsmc_id = document.getElementById("sign_up_tsmc_id").value
    let userInfo = JSON.stringify({
        "name": sign_up_user_name,
        "phone_number": sign_up_phone_number,
        "password": sign_up_password,
        "email": sign_up_email,
        "tsmc_id": sign_up_tsmc_id
    });
    let sign_up_fail = document.getElementById("sign_up_fail");
    let sign_up_success = document.getElementById("sign_up_success");
    console.log("userInfo:", userInfo);
    console.log("userInfo:", typeof (userInfo));
    fetch("api/user", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: userInfo
    })
        .then(res => res.json())
        .then(data => {
            console.log("method:POST", data);
            if (data["ok"] == true) {
                sign_up_fail.style.display = "none";
                sign_up_success.style.display = "block";
                sign_up_success.textContent = data["message"];
                console.log(sign_up_success)
            } else {
                sign_up_fail.style.display = "block";
                sign_up_fail.textContent = data["message"];
                console.log(sign_up_fail)
            }
        })
})

// method:PATCH login in
let loginButton = document.getElementById("log_in_button")
loginButton.addEventListener("click", function () {
    let password = document.getElementById("login_password").value
    let phone_number = document.getElementById("login_phone_number").value
    let login_fail = document.getElementById("login_fail")
    // console.log(phone_number, password)
    fetch("api/user", {
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
                location.reload();
            } else {
                console.log("message", data["message"])
                login_fail.style.display = "block";
                // login_fail.innerHTML = data["message"]
                login_fail.textContent = data["message"]
            }

            // 
        })


})


// method:DELETE log out
let logoutButton = document.getElementById("log_out_button")
logoutButton.addEventListener("click", function () {
    fetch("api/user", {
        method: "DELETE",
        headers: { "content-type": "application/json" },
    })
        .then(res => res.json())
        .then(data => {
            console.log("method:DELETE", data);
            location.reload();
        })
})
