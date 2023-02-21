//  FOR USER
// method:GET check user info
const nav_login = document.getElementById("nav_login");
const nav_logout = document.getElementById("nav_logout");
const nav_logo = document.getElementById("nav_logo")
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
      showAskLeaveData()
    } else {
      location.href = "/";
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


//  FOR ASK LEAVE 
//  SHOW Ask Leave List & create delete , update button
function showAskLeaveData() {
  let ask_leave_list = document.getElementById("ask_leave_list");
  fetch("/api/staff")
    .then(res => res.json())
    .then(res => {
      console.log(res["data"]);
      for (i = 0; i < res["data"].length; i++) {
        // console.log(res["data"][i]);
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
        td.append("請假日期: " + JSON.stringify(res["data"][i]["ask_leave_day"]) + " " + "請假原因: " + JSON.stringify(res["data"][i]["ask_leave_reason"]));
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


//  delete button
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


//  create Ask Leave List
let ask_leave_button = document.getElementById("ask_leave_button")
ask_leave_button.addEventListener("click", function () {
  let ask_leave_day = document.getElementById("ask_leave_day").value;
  let ask_leave_reason = document.getElementById("ask_leave_reason").value
  console.log(ask_leave_day, ask_leave_reason);
  fetch("/api/user")
    .then(res => res.json())
    .then(res => {
      let phone_number = res["data"]["phone_number"]
      sendAskLeaveData(ask_leave_day, ask_leave_reason, phone_number)
    })
})


// SEND Ask Leave Data 
function sendAskLeaveData(ask_leave_day, ask_leave_reason, phone_number) {
  console.log(ask_leave_day, ask_leave_reason, phone_number);
  fetch("/api/staff", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(
      {
        "phone_number": phone_number,
        "ask_leave_day": ask_leave_day,
        "ask_leave_reason": ask_leave_reason
      })
  })
    .then(res => res.json())
    .then(res => {
      if (res["ok"] == true) {
        console.log("ok");
        location.reload();
      } else {
        console.log("res", res);
      }
    })
}