# **Stocks ETL Pipeline**

*A modular, configurable and production-ready ETL pipeline for daily stock prices using the SimFin API.*

---

## **1. Project Overview**

This project is an end-to-end **ETL pipeline** designed to extract, transform and load **daily stock price data** for a configurable list of companies using the **SimFin API**.

The main goal of this first release is to provide a **fully functional and reproducible pipeline** that:

* Is executed via CLI with:

  ```bash
  python -m src.main
  ```
* Automatically retrieves **yesterday’s stock prices** (to ensure SimFin data availability).
* Outputs a clean, structured CSV file stored under `/data/processed/`.
* Follows **clean code, modularity, configuration management, logging, testing and documentation** best practices.

Later releases will evolve this project into a full **Data Engineering workflow** using:

* **Apache Airflow**
* **Docker**
* **PostgreSQL**
* **Power BI**

---

## **2. Objectives**

### **Release 1 (Current)**

* CLI-based modular ETL
* Config-driven extraction
* Load data to CSV
* Logging & error handling
* Clean architecture following DE/MLOps standards
* Dependencies managed through `environment.yml`

### **Release 2 (Future Roadmap)**

* Airflow DAG
* Dockerized execution
* PostgreSQL warehouse
* Power BI dashboards
* Monitoring & alerting

---

## **3. Repository Structure**

```
STOCKS_ETL/
│
├── data/
│   ├── processed/
│   └── raw/
├── logs/
├── src/
│   ├── extract/
│   ├── transform/
│   └── load/
├── .env
├── config.yaml
├── .gitignore
├── environment.yml
└── README.md
```

This structure reflects a **clean separation of concerns**, ideal for professional ETL pipelines.

---

## **4. How It Works**

### **Extraction**

`extract` module connects to the SimFin API using credentials in `.env` and tickers in `config.yaml`.

### **Transformation**

`transform` module cleans and formats yesterday’s stock price data.

### **Load**

`load` module writes the final dataset to `/data/processed/output.csv`.

### **Pipeline Execution**

```bash
python -m src.main
```

---

## **5. Configuration**

Controlled via `config.yaml`, including:

* Stock tickers
* Output file paths
* Logging level

Secrets (API key) must be placed in `.env`:

```
SIMFIN_API_KEY=your_api_key_here
```

---

## **6. Testing (Future Release)**

Planned:

* Unit tests for ETL modules
* CI workflow with linting + pytest

---

## **7. Future Expansions**

* Airflow orchestration
* Docker containers
* PostgreSQL warehouse design
* Power BI visual dashboards

---

## **8. Installation**

```bash
git clone https://github.com/your_username/stocks_etl
cd stocks_etl
conda env create -f environment.yml
conda activate stocks_etl
python -m src.main
```

---

## **9. Lessons & Skills Demonstrated**

* ETL architecture
* Clean Python modularization
* API integration
* Logging & error handling
* Config-based pipelines
* Reproducible environments
* MLOps & DevOps mindset

---

## **10. License**

MIT License
