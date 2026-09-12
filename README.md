# Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A cricket analytics dashboard built using Python, SQL, and Streamlit. The application fetches cricket data through the Cricbuzz API, stores structured data in SQLite, performs SQL-based analysis, and presents cricket statistics through an interactive dashboard.

## Project Overview

Cricbuzz LiveStats is designed to demonstrate how real-time API data can be collected, stored, analyzed, and presented through a business-friendly analytics application.

The project combines:

- REST API integration
- SQLite database management
- SQL analytics
- Python data processing
- Streamlit dashboard development
- CRUD operations
- Interactive visualizations

## Key Features

### 🏠 Home Dashboard
- Overview of cricket data
- Key statistics and KPIs
- Top run scorers
- Top wicket takers
- Match statistics
- Interactive visualizations

### 🏏 Live Matches
- Fetches live cricket matches using the Cricbuzz API
- Displays teams, match format, venue, and status
- Allows scorecard data to be fetched and stored

### 📊 Top Statistics
- Total players
- Total teams
- Batting records
- Bowling records
- Top run scorers
- Top wicket takers
- Highest individual scores

### 🗄️ SQL Analytics

The project contains 20 SQL analytics queries covering:

- Filtering
- Sorting
- Aggregations
- GROUP BY
- HAVING
- JOINs
- Subqueries
- Player statistics
- Team performance
- Match analysis
- Bowling analysis

### ✏️ CRUD Operations

The application supports CRUD operations for team records:

- Create a team
- Read team records
- Update team information
- Delete a team

## Technology Stack

- Python
- SQL
- SQLite
- Streamlit
- Pandas
- Requests
- Plotly
- python-dotenv
- REST API

## Project Structure

```text
cricbuzz_livestats/
│
├── notebooks/
│   └── data_fetching.ipynb
│
├── pages/
│   ├── crud_operations.py
│   ├── home.py
│   ├── live_matches.py
│   ├── sql_queries.py
│   └── top_stats.py
│
├── services/
│   ├── match_service.py
│   ├── database_service.py
│   └── scorecard_service.py
│
├── utils/
│   ├── api.py
│   └── db_connection.py
│
├── app.py
├── create_database.py
├── insert_sample_data.py
├── cricbuzz_livestats.db
├── requirements.txt
└── README.md