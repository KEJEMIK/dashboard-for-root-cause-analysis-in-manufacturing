# Dashboard for Root Cause Analysis in Manufacturing

Prototypical implementation for the submission: Kacper Mucha, Kristof Böhmer and Maria Leitner: Dashboard for Root Cause Analysis in Manufacturing.

This repository presents a prototype of a dashboard designed for root cause analysis in manufacturing processes. The dashboard aims to provide insights into the factors influencing production efficiency and to aid in identifying the root causes of detected anomalies. It contains methods to extract Footprints from the production log, calculate the Footprint KPIs and aggregate them. Based on these calculations, the visualization techniques have been implemented to highlight detected anomalies. Currently the repository provides Directly Follows Graph and Scatter Plot visualization capabilities. The dashboard is made interactive by utilizing Mercury Framework, which converts the Jupyter Notebook into a Web Application.

## Repository Structure

The repository is structured as follows:

- **`data/`**: Contains the data files.
    - **`test_data.csv`**: Randomly generated production data in .csv format.
- **`src/`**: Contains the source code files.
  - **`data_importer.py`**: Functions for processing and filtering data.
  - **`footprint_analyzer.py`**: Functions for analyzing footprints and calculating Key Performance Indicators (KPIs). Additionally provides functionality of drawing plots related to footprint analysis.
  - **`graphviz_helper.py`**: Helper functions for working with Graphviz objects.
  - **`kpi_dashboard.ipynb`**: Jupyter Notebook where the dashboard has been programmed. It is convertible to web application using Mercury Framework. 
- **`README.md`**: This file, providing an overview of the project and its structure.
- **`requirements.txt`**: List of python libraries required to run the project.

## Usage

To start a dashboard, please follow these steps:

1. Open the command line and navigate to the project repository.

2. Activate the Conda Environment using the following command:

    ```bash
    conda activate <your_environment_name>
    ```

3. Install the required Python packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

4. After successfully preparing the Python environment, navigate to the src folder.

5. Run the dashboard using the following command:

    ```bash
    mercury run
    ```

6. The dashboard should open automatically, running on localhost:8000.