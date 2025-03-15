document.getElementById("subscribe-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const source = document.getElementById("source").value;
    const message = document.getElementById("message");

    const response = await fetch("https://your-backend-url/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source })
    });

    const result = await response.json();
    message.innerText = result.message || "Something went wrong!";
});
