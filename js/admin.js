// check user info method:GET
const nav_login = document.getElementById("nav_login");
const nav_logout = document.getElementById("nav_logout");
const nav_logo = document.getElementById("nav_logo")
fetch("/api/user")
  .then(res => res.json())
  .then((data) => {
    console.log("user info:", data["data"])

    if (data["data"] != null) {
      nav_login.style.display = "none";
      nav_logout.style.display = "block";
      nav_logo.innerHTML = data["data"]["name"]
      nav_logo.style.display = "block";
      showAskLeaveData()
      showStaff()
    } else {
      location.href = "/";
    }
  })


// log out method:DELETE 
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


// approve_button & enter TSMC button
const show_approve_button = document.getElementById("show_approve_button");
const ask_leave_section = document.getElementById("ask_leave_section");
const show_enter_tsmc_button = document.getElementById("show_enter_tsmc_button");
const enter_tsmc_section = document.getElementById("enter_tsmc_section");
const show_sign_up_button = document.getElementById("show_sign_up_button");
const sign_up_section = document.getElementById("sign_up_section");
show_approve_button.addEventListener("click", function () {
  ask_leave_section.style.display = "block";
  enter_tsmc_section.style.display = "none";
  sign_up_section.style.display = "none";
});
show_enter_tsmc_button.addEventListener("click", function () {
  ask_leave_section.style.display = "none";
  enter_tsmc_section.style.display = "block";
  sign_up_section.style.display = "none";
});
show_sign_up_button.addEventListener("click", function () {
  ask_leave_section.style.display = "none";
  enter_tsmc_section.style.display = "none";
  sign_up_section.style.display = "block";
});


//  show all staff ask Leave List method:GET
function showAskLeaveData() {
  let ask_leave_list = document.getElementById("ask_leave_list");
  fetch("/api/admin")
    .then(res => res.json())
    .then(res => {
      console.log(res["data"]);
      for (i = 0; i < res["data"].length; i++) {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        let spanDelete = document.createElement("span");
        let spanUpdate = document.createElement("span");
        let deleteButton = document.createElement("button");
        let updateButton = document.createElement("button");
        tr.className = "table-dark";
        td.className = "table-secondary";
        spanDelete.className = "span_button";
        spanUpdate.className = "span_button";
        deleteButton.className = "btn btn-primary";
        updateButton.className = "btn btn-primary";
        td.append("姓名" + JSON.stringify(res["data"][i]["name"]) + " 請假日期: " + JSON.stringify(res["data"][i]["ask_leave_day"]) + " " + "請假原因: " + JSON.stringify(res["data"][i]["ask_leave_reason"]));
        // console.log(div);
        deleteButton.innerHTML = "刪除";
        deleteButton.setAttribute("data-id", res["data"][i]["id"]);
        deleteButton.addEventListener("click", deleteAskLeave);
        updateButton.innerHTML = "更新";
        updateButton.setAttribute("data-id", res["data"][i]["id"]);
        spanDelete.appendChild(deleteButton);
        spanUpdate.appendChild(updateButton);
        td.append(spanDelete, spanUpdate);

        tr.append(td);
        ask_leave_list.appendChild(tr);

      }
    }
    )
}


//  delete button method:DELETE
function deleteAskLeave(btn) {
  const askLeaveId = btn.target.getAttribute('data-id');
  console.log(askLeaveId);
  fetch(`/api/staff/${askLeaveId}`, {
    method: "DELETE",
  })
    .then(res => {
      window.location.reload();
    })
}


// enter TSMC
// show staff list method: "PATCH"
function showStaff() {
  const enter_tsmc_list = document.getElementById("enter_tsmc_list");
  fetch("/api/admin", {
    method: "PATCH",
    headers: { "content-type": "application/json" },
  })
    .then(res => res.json())
    .then(res => {
      console.log("method:PATCH", res["data"]);
      for (i = 0; i < res["data"].length; i++) {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        tr.className = "table-dark";
        td.className = "table-secondary";
        td.append("姓名" + JSON.stringify(res["data"][i][1]));
        tr.append(td);
        enter_tsmc_list.appendChild(tr);

      }
    })
}






//  sign up method:POST
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
  let sign_up_info = document.getElementById("sign_up_info");
  // let sign_up_success = document.getElementById("sign_up_success");

  fetch("/api/admin", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: userInfo
  })
    .then(res => res.json())
    .then(data => {
      console.log("method:POST", data);
      if (data["ok"] == true) {
        sign_up_info.textContent = data["message"];

      } else {
        sign_up_info.textContent = data["message"];
      }
    })
})