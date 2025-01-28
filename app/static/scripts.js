const token = localStorage.getItem("token");

        if (!token) {
            alert("You must be logged in to access this page.");
            window.location.href = "/login";
        }

        async function loadProfile() {
            try {
                const response = await fetch("/api/profile", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();

                    // Populate user info
                    const avatar = document.getElementById("avatar");
                    const greeting = document.getElementById("greeting");
                    const userInfo = document.getElementById("userInfo");

                    avatar.src = data.avatar || "https://via.placeholder.com/120";
                    greeting.textContent = `Welcome, Mr. ${data.username}!`;
                    userInfo.innerHTML = `
                        <p><strong>Username:</strong> ${data.username}</p>
                        <p><strong>Email:</strong> ${data.email}</p>
                    `;

                    // Populate ads
                    const adsList = document.getElementById("adsList");
                    adsList.innerHTML = ""; // Clear previous ads
                    data.ads.forEach((ad) => {
                        const adItem = document.createElement("div");
                        adItem.classList.add("ad-item");
                        adItem.innerHTML = `
                            <p><strong>Title:</strong> ${ad.title}</p>
                            <p><strong>Price:</strong> $${ad.price}</p>
                            <p><strong>Description:</strong> ${ad.description}</p>
                        `;
                        adsList.appendChild(adItem);
                    });
                } else {
                    const error = await response.json();
                    alert(error.error || "Failed to load profile.");
                    window.location.href = "/login";
                }
            } catch (error) {
                console.error("Error loading profile:", error);
                alert("An error occurred. Please try again.");
                window.location.href = "/login";
            }
        }

        async function uploadAvatar() {
            const formData = new FormData(document.getElementById("uploadAvatarForm"));
            try {
                const response = await fetch("/upload_avatar", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                    body: formData,
                });

                const result = await response.json();
                if (response.ok) {
                    alert(result.message);
                    loadProfile();
                } else {
                    alert(result.error || "Failed to upload avatar.");
                }
            } catch (error) {
                console.error("Error uploading avatar:", error);
                alert("An error occurred. Please try again.");
            }
        }

        function logout() {
            localStorage.removeItem("token");
            window.location.href = "/login";
        }

        function showAdForm() {
            document.getElementById("adModal").style.display = "block";
        }

        function closeAdForm() {
            document.getElementById("adModal").style.display = "none";
        }

        async function saveAd() {
            const title = document.getElementById("adTitle").value;
            const description = document.getElementById("adDescription").value;
            const price = document.getElementById("adPrice").value;

            const adData = { title, description, price };

            try {
                const response = await fetch("/ads", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(adData),
                });

                if (response.ok) {
                    alert("Ad created successfully!");
                    closeAdForm();
                    loadProfile();
                } else {
                    const error = await response.json();
                    alert(error.error || "Failed to create ad.");
                }
            } catch (error) {
                console.error("Error creating ad:", error);
                alert("An error occurred. Please try again.");
            }
        }

        loadProfile();