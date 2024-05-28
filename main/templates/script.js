function calibrate() {
  const offset = document.getElementById("calibration-offset").value;
  fetch("/calibrate", {
    method : "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ offset: parseFloat(offset) }),
  }).then((response) => {
    if (response.ok) {
      console.log("Calibration updated successfully.");
    } else {
      console.error("Failed to update calibration.");
    }
  });
}

function toggleOff() {
  fetch("/toggle_off", {
    method: "POST",
  }).then((response) => {
    if (response.ok) {
      console.log("Server turned off.");
    } else {
      console.error("Failed to turn off server.");
    }
  });
}
