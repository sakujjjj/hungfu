
// let singInButton = document.getElementById("singInButton");
// singInButton.addEventListener("click", signIn);
// function signIn() {
//     console.log("hi")
// }

// function getUserSignInInfo() {
//     const signInForm = document.querySelector(".signInForm");
//     const signInEmail = document.querySelector(".signInEmail");
//     const signInPassword = document.querySelector(".signInPassword");

//     signInForm.addEventListener("submit", (e) => {
//         disableBackEndSignInMessage();
//         e.preventDefault();
//         let email = signInEmail.value;
//         let password = signInPassword.value;
//         let emailIsValid = examineEmail(signInEmail);
//         let passwordIsValid = examinePassword(signInPassword);
//         if (!emailIsValid || !passwordIsValid) {
//             return;
//         }

//         data = { email, password };
//         fetch("/api/user/auth", {
//             method: "PUT",
//             headers: { "content-type": "application/json" },
//             body: JSON.stringify(data),
//         })
//             .then((res) => res.json())
//             .then((res) => {
//                 if (res.ok === true) {
//                     window.location.reload();
//                     onLoadPage();
//                 }
//                 if (res.error === true) {
//                     enableBackEndMessage(res.message, "signIn");
//                 }
//             });
//     });
// }




/*
let phone_number = "0912345656"
let password = "1234"
data = { password, phone_number };
fetch('api/user', {
    method: "PATCH",
    headers: { "content-type": "multipart/form-data" },
    body: JSON.stringify(data),
})
    .then(function (response) {
        return response.json();
    })
    .then(function (myJson) {
        console.log(myJson);
    });
*/

// email = "test@test";
// password = "1234"
// data1 = { email, password };
// console.log("data1:", data1)
// console.log("data1_type:", typeof (data1))
// console.log("stringify:", JSON.stringify(data1))
// console.log("stringify_type:", typeof (JSON.stringify(data1)))
// console.log(JSON.stringify(data))
// console.log(data)

const form = document.querySelector('#form')
form.addEventListener('submit', function (e) {
    e.preventDefault();
    const data = new FormData(form);
    console.log([...data]);
    fetch("/api/user", {
        method: "PATCH",
        body: data,
    }).then(function (response) {
        return response.text();
    }).then(function (responseData) {
        console.log("responseData:", responseData)
    })
})

