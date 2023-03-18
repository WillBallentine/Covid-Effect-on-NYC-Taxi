# Covid-Effect-on-NYC-Taxi

## ABOUT

This project sets out to analyze the effect Covid-19 had on the Taxi industry in New York City, New York.

Covid-19 had tremendous impact on every aspect of society and much of the restrictions that were put into place directly impacted the way Taxis could operate.

**This project will attempt to answer the following questions:**

- Did the average passenger count go up or down during the pandemic compared to years before 2020.
- Did the way people paid for rides change during and after the pandemic?
- How did the pandemic affect the average trip distance?
- Was tipping affected by the pandemic?

## Methodology

- Taxi Data was taken from the NYC Taxi & Limousine Commission[^1]
- Covid Data was taken from the CDC [^2]

## How To use this Repo

Start by cloning this repository to your local machine.

This repo utilizes several libraries that are included in the requirements.txt file.

To install these, navigate to the cloned repo folder on your machine in the terminal and run:

    pip install -r requirements.txt

If this gives you any trouble I have also listed the libraries below for individual install:

- Pandas
- Numpy
- Matplotlib
- Geopandas
- Folium
- Glob
- Pyarrow
- ipykernel

I have included a sample data set called `sample.csv` if you would like to use that. If you do, you will need to change the file name in `taxi.ipynb` in the second code block to `assets/sample.csv` for the script to work. Otherwise, you will need to download the montly Parquet files from the linked NYC Gov site[^1] and use the `taxi_csv_create.ipynb` file to collect a larger dataset.

The main file in this project is called `taxi.ipynb` and contains the analysis portion of this project.

#### Running the Program in Jupyter Notebook

1. Clone the repository.
2. Save the folder.
3. Open `jupyter notebook` from command line or start menu.
4. Navigate to the saved location of the repo.
5. Open `taxi.ipynb`.
6. Click `Cell` tab and then `Run All`.

#### Running the Program in Python

1. Clone the repository
2. Save the folder.
3. Open the saved repository in your IDE or terminal.
4. Run the `taxi.py` file.

Citations:

[^1]:
    [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
    .

[^2]:
    [United States COVID-19 Cases and Deaths by State over Time](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36)
    .

[^3]: [Covid-19 Timeline](https://www.cdc.gov/museum/timeline/covid19.html)

---
