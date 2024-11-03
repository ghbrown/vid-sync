document.addEventListener('DOMContentLoaded', () => {
    const videoInputs = document.querySelector('.video-inputs');

    function addVideoInput() {
        const videoRow = document.createElement('div');
        videoRow.classList.add('video-row');

        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Enter video link';
        input.className = 'video-link';

        // Add keyboard event listener to support Enter key
        input.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                addButton.click(); // Trigger the Add button click event
            }
        });

        const addButton = document.createElement('button');
        addButton.textContent = 'Add';
        addButton.className = 'add-video-button';

        addButton.addEventListener('click', () => {
            const videoLink = input.value.trim();
            if (videoLink) {
                addButton.textContent = videoLink; // Replace "Add" with the video link
                input.style.display = 'none'; // Hide the input
                addButton.disabled = true; // Disable the button
                const removeButton = document.createElement('img');
                removeButton.src = '../static/assets/sword.png'; // Replace with the correct path
                removeButton.className = 'remove-video-button';
                removeButton.addEventListener('click', () => {
                    videoRow.remove(); 
                });
                videoRow.insertBefore(removeButton, addButton);
                addVideoInput(); // Add new row for the next video input
            } else {
                alert('Please enter a valid video link.');
            }
        });

        videoRow.appendChild(input);
        videoRow.appendChild(addButton);
        videoInputs.appendChild(videoRow);
    }

    // Initial row
    addVideoInput();
});

function run() {
  // Read links
  var links_html = document.getElementsByClassName("video-link");  // object collection
  var links = new Array(links_html.length);  // proper urls

  for (let i = 0; i < links_html.length; i++) {
    var cur_url = links_html[i].value;
    links[i] = cur_url;
  }

  // Remove empty links
  var found_last_link = false;
  while (!found_last_link && links.length >= 1) {
    if (links.at(-1) === "") {
      links.pop();
    } else {
      found_last_link = true;
    }
  }

  // Serialize list of URLs
  var links_json = JSON.stringify(links);
  fetch("/process_urls", {
    method: "POST",
    body: links_json,
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
  .then(response => response.json())
  .then(data => {
    const resultDisplay = document.getElementById("result-display");

    // Set the result message and add the "Go" button if links are returned
    // resultDisplay.innerHTML = `Result: ${data.message}`;
    // if (data.links && data.links.length > 0) {
    //   resultDisplay.innerHTML += `<br><a href="${data.links[0]}" target="_blank" class="go-button">Go</a>`;
    // }
    // if (data.link) {
      resultDisplay.innerHTML += `<br><a href="${data.link}" target="${data.link}" class="go-button">Go</a>`;
    // }

    resultDisplay.style.display = "block"; // Show the result display
  })
  .catch(error => {
    console.error("Error:", error);
    const resultDisplay = document.getElementById("result-display");

    // Display the error message
    resultDisplay.innerText = "An error occurred. Please try again.";
    resultDisplay.style.display = "block";
  });
}


