-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX idx_tickets_created_at
ON tickets(created_at);

CREATE INDEX idx_tickets_status
ON tickets(status);

CREATE INDEX idx_tickets_priority
ON tickets(priority);

CREATE INDEX idx_tickets_category
ON tickets(category);

CREATE INDEX idx_tickets_agent_id
ON tickets(agent_id);

CREATE INDEX idx_tickets_team_id
ON tickets(team_id);

CREATE INDEX idx_tickets_system_id
ON tickets(system_id);

CREATE INDEX idx_tickets_sla_breached
ON tickets(sla_breached);

CREATE INDEX idx_ticket_updates_ticket_id
ON ticket_updates(ticket_id);

CREATE INDEX idx_ticket_updates_updated_at
ON ticket_updates(updated_at);

-- =========================================
-- OPTIONAL CHECK CONSTRAINTS
-- =========================================

ALTER TABLE tickets
ADD CONSTRAINT chk_priority
CHECK (priority IN ('Critical', 'High', 'Medium', 'Low'));

ALTER TABLE tickets
ADD CONSTRAINT chk_status
CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed'));

ALTER TABLE tickets
ADD CONSTRAINT chk_satisfaction_score
CHECK (
    satisfaction_score IS NULL
    OR satisfaction_score BETWEEN 1 AND 5
);