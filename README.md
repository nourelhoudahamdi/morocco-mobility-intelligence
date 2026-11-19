# Morocco Mobility Intelligence (MMI)

## Overview

Morocco Mobility Intelligence is a Data Engineering project designed to collect, process, store, and analyze mobility-related data in Morocco.

The project aims to combine weather and traffic data to better understand mobility patterns and explore how environmental conditions can influence transportation.

## Problem Statement

Mobility in Moroccan cities faces several challenges, including traffic congestion, unpredictable travel conditions, and difficulties in understanding transportation patterns.

Data can help transform these challenges into measurable insights.

## Project Objectives

- Collect weather data from external APIs.
- Collect traffic data from available data sources.
- Build an automated data ingestion pipeline.
- Store structured data in PostgreSQL.
- Clean and transform data using Python and Pandas.
- Process larger datasets using Apache Spark.
- Design a Data Warehouse.
- Analyze mobility patterns using SQL.
- Build interactive dashboards with Power BI.

## Data Pipeline Architecture

   text
External Data Sources
       |
       v
   Data Ingestion
   (Python + APIs)
       |
       v
   Data Storage
   (PostgreSQL)
       |
       v
 Data Processing
 (Python + Pandas)
       |
       v
 Big Data Processing
      (Spark)
       |
       v
   Data Warehouse
   (PostgreSQL + SQL)
       |
       v
    Analytics
       |
       v
    Power BI


## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data collection and processing |
| APIs | External data collection |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Data storage |
| Apache Spark | Large-scale data processing |
| SQL | Data analysis and warehouse queries |
| Power BI | Data visualization |
| Git & GitHub | Version control and project management |

## Project Structure

   text
morocco-mobility-intelligence/
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
├── src/
│   ├── ingestion/
│   ├── processing/
│   └── analytics/
├── tests/
├── config/
├── notebooks/
├── sql/
├── dashboards/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md


## Project Status

Currently in the initial development phase.

The project will be developed progressively, starting with data collection and ending with analytics and visualization.

## Future Goals

- Expand data coverage across Moroccan cities.
- Explore relationships between weather conditions and traffic.
- Identify mobility trends and patterns.
- Develop useful insights to support transportation planning.

---

**Author:** Nour El Houda HAMDI

**Project:** Morocco Mobility Intelligence