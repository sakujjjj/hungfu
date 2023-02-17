fetch("api/user")
  .then(res => res.json())
  // .then(data => console.log(data["data"]))
  .then((res) => {
    if (res["data"] == null) {
      window.location.replace("/");
    }
    else {
      console.log("user info:", res["data"])
      showAskLeaveData()
    }
  })


//  SHOW Ask Leave List 
function showAskLeaveData() {
  let ask_leave_list = document.getElementById("ask_leave_list");
  fetch("api/staff")
    .then(res => res.json())
    .then(res => {
      // console.log(res["data"][0]);
      // console.log(res["data"].length);
      for (i = 0; i < res["data"].length; i++) {
        // console.log(res["data"][i]);
        let div = document.createElement("div");
        div.append("請假日期: " + JSON.stringify(res["data"][i]["ask_leave_day"]) + " " + "請假原因: " + JSON.stringify(res["data"][i]["ask_leave_reason"]));
        // console.log(div);
        ask_leave_list.append(div);


      }
    }
    )
}

// SEND Ask Leave Data List
let ask_leave_button = document.getElementById("ask_leave_button")
ask_leave_button.addEventListener("click", function () {
  let ask_leave_day = document.getElementById("ask_leave_day").value;
  let ask_leave_reason = document.getElementById("ask_leave_reason").value
  // console.log(ask_leave_day, ask_leave_reason);
  fetch("api/user")
    .then(res => res.json())
    .then(res => {
      let phone_number = res["data"]["phone_number"]
      // console.log(ask_leave_day, ask_leave_reason, res["data"]["phone_number"]);
      sendAskLeaveData(ask_leave_day, ask_leave_reason, phone_number)
    })
})


function sendAskLeaveData(ask_leave_day, ask_leave_reason, phone_number) {
  console.log(ask_leave_day, ask_leave_reason, phone_number);
  fetch("api/staff", {
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
      // console.log("sendAskLeaveData:", res);
      if (res["ok"] == true) {
        console.log("ok");
        location.reload();
      } else {
        console.log("res", res);
      }
    })
}