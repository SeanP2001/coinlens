// When the coin form is submitted
document.getElementById("coin-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // stop the page from reloading

    // Get the form and the data from the form
    const form = e.target;
    const formData = new FormData(form);

    // Get the image files from the form
    const fileInput1 = form.querySelector('input[name="image1"]');
    const fileInput2 = form.querySelector('input[name="image2"]');
    const files = [fileInput1.files[0], fileInput2.files[0]];

    // Ensure that both images are given
    const errorDiv = document.getElementById("form-error");
    if (!fileInput1.files[0] || !fileInput2.files[0]) {
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
        renderImagesWithText(files, data);
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

function renderImagesWithText(files, data) {
    // Get the image elements from the page
    const obverseImg = document.getElementById("obverse-img");
    const reverseImg = document.getElementById("reverse-img");
    
    // Get the image files from the form 
    // The data from the LLM shows which image was identified as each side (obverse or reverse)
    const obverseFile = files[data.obverse_image_no - 1];
    const reverseFile = files[data.reverse_image_no - 1];

    // Create a temporary in-memory URL for each image
    // And point the image element source to these URLs
    obverseImg.src = URL.createObjectURL(obverseFile);
    reverseImg.src = URL.createObjectURL(reverseFile);

    // Populate the descriptions
    document.getElementById("obverse-description-val").innerText = data.obverse_image_desc
    document.getElementById("reverse-description-val").innerText = data.reverse_image_desc

    // Populate the transcriptions
    document.getElementById("obverse-transcription-val").innerText = data.obverse_text
    document.getElementById("reverse-transcription-val").innerText = data.reverse_text
}