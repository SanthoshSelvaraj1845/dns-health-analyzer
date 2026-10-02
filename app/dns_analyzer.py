import dns.resolver


# =========================================================
# DNS RECORD LOOKUP
# =========================================================

def get_dns_records(domain: str) -> dict:
    """
    Retrieve common DNS records for the given domain.

    Record types:
    - A
    - AAAA
    - MX
    - NS
    - TXT
    """

    dns_records = {}

    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
    ]

    for record_type in record_types:

        try:

            answers = dns.resolver.resolve(
                domain,
                record_type,
                lifetime=5.0
            )

            dns_records[record_type] = [
                answer.to_text()
                for answer in answers
            ]

        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.resolver.LifetimeTimeout,
        ):

            dns_records[record_type] = []

        except Exception:

            dns_records[record_type] = []

    return dns_records


# =========================================================
# DNSSEC CHECK
# =========================================================

def check_dnssec(domain: str) -> dict:
    """
    Perform basic DNSSEC configuration detection.

    The function checks:

    1. DNSKEY records
    2. DS records

    DNSKEY records contain the public keys used by DNSSEC.

    DS records are normally published in the parent zone and
    help establish the DNSSEC chain of trust.

    This is DNSSEC configuration detection, not full
    cryptographic chain validation.
    """

    dnskey_records = []
    ds_records = []

    dnskey_error = None
    ds_error = None


    # =====================================================
    # CHECK DNSKEY RECORDS
    # =====================================================

    try:

        dnskey_answers = dns.resolver.resolve(
            domain,
            "DNSKEY",
            raise_on_no_answer=False,
            lifetime=5.0
        )

        if dnskey_answers.rrset is not None:

            dnskey_records = [
                record.to_text()
                for record in dnskey_answers
            ]

    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
    ):

        dnskey_records = []

    except (
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ) as error:

        dnskey_error = str(error)

    except Exception as error:

        dnskey_error = str(error)


    # =====================================================
    # CHECK DS RECORDS
    # =====================================================

    try:

        ds_answers = dns.resolver.resolve(
            domain,
            "DS",
            raise_on_no_answer=False,
            lifetime=5.0
        )

        if ds_answers.rrset is not None:

            ds_records = [
                record.to_text()
                for record in ds_answers
            ]

    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
    ):

        ds_records = []

    except (
        dns.resolver.NoNameservers,
        dns.resolver.LifetimeTimeout,
    ) as error:

        ds_error = str(error)

    except Exception as error:

        ds_error = str(error)


    # =====================================================
    # DETERMINE DNSSEC STATUS
    # =====================================================

    has_dnskey = bool(dnskey_records)

    has_ds = bool(ds_records)


    # Stronger indication:
    # both DNSKEY and DS records are available.

    if has_dnskey and has_ds:

        status = "enabled"

        enabled = True

        message = (
            "DNSKEY and DS records were detected. "
            "DNSSEC appears to be configured."
        )


    # DNSKEY exists but DS was not detected.
    elif has_dnskey:

        status = "partial"

        enabled = True

        message = (
            "DNSKEY records were detected, but no DS "
            "records were found."
        )


    # DS exists but DNSKEY was not returned.
    elif has_ds:

        status = "partial"

        enabled = True

        message = (
            "DS records were detected, but DNSKEY "
            "records could not be retrieved."
        )


    # Resolver/network problem means we should not
    # incorrectly claim DNSSEC is disabled.
    elif dnskey_error or ds_error:

        status = "unknown"

        enabled = False

        message = (
            "DNSSEC status could not be fully determined "
            "because one or more DNS queries failed."
        )


    # Neither DNSKEY nor DS was detected.
    else:

        status = "not_enabled"

        enabled = False

        message = (
            "No DNSKEY or DS records were detected."
        )


    # =====================================================
    # BUILD RESULT
    # =====================================================

    result = {

        "status": status,

        "enabled": enabled,

        "message": message,

        "dnskey_count":
            len(dnskey_records),

        "dnskey_records":
            dnskey_records,

        "ds_count":
            len(ds_records),

        "ds_records":
            ds_records,
    }


    # Add errors only when a DNS query actually failed.

    if dnskey_error:

        result["dnskey_error"] = (
            dnskey_error
        )


    if ds_error:

        result["ds_error"] = (
            ds_error
        )


    return result


# =========================================================
# DOMAIN HEALTH CHECK
# =========================================================

def calculate_health(
    dns_records: dict
) -> tuple:
    """
    Perform basic DNS health checks.

    A domain is considered healthy when:

    - At least one A record exists
    - At least one NS record exists
    """

    health_checks = {

        "has_a_record":
            bool(
                dns_records.get(
                    "A",
                    []
                )
            ),

        "has_aaaa_record":
            bool(
                dns_records.get(
                    "AAAA",
                    []
                )
            ),

        "has_mx_record":
            bool(
                dns_records.get(
                    "MX",
                    []
                )
            ),

        "has_ns_record":
            bool(
                dns_records.get(
                    "NS",
                    []
                )
            ),

        "has_txt_record":
            bool(
                dns_records.get(
                    "TXT",
                    []
                )
            ),
    }


    healthy = (
        health_checks[
            "has_a_record"
        ]
        and
        health_checks[
            "has_ns_record"
        ]
    )


    return (
        health_checks,
        healthy
    )


# =========================================================
# MAIN DOMAIN ANALYZER
# =========================================================

def analyze_domain(domain: str) -> dict:
    """
    Analyze the DNS health of a domain.

    The returned result contains:

    - Domain
    - Overall health status
    - DNS records
    - Individual health checks
    - DNSSEC information
    """

    # Remove accidental whitespace.

    domain = domain.strip().lower()


    # =====================================================
    # DNS RECORDS
    # =====================================================

    dns_records = get_dns_records(
        domain
    )


    # =====================================================
    # HEALTH CHECKS
    # =====================================================

    (
        health_checks,
        healthy
    ) = calculate_health(
        dns_records
    )


    # =====================================================
    # DNSSEC CHECK
    # =====================================================

    dnssec_result = check_dnssec(
        domain
    )


    # =====================================================
    # FINAL RESULT
    # =====================================================

    result = {

        "domain":
            domain,

        "health_status":
            (
                "healthy"
                if healthy
                else "unhealthy"
            ),

        "dns_records":
            dns_records,

        "health_checks":
            health_checks,

        "dnssec":
            dnssec_result,
    }


    return result