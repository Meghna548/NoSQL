const API = "http://127.0.0.1:5000";


async function searchReports() {

    const search =
        document.getElementById(
            "search"
        ).value;

    const response =
        await fetch(
            API +
            "/api/reports?search=" +
            encodeURIComponent(search)
        );

    const data =
        await response.json();

    displayReports(data);
}


function displayReports(data) {

    const container =
        document.getElementById(
            "reports"
        );

    container.innerHTML = "";

    if (data.length === 0) {

        container.innerHTML =
            "<p>No reports found.</p>";

        return;
    }


    data.forEach(report => {

        const div =
            document.createElement(
                "div"
            );

        div.className = "report";

        div.innerHTML = `
            <h3>${report.title}</h3>

            <p>
                ${report.summary}
            </p>

            <p>
                Category:
                ${report.category}
            </p>

            <p class="threat">
                Threat Level:
                ${report.threat_level}
            </p>
        `;

        container.appendChild(div);

    });
}


async function classifyThreat() {

    const text =
        document.getElementById(
            "classificationText"
        ).value;

    const response =
        await fetch(
            API +
            "/api/classify?text=" +
            encodeURIComponent(text)
        );

    const data =
        await response.json();

    document.getElementById(
        "classificationResult"
    ).innerText =
        "Threat Level: " +
        data.threat_level;
}


searchReports();