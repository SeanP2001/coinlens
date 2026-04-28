// When the coin form is submitted
document.getElementById("coin-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // stop the page from reloading

    // Get the data (coin images) from the form
    const form = e.target;
    const formData = new FormData(form);

    const fileInput = form.querySelector('input[name="images"]');
    const files = fileInput.files;

    // Ensure that exactly 2 images are given
    const errorDiv = document.getElementById("form-error");
    if (files.length !== 2) {
        errorDiv.innerText = "Please upload exactly 2 images (front and back of the coin).";
        return;
    }
    else {
        errorDiv.innerText = "";
    }

    try {
        // Show the loader while waiting for the response
        const loader = document.querySelector(".loaderDiv");
        loader.classList.add("active");

        // POST the data to the analyse-coin endpoint
        const response = await fetch("/analyse-coin/", {
            method: "POST",
            body: formData
        });

        // Get the json response from the endpoint
        const data = await response.json();

        // Hide the loader once the response has been received
        loader.classList.remove("active");

        // Print the data to the console
        console.log(data);

        // Render the data on the page (and make visible)
        renderData(data);
        document.getElementById("result").classList.add("active");

    } catch (err) {
        console.error("Error:", err);

    }
});

function renderData(data) {
    // Populate the context paragraph
    document.getElementById("context-paragraph").innerText = data.context;

    // Populate the table
    document.getElementById("country-val").innerText = data.country;
    document.getElementById("year-val").innerText = data.year;
    document.getElementById("denomination-val").innerText = data.denomination;
    document.getElementById("rarity-val").innerText = data.rarity;

    // Construct the string of materials
    const materialsStr = data.materials
        .map(m => `${m.material} (${m.percentage}%)`)
        .join(",\n");
    document.getElementById("materials-val").innerText = materialsStr;

    // Populate the estimate value (as a currency string)
    const estValStr = Number(data.estimated_value).toLocaleString('en-GB', {
        style: 'currency',
        currency: 'GBP'
    });
    document.getElementById("est-value-val").innerText = estValStr;
}