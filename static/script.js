// Form submission handler
document.getElementById("query-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("Form submitted");
    await fetchOpenAIResponse();
});

async function fetchOpenAIResponse() {
    const queryInput = document.getElementById("query");
    const query = queryInput.value.trim();
    const responseContainer = document.getElementById("response-container");
    const responseElement = document.getElementById("response");

    // Clear the existing content and set up the question title
    responseContainer.innerHTML = ""; 

    const questionTitle = document.createElement("h2");
    questionTitle.textContent = query;
    questionTitle.style.textAlign = "center";
    questionTitle.style.fontFamily = "'EB Garamond', serif";
    responseContainer.appendChild(questionTitle);

    responseElement.textContent = "";
    responseElement.style.textAlign = "center";
    responseContainer.appendChild(responseElement);

    const bellIcon = document.querySelector(".bell-icon");

    // Disable the bell icon and change its class
    bellIcon.disabled = true;
    bellIcon.classList.add("bell-icon-clicked");
    bellIcon.classList.remove("bell-icon");

    console.log("Query:", query);

    // Remove the hidden class if it exists
    responseContainer.classList.remove("hidden");

    if (!query) {
        responseElement.textContent = "Please enter a question.";
        responseContainer.classList.add("visible");
        enableBellIcon(bellIcon);
        return;
    }

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query_text: query }),
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            throw new Error("Failed to fetch the response from the server.");
        }

        const data = await response.json();
        console.log("Response data:", data);

        if (data.response) {
            responseElement.textContent = data.response;
            responseContainer.classList.add("visible");
            console.log("Response displayed");
        } else {
            responseElement.textContent = "No response received.";
            responseContainer.classList.add("visible");
        }

        queryInput.value = "";

    } catch (error) {
        console.error("Error:", error);
        responseElement.textContent = "An error occurred. Please try again.";
        responseContainer.classList.add("visible");
    } finally {
        enableBellIcon(bellIcon);
    }
}

function enableBellIcon(bellIcon) {
    bellIcon.disabled = false;
    bellIcon.classList.add("bell-icon");
    bellIcon.classList.remove("bell-icon-clicked");
}

// Typewriter animation - runs when page loads
document.addEventListener("DOMContentLoaded", async () => {
    const typewriterArea = document.getElementById("typewriter-area");

    // Fetch quotes from Flask API
    let lines = [];
    try {
        const res = await fetch("/api/quotes");
        lines = await res.json();
        console.log("Fetched quotes:", lines.length);
    } catch (err) {
        console.error("Error fetching quotes:", err);
    }

    // Define 3 fixed regions for text blocks
    const regions = [
        { x: 50, y: 100, maxWidth: 300 },      // Top left
        { x: window.innerWidth - 350, y: 150, maxWidth: 300 }, // Top right
        { x: 100, y: window.innerHeight - 250, maxWidth: 320 }  // Bottom left
    ];

    async function typewriterEffect(lineText, region) {
        return new Promise(resolve => {
            const el = document.createElement("div");
            el.classList.add("typewriter-line");
            el.textContent = "";
            el.style.maxWidth = `${region.maxWidth}px`;
            typewriterArea.appendChild(el);

            // Position the element
            el.style.left = `${region.x}px`;
            el.style.top = `${region.y}px`;

            // Typewriter effect
            let i = 0;
            el.style.opacity = 1;
            el.classList.add("typewriter");
            const typingInterval = setInterval(() => {
                if (i < lineText.length) {
                    el.textContent += lineText.charAt(i);
                    i++;
                } else {
                    clearInterval(typingInterval);
                    el.classList.remove("typewriter");
                    
                    // Fade out after 3 seconds
                    setTimeout(() => {
                        el.style.opacity = 0;
                        setTimeout(() => el.remove(), 1000);
                    }, 3000);
                    
                    resolve();
                }
            }, 50); // Faster typing speed
        });
    }

    async function startAnimation() {
        let lineIndex = 0;
        
        // Animate 2-3 quotes at a time in different regions
        while (lineIndex < Math.min(lines.length, 9)) {
            const promises = [];
            
            // Start 2-3 animations simultaneously in different regions
            for (let i = 0; i < Math.min(3, regions.length); i++) {
                if (lineIndex < lines.length) {
                    const region = regions[i];
                    promises.push(typewriterEffect(lines[lineIndex], region));
                    lineIndex++;
                }
            }
            
            // Wait for all current animations to complete
            await Promise.all(promises);
            
            // Pause before next batch
            await new Promise(res => setTimeout(res, 1500));
        }
        
        // Loop the animation
        setTimeout(() => {
            if (lines.length > 0) {
                startAnimation();
            }
        }, 2000);
    }

    if (lines.length > 0) {
        startAnimation();
    }
});