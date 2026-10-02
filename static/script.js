const domainInput = document.getElementById("domainInput");
const analyzeButton = document.getElementById("analyzeButton");

const loadingSection = document.getElementById("loadingSection");
const resultsSection = document.getElementById("resultsSection");
const errorSection = document.getElementById("errorSection");
const errorMessage = document.getElementById("errorMessage");


/* =====================================================
   ANALYZE BUTTON
===================================================== */

analyzeButton.addEventListener("click", analyzeDomain);


/* =====================================================
   ENTER KEY
===================================================== */

domainInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        analyzeDomain();
    }

});


/* =====================================================
   ANALYZE DOMAIN
===================================================== */

async function analyzeDomain() {

    let domain = domainInput.value.trim();


    // Remove protocol if user types:
    // https://google.com
    // http://google.com
    domain = domain
        .replace(/^https?:\/\//i, "")
        .replace(/\/.*$/, "");


    if (!domain) {

        showError("Please enter a domain name.");

        return;
    }


    // Reset UI
    hideError();

    resultsSection.classList.add("hidden");
    loadingSection.classList.remove("hidden");

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";


    try {

        /* =================================================
           STEP 1
           POST /api/v1/analysis
        ================================================= */

        const response = await fetch(
            "/api/v1/analysis",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    domain: domain
                })
            }
        );


        if (!response.ok) {

            let message = "DNS analysis failed.";

            try {

                const errorData = await response.json();

                message =
                    errorData.detail ||
                    message;

            } catch (error) {

                console.error(
                    "Unable to parse error response:",
                    error
                );
            }


            throw new Error(message);
        }


        const startData = await response.json();


        console.log(
            "POST response:",
            startData
        );


        const analysisId =
            startData.analysis_id;


        if (!analysisId) {

            throw new Error(
                "Analysis ID was not returned by the server."
            );
        }


        /* =================================================
           STEP 2
           GET /api/v1/analysis/{analysis_id}
        ================================================= */

        const resultResponse = await fetch(
            `/api/v1/analysis/${analysisId}`
        );


        if (!resultResponse.ok) {

            throw new Error(
                "Unable to retrieve DNS analysis result."
            );
        }


        const analysisData =
            await resultResponse.json();


        console.log(
            "GET response:",
            analysisData
        );


        /* =================================================
           STEP 3
           DISPLAY RESULT
        ================================================= */

        displayResults(analysisData);


    } catch (error) {

        console.error(
            "DNS Analyzer Error:",
            error
        );


        showError(
            error.message ||
            "Something went wrong while analyzing the domain."
        );

    } finally {

        loadingSection.classList.add("hidden");

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Domain";

    }

}


/* =====================================================
   DISPLAY RESULTS
===================================================== */

function displayResults(data) {

    /*
        Your FastAPI GET response:

        {
            analysis_id: "...",
            domain: "google.com",
            status: "completed",
            result: {
                domain: "...",
                health_status: "healthy",
                dns_records: {...},
                ...
            }
        }
    */


    const result = data.result || {};


    const domain =
        data.domain ||
        result.domain ||
        "Unknown";


    const healthStatus =
        result.health_status ||
        "unknown";


    const dnsRecords =
        result.dns_records ||
        {};


    /* =================================================
       DOMAIN
    ================================================= */

    document.getElementById(
        "domainName"
    ).textContent = domain;


    document.getElementById(
        "analysisDomain"
    ).textContent = domain;


    /* =================================================
       ANALYSIS ID
    ================================================= */

    document.getElementById(
        "analysisId"
    ).textContent =
        data.analysis_id || "-";


    /* =================================================
       ANALYSIS STATUS
    ================================================= */

    document.getElementById(
        "analysisStatus"
    ).textContent =
        capitalize(
            data.status || "unknown"
        );


    /* =================================================
       HEALTH STATUS
    ================================================= */

    document.getElementById(
        "healthStatus"
    ).textContent =
        capitalize(healthStatus);


    const healthBadge =
        document.getElementById(
            "healthBadge"
        );


    const healthy =
        healthStatus
            .toLowerCase() ===
        "healthy";


    if (healthy) {

        healthBadge.className =
            "health-badge healthy";

        healthBadge.innerHTML =
            "<span></span> HEALTHY";

    } else {

        healthBadge.className =
            "health-badge unhealthy";

        healthBadge.innerHTML =
            `<span></span> ${healthStatus.toUpperCase()}`;

    }


    /* =================================================
       DNS RECORDS
    ================================================= */

    renderRecords(
        "aRecords",
        dnsRecords.A
    );


    renderRecords(
        "aaaaRecords",
        dnsRecords.AAAA
    );


    renderRecords(
        "mxRecords",
        dnsRecords.MX
    );


    renderRecords(
        "nsRecords",
        dnsRecords.NS
    );


    renderRecords(
        "txtRecords",
        dnsRecords.TXT
    );


    /* =================================================
       COUNT DNS RECORDS
    ================================================= */

    let totalRecords = 0;


    Object.values(dnsRecords)
        .forEach(records => {

            if (Array.isArray(records)) {

                totalRecords +=
                    records.length;

            }

        });


    document.getElementById(
        "recordCount"
    ).textContent =
        totalRecords;


    /* =================================================
       DNSSEC
    ================================================= */

    displayDNSSEC(result);


    /* =================================================
       SHOW RESULTS
    ================================================= */

    resultsSection.classList.remove(
        "hidden"
    );


    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =====================================================
   DISPLAY DNSSEC
===================================================== */

function displayDNSSEC(result) {

    /*
       Different analyzers may return DNSSEC
       in slightly different formats.

       This checks several common possibilities.
    */

    const dnssec =
        result.dnssec ||
        result.dnssec_status ||
        {};


    let enabled = false;


    if (typeof dnssec === "boolean") {

        enabled = dnssec;

    }


    else if (typeof dnssec === "string") {

        const value =
            dnssec.toLowerCase();


        enabled =
            value === "enabled" ||
            value === "valid" ||
            value === "secure";

    }


    else if (
        dnssec &&
        typeof dnssec === "object"
    ) {

        enabled =
            dnssec.enabled === true ||
            dnssec.valid === true ||
            dnssec.secure === true ||
            dnssec.status === "enabled" ||
            dnssec.status === "valid" ||
            dnssec.status === "secure";

    }


    const statusElement =
        document.getElementById(
            "dnssecStatus"
        );


    const titleElement =
        document.getElementById(
            "dnssecTitle"
        );


    const descriptionElement =
        document.getElementById(
            "dnssecDescription"
        );


    if (enabled) {

        statusElement.textContent =
            "Enabled";


        titleElement.textContent =
            "DNSSEC Enabled";


        descriptionElement.textContent =
            "DNSSEC protection was detected for this domain.";

    } else {

        statusElement.textContent =
            "Not Enabled";


        titleElement.textContent =
            "DNSSEC Not Enabled";


        descriptionElement.textContent =
            "DNSSEC protection was not detected or could not be verified.";

    }

}


/* =====================================================
   RENDER DNS RECORDS
===================================================== */

function renderRecords(
    elementId,
    records
) {

    const container =
        document.getElementById(
            elementId
        );


    container.innerHTML = "";


    if (
        !Array.isArray(records) ||
        records.length === 0
    ) {

        const emptyRecord =
            document.createElement("div");


        emptyRecord.className =
            "record-value";


        emptyRecord.textContent =
            "No records found";


        container.appendChild(
            emptyRecord
        );


        return;

    }


    records.forEach(record => {

        const recordElement =
            document.createElement("div");


        recordElement.className =
            "record-value";


        recordElement.textContent =
            String(record);


        container.appendChild(
            recordElement
        );

    });

}


/* =====================================================
   SHOW ERROR
===================================================== */

function showError(message) {

    loadingSection.classList.add(
        "hidden"
    );


    resultsSection.classList.add(
        "hidden"
    );


    errorMessage.textContent =
        message;


    errorSection.classList.remove(
        "hidden"
    );

}


/* =====================================================
   HIDE ERROR
===================================================== */

function hideError() {

    errorSection.classList.add(
        "hidden"
    );

}


/* =====================================================
   CAPITALIZE
===================================================== */

function capitalize(value) {

    value = String(value);


    if (!value) {
        return "";
    }


    return (
        value.charAt(0).toUpperCase() +
        value.slice(1)
    );

}