import dns.resolver


def analyze_domain(domain: str) -> dict:
    dns_records = {}

    record_types = ["A", "AAAA", "MX", "NS", "TXT"]

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)

            dns_records[record_type] = [
                answer.to_text() for answer in answers
            ]

        except Exception:
            dns_records[record_type] = []

    # Basic health checks
    health_checks = {
        "has_a_record": bool(dns_records["A"]),
        "has_mx_record": bool(dns_records["MX"]),
        "has_ns_record": bool(dns_records["NS"]),
        "has_txt_record": bool(dns_records["TXT"]),
    }

    healthy = (
        health_checks["has_a_record"]
        and health_checks["has_ns_record"]
    )

    return {
        "domain": domain,
        "health_status": "healthy" if healthy else "unhealthy",
        "dns_records": dns_records,
        "health_checks": health_checks,
        "dnssec": {
            "status": "unknown"
        }
    }