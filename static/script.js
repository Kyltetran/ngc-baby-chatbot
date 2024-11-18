document.getElementById("query-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = document.getElementById("query").value;
    const responseContainer = document.getElementById("response-container");
    const responseElement = document.getElementById("response");
    const sourcesElement = document.getElementById("sources");

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query_text: query }),
        });

        const data = await response.json();

        // Display the main response
        responseElement.textContent = data.response;
        sourcesElement.innerHTML = ""; // Clear previous sources

        // Extract and format each source's content
        data.sources.forEach((source) => {
            const rawContent = source.content;

            // Use a regular expression to extract only the desired fields
            const match = rawContent.match(/'Chủ đề,Bài viết,Tác giả,Chuyên mục,Số báo,Ngày xuất bản,Nội dung': '([^']+)'/);

            if (match && match[1]) {
                const extractedContent = match[1];

                // Create an <li> element for the extracted content
                const li = document.createElement("li");
                li.textContent = extractedContent; // Display the extracted content
                li.style.whiteSpace = "pre-wrap";  // Preserve formatting
                sourcesElement.appendChild(li);
            }
        });

    } catch (error) {
        responseElement.textContent = "Error fetching the response";
        console.error("Error:", error);
    }
});
