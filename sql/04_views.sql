-- =========================================
-- MONTHLY TICKET TREND VIEW
-- =========================================

CREATE OR REPLACE VIEW vw_monthly_ticket_trends AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;


-- =========================================
-- SLA PERFORMANCE VIEW
-- =========================================

CREATE OR REPLACE VIEW vw_sla_performance AS
SELECT
    priority,
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN sla_breached = TRUE THEN 1 ELSE 0 END) AS breached_tickets,
    ROUND(
        100.0 *
        SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END)
        /
        COUNT(sla_breached),
        2
    ) AS sla_compliance_percent,
    ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time_hours
FROM tickets
WHERE sla_breached IS NOT NULL
GROUP BY priority;


-- =========================================
-- SUPPORT TEAM PERFORMANCE VIEW
-- =========================================

CREATE OR REPLACE VIEW vw_support_team_performance AS
SELECT
    st.team_name,
    COUNT(t.ticket_id) AS total_tickets,
    ROUND(AVG(t.resolution_time_hours), 2) AS avg_resolution_time_hours,
    ROUND(AVG(t.satisfaction_score), 2) AS avg_satisfaction_score,
    ROUND(
        100.0 *
        SUM(CASE WHEN t.sla_breached = FALSE THEN 1 ELSE 0 END)
        /
        COUNT(t.sla_breached),
        2
    ) AS sla_compliance_percent
FROM tickets t
JOIN support_teams st
    ON t.team_id = st.team_id
WHERE t.sla_breached IS NOT NULL
GROUP BY st.team_name
ORDER BY total_tickets DESC;


-- =========================================
-- OPEN TICKET BACKLOG VIEW
-- =========================================

CREATE OR REPLACE VIEW vw_open_ticket_backlog AS
SELECT
    ticket_id,
    priority,
    category,
    status,
    created_at,
    ROUND(
        EXTRACT(EPOCH FROM (NOW() - created_at)) / 3600,
        2
    ) AS hours_open
FROM tickets
WHERE status IN ('Open', 'In Progress')
ORDER BY hours_open DESC;