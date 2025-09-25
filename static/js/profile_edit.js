document.addEventListener('DOMContentLoaded', function() {
    const verifyBtn = document.getElementById('verifyLocationBtn');
    if (verifyBtn) {
        verifyBtn.addEventListener('click', function () {
            const statusDiv = document.getElementById('verificationStatus');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            statusDiv.innerHTML = `<span class="text-primary">Verifying location...</span>`;

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    fetch("/users/verify-location/", {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
                        body: JSON.stringify({ latitude, longitude })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            statusDiv.innerHTML = `
                                <div class="alert alert-success">
                                    <strong>Location Verified:</strong> ${data.city}, ${data.state}
                                </div>`;
                            document.getElementById('id_city').value = data.city;
                            document.getElementById('id_state').value = data.state;
                        } else {
                            statusDiv.innerHTML = `<span class="text-danger">
                                ${data.message || 'Verification failed. Please try again.'}
                            </span>`;
                        }
                    })
                    .catch(() => {
                        statusDiv.innerHTML = `<span class="text-danger">
                            Could not verify location. Please check your internet connection.
                        </span>`;
                    });
                },
                () => {
                    statusDiv.innerHTML = `<span class="text-danger">
                        Could not get location. Please enable location services in your browser.
                    </span>`;
                }
            );
        });
    }
});
