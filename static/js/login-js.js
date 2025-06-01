function animateRememberMe() {
    let label = document.getElementById("remember_label");
    let text = label.innerText;
    label.innerHTML = "";  // Clear the text inside the label
    let wordElements = [];

    // Split the text into words and create spans for each word
    let words = text.split(" ");
    words.forEach((word, index) => {
        let span = document.createElement("span");
        span.innerText = word;
        span.style.color = "white";  // Default color is white
        span.style.display = "inline-block"; // Keeps each word in place
        span.style.marginRight = "4px"; // Small gap between words
        wordElements.push(span);
        label.appendChild(span);

        // Add a space after each word
        if (index < words.length - 1) {
            label.appendChild(document.createTextNode(" "));
        }
    });

    // Check if the checkbox is checked or unchecked
    let checkbox = document.getElementById("remember_me");

    if (checkbox.checked) {
        // Animate each word when the checkbox is checked (color changes to gold)
        let delay = 0;
        wordElements.forEach((span, index) => {
            setTimeout(() => {
                span.style.color = "gold";  // Change the word's color to gold
                span.classList.add("animateUp"); // Move word up
                setTimeout(() => {
                    span.classList.remove("animateUp"); // Return the word to its original position
                }, 500); // After 500ms, return it to its place
            }, delay);
            delay += 500; // Delay for each word (increased delay time to 500ms for visibility)
        });
    } else {
        // Animate each word when the checkbox is unchecked (color changes to white)
        let delay = 0;
        for (let i = wordElements.length - 1; i >= 0; i--) {
            let span = wordElements[i];
            setTimeout(() => {
                span.style.color = "white"; // Change the word's color to white
                span.classList.add("animateDown"); // Move word down
                setTimeout(() => {
                    span.classList.remove("animateDown"); // Return the word to its original position
                }, 500); // After 500ms, return it to its place
            }, delay);
            delay += 300; // Slow down the transition when unchecked (300ms for each word)
        }
    }
}

function closeMessage() {
    document.getElementById("overlay").classList.add("hidden");
}

function closeMessageLog() {
    document.getElementById('messageOverlay').style.display = 'none';
}
 