
# IT Helpdesk Operations Analytics Platform

An end-to-end data analytics project that simulates an enterprise IT helpdesk environment and analyzes ticket trends, SLA performance, backlog aging, team performance, and business impact.

This project uses Python, PostgreSQL, SQL, Excel, and Power BI to demonstrate a realistic data analyst / BI analyst workflow.

## Tech Stack

- Python
- pandas
- Faker
- SQLAlchemy
- PostgreSQL
- pgAdmin
- SQL
- Excel
- Power BI
- DAX

## Project Workflow

Python synthetic data generation
→ PostgreSQL relational database
→ SQL analytics queries and views
→ Python Excel export pipeline
→ Excel operational report
→ Power BI dashboard

## Business Problem

IT helpdesk teams need visibility into ticket volume, SLA compliance, agent workload, backlog aging, and business impact.

This project answers questions such as:

- How many tickets are created over time?
- Which ticket categories occur most often?
- Which priorities have the most SLA breaches?
- Which teams and agents handle the most workload?
- Which departments generate the most support demand?
- How old are unresolved tickets?
- Which systems create the most operational impact?

## Data Model

The PostgreSQL database uses a relational schema with the following tables:

- locations
- departments
- employees
- support_teams
- support_agents
- systems
- sla_policies
- tickets
- ticket_updates

The tickets table is the central fact table.

## Python Scripts

### generate_data.py

Generates realistic synthetic IT helpdesk data.

Creates CSV files for:
- locations
- departments
- support teams
- systems
- SLA policies
- employees
- support agents
- tickets
- ticket updates

Simulates:
- ticket creation dates
- priorities
- categories
- response times
- resolution times
- SLA breaches
- satisfaction scores
- ticket lifecycle updates

Output:
data/raw/*.csv

### test_connection.py

Tests Python connectivity to PostgreSQL using environment variables stored in .env.

### load_to_postgres.py

Loads generated CSV files into PostgreSQL.

Responsibilities:
- connect to PostgreSQL
- clear existing data
- load CSVs in correct FK order
- populate relational database tables

### export_reports.py

Exports analytics data from PostgreSQL into an Excel workbook.

Creates:
helpdesk_operations_report.xlsx

Sheets:
- Executive Summary
- Monthly Trends
- SLA Performance
- Team Performance
- Open Backlog
- Category Breakdown
- Department Breakdown
- Agent Performance

## SQL Files

### 01_create_tables.sql

Creates:
- tables
- primary keys
- foreign keys
- relationships

Defines the PostgreSQL relational schema.

### 02_indexes_constraints.sql

Adds:
- indexes
- query optimization
- check constraints
- data validation rules

Improves performance and integrity.

### 03_analysis_queries.sql

Contains analytical SQL queries including:
- total tickets
- open tickets
- SLA compliance
- average resolution time
- ticket trends
- category analysis
- priority analysis

### 04_views.sql

Creates reporting views:
- vw_monthly_ticket_trends
- vw_sla_performance
- vw_support_team_performance
- vw_open_ticket_backlog

These views are used in Power BI and Excel reporting.

## PostgreSQL Usage

PostgreSQL is the primary relational database for the project.

Database:
helpdesk_analytics

PostgreSQL is used for:
- relational modeling
- SQL analytics
- views
- Power BI integration
- operational reporting

Power BI connects directly to PostgreSQL using:
Server: localhost
Database: helpdesk_analytics

## Excel Output

The project generates:
helpdesk_operations_report.xlsx

Includes:
- executive KPIs
- SLA reporting
- team performance
- backlog monitoring
- department analysis
- agent analysis

## Power BI Dashboard

Dashboard pages:
1. Executive Overview
2. SLA Performance
3. Team Performance
4. Backlog & Aging
5. Business Impact

Power BI features used:
- DAX measures
- KPI cards
- slicers
- line charts
- bar charts
- donut charts
- tables
- date table
- calculated columns
- relational model

## Installation Instructions

### Clone Repository

git clone <repo-url>

### Create Virtual Environment

python -m venv venv

Windows:
.\\venv\\Scripts\\Activate.ps1

Mac/Linux:
source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Install PostgreSQL

Download:
https://www.postgresql.org/download/

Recommended:
PostgreSQL 17.x

### Create Database

CREATE DATABASE helpdesk_analytics;

### Create .env File

DB_HOST=localhost
DB_PORT=5432
DB_NAME=helpdesk_analytics
DB_USER=postgres
DB_PASSWORD=your_password

### Run SQL Files

01_create_tables.sql
02_indexes_constraints.sql
03_analysis_queries.sql
04_views.sql

### Generate Data

python scripts/generate_data.py

### Load Data

python scripts/load_to_postgres.py

### Export Excel Report

python scripts/export_reports.py

### Open Power BI Dashboard

Connect Power BI to:
Server: localhost
Database: helpdesk_analytics

## Skills Demonstrated

- SQL
- PostgreSQL
- relational modeling
- Power BI
- DAX
- Python
- pandas
- ETL
- Excel reporting
- business intelligence
- operational analytics
- dashboard engineering

## Project Summary

This project demonstrates an end-to-end analytics workflow for IT helpdesk operations using Python, PostgreSQL, SQL, Excel, and Power BI.
