const socket = io();
socket.on('new_alert', (data) => {
    alert("⚠️ Intrusion Detected: " + JSON.stringify(data));
    location.reload();
});

if (response.status === 403) {
  resultBox.innerHTML = `<p style="color:red;"><strong>Threat Detected:</strong> ${data.details.attack_type}<br>
    Confidence: ${(data.details.confidence * 100).toFixed(2)}%<br>
    IP Blocked: ${data.details.ip}</p>`;
}
