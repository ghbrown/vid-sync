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
  // read links
  var links_html = document.getElementsByClassName("video-link");  // object collection
  var links = new Array(links_html.length);  // proper urls

  for (let i=0; i<links_html.length; i++) {
    var cur_url = links_html[i].value;
    links[i] = cur_url;
  }

  // remove empty links
  var found_last_link = false;
  while (!found_last_link && links.length>=1) {
    if (links.at(-1) === "") {
        links.pop();
    } else {
      found_last_link = true;
    }
  }

  // serialize list of urls
  var links_json = JSON.stringify(links);
  fetch("https://jsonplaceholder.typicode.com/todos", {
    method: "POST",
    body: links_json,
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    .then((response) => response.json())
    .then((json) => console.log(json));
}
