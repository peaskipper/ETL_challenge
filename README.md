# ETL_challenge
The Challenge: Data Warehouse and Data Pipeline
This repository contains an end-to-end ETL pipeline that ingests, validates, transforms, and aggregates raw data files into a structured, query-ready format using Databricks.
It also includes tools for visualizing and analyzing the data model.

🧱 Architecture Overview

![alt text](https://github.com/peaskipper/ETL_challenge/blob/develop/ETL%20challenge.jpg)

The pipeline is composed of the following stages:

📥 Ingestion

Raw pipe-delimited .gz files are read using pandas, parsed, and stored in ADLS.
External Unity Catalog (UC) tables are created with metadata and constraints.

✅ Validation

Non-null, data type, primary key uniqueness, and foreign key relationship checks.

📐 Normalization

Hierarchy tables split into multiple normalized levels.
SQL file organises normalized table creation using logical mapping.

📊 Aggregation (WIP)

Aggregates facts by dimensions using PySpark SQL and DLT pipelines.
Watermarking ensures incremental fault-tolerant processing.

📈 Visualization

Inferred schema exported to .puml using uml_writer.py.
ER diagram rendered and saved as .png.

📁 Repository Structure
ETL_challenge/
├── migration_library/           # Core library for parsing and ER diagram generation
│   ├── ingest.py                # Reads and processes raw gz files into dataframes
│   ├── analyse.py               # Extracts relationships, infers PK/FK
│   ├── uml_writer.py            # Generates PlantUML format from schema
│   └── main.py                  # Orchestrates the extraction and parsing on local
│
├── pipeline_notebooks/         # Databricks PySpark notebooks
│   ├── data_ingestion.ipynb    # Writes raw files to Unity Catalog (external tables)
│   ├── data_validation.ipynb   # Data quality checks: PK, FK, nulls, type mismatches
│   ├── data_staging.ipynb      # Normalizes hierarchy into separate tables
│   ├── data_transformation.ipynb   # Basic transformations, joins
│   ├── create_aggregate.ipynb      # Aggregation logic using SQL
│   ├── data_aggregation_dlt.ipynb  # DLT-based implementation (with watermarking)
│   └── secret_scope.py             # Placeholder file for storing environment variables
│
├── sql_files_normalised/       # Contains SQL scripts to split hierarchies into normalised dims
│   ├── dim_cat.sql
│   ├── dim_subcat.sql
│   ├── ...
│
├── output_obj/
│   ├── ER_diagram.puml         # PlantUML source file
│   ├── ERD.png                 # Generated ER diagram
│   └── tbl_metadata.json       # Inferred table + column metadata
│
├── source_data/                # Contains sample or placeholder gzipped input files
│
├── databricks_workflow.yaml    # Workflow YAML for Databricks job orchestration
├── README.md                   # You're here!
└── ...


🚀 How to Run

1. For data ingestion and puml render on local machine, run: `ETL_challenge/migration_library/main.py`
2. For end-to-end pipeline: Set up databricks workflow using `ETL_challenge/databricks_workflow.yaml` and configure write locations

Prerequisite: Access to a Databricks workspace with Unity Catalog & ADLS mount

📦 Local (Setup and ER Diagram)

# Install dependencies
pip install pandas plantuml-markdown

## installations

pip install pandas  
pip install gzip
pip install graphviz
pip install pythonplantuml
pip install pyspark

## downloads
### for ER visualisation
[plantUML](https://plantuml.com/download) - standalone JAR
[java](https://www.oracle.com/java/technologies/downloads/#jdk24-windows) - prerequisite for plantUML
[puml vsc extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) - for reading .puml file

## docker setup to run notebooks(pyspark, hadoop) on local 
1. Run docker
2. Use command to run pyspark on docker docker: `pull jupyter/all-spark-notebook`
3. Run docker image with this command docker: `run -it --rm -p 8888:8888 -v /path/to/your/notebooks:/home/jovyan/work jupyter/all-spark-notebook`
4. Retrieve/Update variables in notebook to point to your azure blob storage

## Set up databricks workflow using pipeline_notebooks/databricks_workflow.yaml
databricks jobs import --yaml-file databricks_workflow.yaml

📌 Highlights

📚 Modular design using functional libraries + parameterized notebooks
🔍 Automated metadata inference + schema validation
📊 Auto-generated ERD using PlantUML

📝 Limitations

The current implementation assumes no live access to a Databricks workspace.
All Spark operations are developed and tested locally using mocks or PySpark local mode.

📌 Future Scope

Implement SCD Type 2 logic for slowly changing dimensions.
Integrate full CI/CD with GitHub Actions and Databricks CLI.
Extend to support Change Data Capture for near-real-time loads.

