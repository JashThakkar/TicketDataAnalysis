from pathlib import Path
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

fake = Faker()
Faker.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_locations():
    return pd.DataFrame([
        [1, "Headquarters", "Atlanta", "GA", "Southeast"],
        [2, "Remote - East", "Charlotte", "NC", "Southeast"],
        [3, "Remote - Central", "Dallas", "TX", "Central"],
        [4, "Remote - West", "Phoenix", "AZ", "West"],
        [5, "Branch Office", "Nashville", "TN", "Southeast"],
    ], columns=["location_id", "location_name", "city", "state", "region"])


def generate_departments():
    return pd.DataFrame([
        [1, "Information Technology"],
        [2, "Finance"],
        [3, "Human Resources"],
        [4, "Operations"],
        [5, "Sales"],
        [6, "Marketing"],
        [7, "Engineering"],
        [8, "Customer Support"],
        [9, "Legal"],
        [10, "Executive"],
    ], columns=["department_id", "department_name"])


def generate_support_teams():
    return pd.DataFrame([
        [1, "Helpdesk L1"],
        [2, "Helpdesk L2"],
        [3, "Network Operations"],
        [4, "Security Operations"],
        [5, "Application Support"],
        [6, "Infrastructure"],
    ], columns=["team_id", "team_name"])


def generate_systems():
    return pd.DataFrame([
        [1, "Active Directory", "Identity", "Critical"],
        [2, "VPN Gateway", "Network", "Critical"],
        [3, "Exchange Email", "Email", "High"],
        [4, "WiFi Controller", "Network", "High"],
        [5, "ERP System", "Business Application", "Critical"],
        [6, "CRM Platform", "Business Application", "High"],
        [7, "File Server", "Storage", "Medium"],
        [8, "Print Server", "Infrastructure", "Low"],
        [9, "Endpoint Security", "Security", "Critical"],
        [10, "Cloud Storage", "Cloud", "Medium"],
    ], columns=["system_id", "system_name", "system_type", "business_criticality"])


def generate_sla_policies():
    return pd.DataFrame([
        [1, "Critical", 1, 4],
        [2, "High", 2, 8],
        [3, "Medium", 4, 24],
        [4, "Low", 8, 72],
    ], columns=["sla_id", "priority", "response_target_hours", "resolution_target_hours"])


def save_csv(df, filename):
    output_path = RAW_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Created {output_path}")

def generate_employees(num_employees=300):
    employees = []

    for employee_id in range(1, num_employees + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        employees.append([
            employee_id,
            first_name,
            last_name,
            f"{first_name.lower()}.{last_name.lower()}@company.com",
            random.randint(1, 10),  # department_id
            random.randint(1, 5),   # location_id
        ])

    return pd.DataFrame(employees, columns=[
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "department_id",
        "location_id",
    ])


def generate_support_agents(num_agents=35):
    agents = []

    for agent_id in range(1, num_agents + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        agents.append([
            agent_id,
            first_name,
            last_name,
            f"{first_name.lower()}.{last_name.lower()}@company.com",
            random.randint(1, 6),  # team_id
        ])

    return pd.DataFrame(agents, columns=[
        "agent_id",
        "first_name",
        "last_name",
        "email",
        "team_id",
    ])

def generate_tickets(num_tickets=10000):
    tickets = []

    statuses = ["Resolved", "Closed", "In Progress", "Open"]
    status_weights = [0.70, 0.15, 0.10, 0.05]

    priorities = ["Critical", "High", "Medium", "Low"]
    priority_weights = [0.05, 0.20, 0.50, 0.25]

    categories = {
        "Password Reset": ["Forgot password", "Expired password", "Password reset request"],
        "VPN Issue": ["VPN connection failed", "MFA failure", "VPN disconnecting"],
        "Email Issue": ["Outlook not syncing", "Mailbox access issue", "Email delivery delay"],
        "WiFi/Network": ["Slow network", "WiFi disconnecting", "No internet access"],
        "Hardware": ["Laptop issue", "Monitor not working", "Docking station problem"],
        "Software Access": ["Application access request", "Permission issue", "License missing"],
        "Account Lockout": ["Account locked", "Too many login attempts", "AD account issue"],
        "Printer Issue": ["Printer offline", "Print queue stuck", "Unable to print"],
        "Security Alert": ["Suspicious login", "Phishing email reported", "Endpoint alert"],
        "Application Error": ["Application crash", "ERP timeout", "CRM login issue"],
    }

    sla_lookup = {
        "Critical": {"sla_id": 1, "response": 1, "resolution": 4},
        "High": {"sla_id": 2, "response": 2, "resolution": 8},
        "Medium": {"sla_id": 3, "response": 4, "resolution": 24},
        "Low": {"sla_id": 4, "response": 8, "resolution": 72},
    }

    start_date = datetime.now() - timedelta(days=730)

    for ticket_id in range(1, num_tickets + 1):
        created_at = start_date + timedelta(
            days=random.randint(0, 729),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        status = random.choices(statuses, weights=status_weights, k=1)[0]
        priority = random.choices(priorities, weights=priority_weights, k=1)[0]

        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])

        employee_id = random.randint(1, 300)
        agent_id = random.randint(1, 35)
        team_id = random.randint(1, 6)
        system_id = random.randint(1, 10)

        sla_id = sla_lookup[priority]["sla_id"]
        response_target = sla_lookup[priority]["response"]
        resolution_target = sla_lookup[priority]["resolution"]

        # Response time: usually within SLA, sometimes late
        if random.random() < 0.82:
            first_response_time_hours = round(random.uniform(0.1, response_target), 2)
        else:
            first_response_time_hours = round(random.uniform(response_target, response_target * 2.5), 2)

        first_response_at = created_at + timedelta(hours=first_response_time_hours)

        if status in ["Resolved", "Closed"]:
            # Resolution time: usually within SLA, sometimes breached
            if random.random() < 0.78:
                resolution_time_hours = round(random.uniform(first_response_time_hours, resolution_target), 2)
            else:
                resolution_time_hours = round(random.uniform(resolution_target, resolution_target * 3), 2)

            resolved_at = created_at + timedelta(hours=resolution_time_hours)
            sla_breached = resolution_time_hours > resolution_target
            satisfaction_score = random.choices([1, 2, 3, 4, 5], weights=[0.03, 0.07, 0.15, 0.35, 0.40], k=1)[0]
        else:
            resolution_time_hours = None
            resolved_at = None
            sla_breached = None
            satisfaction_score = None

        ticket_summary = f"{subcategory} - {category.lower()} reported by user"

        tickets.append([
            ticket_id,
            employee_id,
            agent_id,
            team_id,
            system_id,
            sla_id,
            created_at,
            first_response_at,
            resolved_at,
            status,
            priority,
            category,
            subcategory,
            first_response_time_hours,
            resolution_time_hours,
            sla_breached,
            satisfaction_score,
            ticket_summary
        ])

    return pd.DataFrame(tickets, columns=[
        "ticket_id",
        "employee_id",
        "agent_id",
        "team_id",
        "system_id",
        "sla_id",
        "created_at",
        "first_response_at",
        "resolved_at",
        "status",
        "priority",
        "category",
        "subcategory",
        "first_response_time_hours",
        "resolution_time_hours",
        "sla_breached",
        "satisfaction_score",
        "ticket_summary"
    ])

def generate_ticket_updates(tickets_df):
    updates = []
    update_id = 1

    for _, ticket in tickets_df.iterrows():
        ticket_id = ticket["ticket_id"]
        created_at = pd.to_datetime(ticket["created_at"])
        first_response_at = pd.to_datetime(ticket["first_response_at"])
        resolved_at = pd.to_datetime(ticket["resolved_at"]) if pd.notna(ticket["resolved_at"]) else None
        status = ticket["status"]

        # Ticket created
        updates.append([
            update_id,
            ticket_id,
            created_at,
            "Created",
            None,
            "Open",
            "Ticket created by employee"
        ])
        update_id += 1

        # First response
        updates.append([
            update_id,
            ticket_id,
            first_response_at,
            "First Response",
            "Open",
            "In Progress",
            "Support agent responded to ticket"
        ])
        update_id += 1

        # Optional escalation for some tickets
        if random.random() < 0.18:
            escalation_time = created_at + timedelta(
                hours=random.uniform(1, 12)
            )

            updates.append([
                update_id,
                ticket_id,
                escalation_time,
                "Escalation",
                "In Progress",
                "Escalated",
                "Ticket escalated to higher support tier"
            ])
            update_id += 1

        # Resolution/closure for completed tickets
        if status in ["Resolved", "Closed"] and resolved_at is not None:
            updates.append([
                update_id,
                ticket_id,
                resolved_at,
                "Resolved",
                "In Progress",
                "Resolved",
                "Issue resolved by support team"
            ])
            update_id += 1

            if status == "Closed":
                closed_at = resolved_at + timedelta(hours=random.uniform(1, 48))

                updates.append([
                    update_id,
                    ticket_id,
                    closed_at,
                    "Closed",
                    "Resolved",
                    "Closed",
                    "Ticket closed after user confirmation"
                ])
                update_id += 1

    return pd.DataFrame(updates, columns=[
        "update_id",
        "ticket_id",
        "updated_at",
        "update_type",
        "old_status",
        "new_status",
        "update_notes"
    ])

def main():
    save_csv(generate_locations(), "locations.csv")
    save_csv(generate_departments(), "departments.csv")
    save_csv(generate_support_teams(), "support_teams.csv")
    save_csv(generate_systems(), "systems.csv")
    save_csv(generate_sla_policies(), "sla_policies.csv")

    save_csv(generate_employees(), "employees.csv")
    save_csv(generate_support_agents(), "support_agents.csv")

    tickets_df = generate_tickets()
    save_csv(tickets_df, "tickets.csv")

    ticket_updates_df = generate_ticket_updates(tickets_df)
    save_csv(ticket_updates_df, "ticket_updates.csv")

    print("\nSynthetic helpdesk data generated successfully.")


if __name__ == "__main__":
    main()