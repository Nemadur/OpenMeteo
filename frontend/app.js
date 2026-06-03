const API_URL = "http://localhost:8000/api/v1/cities-scores";

document.getElementById("btn").addEventListener("click", getRanking);
const spinner = document.getElementById("spinner");
const button = document.querySelector("button");

async function getRanking() {
    loadingState(true); // show loading state
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;

    if (!dateValidation(startDate, endDate)) {
        loadingState(false); // hide loading state
        return;
    }

    const payload = {};

    // only send dates if user selected them
    if (startDate) payload.start_date = startDate;
    if (endDate) payload.end_date = endDate;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        const list = document.getElementById("results");
        list.innerHTML = "";

        data.rankings.forEach((item) => {
            const li = document.createElement("li");
            li.textContent = `${item.rank}. ${item.city} - ${item.score}`;
            list.appendChild(li);
        });
    } catch (err) {
        console.error(err);
        alert("Error fetching ranking");
    }
    loadingState(false); // hide loading state
}

function dateValidation(startDate, endDate) {
    if (startDate > endDate) {
        alert("Start date must be before end date");
        return false;
    }
    return true;
}

function loadingState(isLoading) {
    if (isLoading) {
        spinner.classList.remove("hidden"); // show spinner
        button.disabled = true;
        button.textContent = "Loading...";
    } else {
        spinner.classList.add("hidden"); // hide spinner
        button.disabled = false;
        button.textContent = "Get Ranking";
    }
}
