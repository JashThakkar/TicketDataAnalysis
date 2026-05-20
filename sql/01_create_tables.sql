DROP TABLE IF EXISTS ticket_updates;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS sla_policies;
DROP TABLE IF EXISTS support_agents;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS support_teams;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS locations;

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    region VARCHAR(50)
);

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE support_teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);

CREATE TABLE systems (
    system_id SERIAL PRIMARY KEY,
    system_name VARCHAR(100) NOT NULL,
    system_type VARCHAR(100),
    business_criticality VARCHAR(20)
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(150),
    department_id INT REFERENCES departments(department_id),
    location_id INT REFERENCES locations(location_id)
);

CREATE TABLE support_agents (
    agent_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(150),
    team_id INT REFERENCES support_teams(team_id)
);

CREATE TABLE sla_policies (
    sla_id SERIAL PRIMARY KEY,
    priority VARCHAR(20) NOT NULL,
    response_target_hours INT NOT NULL,
    resolution_target_hours INT NOT NULL
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    agent_id INT REFERENCES support_agents(agent_id),
    team_id INT REFERENCES support_teams(team_id),
    system_id INT REFERENCES systems(system_id),
    sla_id INT REFERENCES sla_policies(sla_id),

    created_at TIMESTAMP NOT NULL,
    first_response_at TIMESTAMP,
    resolved_at TIMESTAMP,

    status VARCHAR(30) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),

    first_response_time_hours NUMERIC(10,2),
    resolution_time_hours NUMERIC(10,2),

    sla_breached BOOLEAN,
    satisfaction_score INT,

    ticket_summary TEXT
);

CREATE TABLE ticket_updates (
    update_id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES tickets(ticket_id),
    updated_at TIMESTAMP NOT NULL,
    update_type VARCHAR(50),
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    update_notes TEXT
);