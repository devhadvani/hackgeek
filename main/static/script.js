function checkEmailAvailability(memberNumber) {
    const emailInput = document.getElementById(`team-member-${memberNumber}`);
    const availabilityMessage = document.getElementById(`availability-message-${memberNumber}`);
    const email = emailInput.value;

    // Make an AJAX request to check email availability
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `/check_email_availability/?email=${email}`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.available) {
                availabilityMessage.textContent = "Email is available";
                availabilityMessage.classList.add("available");
            } else {
                availabilityMessage.textContent = "Email is not available";
                availabilityMessage.classList.remove("available");
            }
        }
    };
    xhr.send();
}
