from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
EXPORT_DIR = BASE_DIR / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

QUERIES = {
    "Executive Summary": """
        SELECT
            COUNT(*) AS total_tickets,

            COUNT(*) FILTER (
                WHERE status IN ('Open', 'In Progress')
            ) AS open_tickets,

            COUNT(*) FILTER (
                WHERE status IN ('Resolved', 'Closed')
            ) AS resolved_or_closed_tickets,

            ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time_hours,

            ROUND(AVG(first_response_time_hours), 2) AS avg_first_response_time_hours,

            ROUND(
                100.0 *
                SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END)
                / NULLIF(COUNT(sla_breached), 0),
                2
            ) AS sla_compliance_percent,

            ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction_score
        FROM tickets;
    """,

    "Monthly Trends": """
        SELECT
            TO_CHAR(month, 'YYYY-MM') AS month,
            ticket_count
        FROM vw_monthly_ticket_trends
        ORDER BY month;
    """,

    "SLA Performance": """
        SELECT *
        FROM vw_sla_performance;
    """,

    "Team Performance": """
        SELECT *
        FROM vw_support_team_performance;
    """,

    "Open Backlog": """
        SELECT *
        FROM vw_open_ticket_backlog;
    """,

    "Category Breakdown": """
        SELECT
            category,
            COUNT(*) AS total_tickets,
            ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time_hours,
            ROUND(AVG(first_response_time_hours), 2) AS avg_first_response_time_hours,
            SUM(CASE WHEN sla_breached = TRUE THEN 1 ELSE 0 END) AS sla_breaches,
            ROUND(
                100.0 *
                SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END)
                / NULLIF(COUNT(sla_breached), 0),
                2
            ) AS sla_compliance_percent
        FROM tickets
        WHERE sla_breached IS NOT NULL
        GROUP BY category
        ORDER BY total_tickets DESC;
    """,

    "Department Breakdown": """
        SELECT
            d.department_name,
            COUNT(t.ticket_id) AS total_tickets,
            ROUND(AVG(t.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(CASE WHEN t.sla_breached = TRUE THEN 1 ELSE 0 END) AS sla_breaches,
            ROUND(
                100.0 *
                SUM(CASE WHEN t.sla_breached = FALSE THEN 1 ELSE 0 END)
                / NULLIF(COUNT(t.sla_breached), 0),
                2
            ) AS sla_compliance_percent
        FROM tickets t
        JOIN employees e
            ON t.employee_id = e.employee_id
        JOIN departments d
            ON e.department_id = d.department_id
        WHERE t.sla_breached IS NOT NULL
        GROUP BY d.department_name
        ORDER BY total_tickets DESC;
    """,

    "Agent Performance": """
        SELECT
            sa.agent_id,
            sa.first_name || ' ' || sa.last_name AS agent_name,
            st.team_name,
            COUNT(t.ticket_id) AS total_tickets,
            ROUND(AVG(t.resolution_time_hours), 2) AS avg_resolution_time_hours,
            ROUND(AVG(t.satisfaction_score), 2) AS avg_satisfaction_score,
            SUM(CASE WHEN t.sla_breached = TRUE THEN 1 ELSE 0 END) AS sla_breaches,
            ROUND(
                100.0 *
                SUM(CASE WHEN t.sla_breached = FALSE THEN 1 ELSE 0 END)
                / NULLIF(COUNT(t.sla_breached), 0),
                2
            ) AS sla_compliance_percent
        FROM tickets t
        JOIN support_agents sa
            ON t.agent_id = sa.agent_id
        JOIN support_teams st
            ON sa.team_id = st.team_id
        WHERE t.sla_breached IS NOT NULL
        GROUP BY sa.agent_id, agent_name, st.team_name
        ORDER BY total_tickets DESC;
    """
}


def export_excel_report():
    output_path = EXPORT_DIR / "helpdesk_operations_report.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, query in QUERIES.items():
            df = pd.read_sql(query, engine)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Exported {sheet_name}: {len(df)} rows")

    print(f"\nExcel report created: {output_path}")


if __name__ == "__main__":
    export_excel_report()