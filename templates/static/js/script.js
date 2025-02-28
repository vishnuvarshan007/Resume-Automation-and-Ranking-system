window.onload = function() {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "./details.html"; // Redirect on success
                } else {
                    document.getElementById("error-message").innerText = data.message;
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    } else {
        console.error("Login form not found in the DOM!");
    }

    // Resume upload functionality
    const uploadForm = document.getElementById("upload-form");
    const resumeInput = document.getElementById("resume-files");
    const messageBox = document.getElementById("message");

    if (uploadForm && resumeInput && messageBox) {
        uploadForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const formData = new FormData();
            const files = resumeInput.files;

            if (files.length === 0) {
                messageBox.innerText = "Please select a file!";
                return;
            }

            for (let i = 0; i < files.length; i++) {
                formData.append("resumes", files[i]);
            }

            axios.post("http://localhost:5000/upload", formData)
                .then(response => {
                    messageBox.innerText = "Resumes uploaded successfully!";
                    processResumes();
                })
                .catch(error => {
                    messageBox.innerText = "Error uploading resumes.";
                });
        });
    } else {
        console.error("Upload form or elements not found in the DOM!");
    }
};

function processResumes() {
    fetch("http://localhost:5000/process_resumes", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resumes processed and ranked:", data.ranked_resumes);
            alert("Resumes processed successfully!");
        } else {
            alert("Error processing resumes");
        }
    })
    .catch(error => {
        console.error("Error processing resumes:", error);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    const filterSelect = document.getElementById("filter");
    const filterButton = document.getElementById("apply-filter");

    function fetchResumes(filter = "") {
        fetch("http://localhost:5000/details", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ filter: filter }) // Send selected filter
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("resume-table");
            tableBody.innerHTML = ""; // Clear previous data

            if (!data.success) {
                console.error("Error:", data.message);
                return;
            }

            data.resumes.forEach((resume, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${resume.name}</td>
                    <td>${resume.email}</td>
                    <td>${resume.phone ? resume.phone : "Not Available"}</td>
                    <td>${resume.score}</td>
                    <td><a href="http://localhost:5000/uploads/${resume.filename}" target="_blank">View Resume</a></td>
                    <td><button class="send-email" data-email="${resume.email}">Send Email</button></td>
                `;
                tableBody.appendChild(row);
            });

            // Attach event listeners to "Send Email" buttons
            document.querySelectorAll(".send-email").forEach(button => {
                button.addEventListener("click", function() {
                    const email = this.getAttribute("data-email");
                    sendEmail(email);
                });
            });
        })
        .catch(error => console.error("Error fetching resumes:", error));
    }

    // Load resumes on page load
    fetchResumes();

    // Apply filter when the button is clicked
    filterButton.addEventListener("click", function () {
        const selectedFilter = filterSelect.value;
        fetchResumes(selectedFilter);
    });
});



function sendEmail(email) {
    fetch("http://localhost:5000/send_email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Email sent to ${email}`);
        } else {
            alert(`Failed to send email: ${data.message}`);
        }
    })
    .catch(error => console.error("Error sending email:", error));
}
