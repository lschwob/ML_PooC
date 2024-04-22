# Finding the best investments - Trading

## Overview
In our project, we decided to simulate a portfolio (its creation is explained in the following sections ( ## Data collection & ## Our data)).
Based on the portfolio we have created, we are looking for pairs of stocks.
We will therefore study the correlations between them, using different models.
The ultimate aim is to help us select our future shares and sell the most expensive and buy the cheapest.

## Data collection
- Scraping the list of S&P 500 companies: We start by obtaining the complete list of companies making up the index, which forms the basis for the following scraping steps.
- Extract historical data: For each company, we retrieve the historical data available by scraping Yahoo Finance.
- Saving the data: Each data set will be saved in a CSV file to facilitate subsequent analyses.

## Our data
We have 500 csvs: each csv corresponds to the history of the 500 companies in the S&P 500.
Each csv contains the following columns:
- Date (day)
- Opening price
- Highest price of the day
- Lowest price of the day
- Closing price
- Adjusted closing price
- Volume of shares traded
These data are extracted for each available trading day and are structured into corresponding columns in a CSV file.

## Data cleaning
The data is already clean, so no cleaning is required.
______________________________________________________________________________








Corrélation à un instant t : si ensuite l'une est haute par rapport à l'autre, on la vend et on achète l'autre
## Features
- Feature 1: Describe the feature and its benefit.
- Feature 2: Highlight another feature and why it's useful
- Feature 3: If applicable, describe another key aspect of the project.

## Installation
Provide step-by-step instructions on how to get a development environment running.

```bash
git clone https://github.com/username/projectname.git
cd projectname
pip install -r requirements.txt


## Drive Folder :
https://drive.google.com/drive/folders/1jBxBjaKs8gJVh0EJ15seDMgjDhoDkbpm?usp=sharing