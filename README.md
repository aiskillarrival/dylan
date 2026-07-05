# 12-Lesson Syllabus: Backend, Snowflake, and dbt

This syllabus is designed to help a student:

1. Read scripts and understand what they do.
2. Learn backend fundamentals: app components, infrastructure, DevOps, and architecture.
3. Build analytics and reporting workflows with Snowflake and dbt.
4. Process data using SQL and Snowflake stored procedures.

Constraints for this track:

- No PySpark
- No Airflow

## Lesson 1: Reading Scripts and Building a Mental Model

- Goal: Understand how to read code and SQL scripts with confidence.
- Topics:
  - How to scan a script: inputs, processing, outputs
  - Recognizing control flow, dependencies, and side effects
  - Reading SQL scripts and identifying transformation steps
- Hands-on:
  - Annotate a provided script line-by-line
  - Write a short summary of script purpose, inputs, and outputs

## Lesson 2: Backend Fundamentals and App Components

- Goal: Understand what makes up a backend application.
- Topics:
  - APIs, services, databases, queues, and batch jobs
  - Request/response flow and data lifecycle
  - Stateless vs stateful services
- Hands-on:
  - Draw a simple backend component diagram
  - Map where analytics data enters and exits the system

## Lesson 3: Architecture Basics for Data and Analytics Systems

- Goal: Learn practical architecture patterns used in backend + analytics.
- Topics:
  - Layered architecture (ingest, transform, serve)
  - OLTP vs OLAP responsibilities
  - Tradeoffs: cost, performance, reliability
- Hands-on:
  - Convert a business requirement into a high-level architecture

## Lesson 4: Infrastructure and DevOps Foundations

- Goal: Understand infrastructure and deployment concepts for data systems.
- Topics:
  - Environments: dev, test, prod
  - IaC concepts (what it is, why it matters)
  - CI/CD basics for SQL + analytics projects
- Hands-on:
  - Create a release checklist for dbt and Snowflake changes

## Lesson 5: Snowflake Core Concepts

- Goal: Build strong Snowflake fundamentals.
- Topics:
  - Warehouses, databases, schemas, roles, and permissions
  - Tables, views, transient/temporary objects
  - Query execution and cost awareness
- Hands-on:
  - Set up a basic Snowflake workspace model (schemas + roles)

## Lesson 6: Data Modeling for Analytics

- Goal: Model data for clear reporting and maintainability.
- Topics:
  - Fact and dimension tables
  - Star schema basics
  - Naming conventions and data contracts
- Hands-on:
  - Design a mini star schema for a reporting use case

## Lesson 7: dbt Foundations

- Goal: Use dbt to structure and manage SQL transformations.
- Topics:
  - dbt project structure and model materializations
  - refs, sources, macros, and variables
  - Basic tests and documentation
- Hands-on:
  - Create staging and mart models in dbt
  - Add tests for key columns and relationships

## Lesson 8: dbt Intermediate Patterns

- Goal: Improve quality, reusability, and maintainability in dbt.
- Topics:
  - Incremental models
  - Reusable macros and Jinja patterns
  - Source freshness and testing strategy
- Hands-on:
  - Convert one model to incremental
  - Add custom tests and project docs

## Lesson 9: Snowflake SQL Stored Procedures

- Goal: Build procedural data workflows in Snowflake (without PySpark).
- Topics:
  - When to use stored procedures vs plain SQL models
  - Procedure inputs, control flow, and error handling
  - Logging and audit table patterns
- Hands-on:
  - Implement a stored procedure to orchestrate multi-step SQL processing

## Lesson 10: Reporting and Analytics Delivery

- Goal: Deliver reliable and understandable reporting datasets.
- Topics:
  - KPI definitions and metric consistency
  - Semantic layer mindset for reporting tables/views
  - Performance tuning for reporting queries
- Hands-on:
  - Build a reporting-ready mart and benchmark query performance

## Lesson 11: Operations, Monitoring, and Reliability

- Goal: Operate analytics pipelines safely without Airflow.
- Topics:
  - Task scheduling options in Snowflake (tasks, chains)
  - Monitoring run status and failure handling
  - Data quality checks and alerting strategy
- Hands-on:
  - Create a runbook for incident response and recovery

## Lesson 12: Capstone Project

- Goal: Integrate backend thinking with Snowflake + dbt implementation.
- Topics:
  - End-to-end architecture review
  - Build and present a production-style analytics workflow
  - Defend design decisions and tradeoffs
- Hands-on:
  - Deliver a capstone that includes:
    - Architecture diagram
    - dbt models and tests
    - Snowflake stored procedure(s)
    - Reporting table/view layer
    - Monitoring and runbook notes

## Expected Outcomes by the End

The student should be able to:

- Read backend and SQL scripts and explain behavior clearly.
- Describe backend app components and architecture tradeoffs.
- Build Snowflake + dbt analytics pipelines for reporting.
- Implement SQL processing with Snowflake stored procedures.
- Operate data workflows using Snowflake-native scheduling (no Airflow).
