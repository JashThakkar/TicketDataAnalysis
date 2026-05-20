-- =========================================
-- TOTAL TICKETS
-- =========================================

SELECT COUNT(*) AS total_tickets
FROM tickets;

-- =========================================
-- OPEN TICKETS
-- =========================================

SELECT COUNT(*) AS open_tickets
FROM tickets
WHERE status IN ('Open', 'In Progress');

-- =========================================
-- SLA COMPLIANCE RATE
-- =========================================

SELECT
    ROUND(
        100.0 *
        SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END)
        /
        COUNT(sla_breached),
        2
    ) AS sla_compliance_percent
FROM tickets
WHERE sla_breached IS NOT NULL;

-- =========================================
-- AVG RESOLUTION TIME
-- =========================================

SELECT
    ROUND(AVG(resolution_time_hours), 2)
    AS avg_resolution_time_hours
FROM tickets
WHERE resolution_time_hours IS NOT NULL;

-- =========================================
-- TICKETS BY PRIORITY
-- =========================================

SELECT
    priority,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY priority
ORDER BY ticket_count DESC;

-- =========================================
-- TICKETS BY CATEGORY
-- =========================================

SELECT
    category,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY category
ORDER BY ticket_count DESC;

-- =========================================
-- MONTHLY TICKET TREND
-- =========================================

SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY month
ORDER BY month;

