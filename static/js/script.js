// When the coin form is submitted
document.getElementById("coin-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // stop the page from reloading

    // Get the data (coin images) from the form
    const form = e.target;
    const formData = new FormData(form);

    try {
        console.log('Processing...');

        // POST the data to the analyse-coin endpoint
        const response = await fetch("/analyse-coin/", {
            method: "POST",
            body: formData
        });

        // Get the json response from the endpoint
        const data = await response.json();

        // Print the data to the console
        console.log(data);

        // Render the data on the page
        document.getElementById("result").innerText =
            JSON.stringify(data, null, 2);

    } catch (err) {
        console.error("Error:", err);
    }
});