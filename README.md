# Movie Recommendation System

## Introduction

This project is a movie recommendation system using the MovieLens dataset. It employs advanced recommendation models and features a Streamlit-based dashboard for users to explore personalized movie recommendations and item similarities.

## Project Structure


- **data**: Dataset files.
- **notebooks**: Jupyter Notebooks for model training.
- **scripts**: Python scripts for the Streamlit dashboard.
- **README.md**: Project documentation.
- **requirements.txt**: Python package requirements.

## User Interface Components

### User Page

- **User Selection**: Dropdown to select users.
- **User History**: Displays user interactions.
- **Top-N Recommendations**: List of top-N items recommended for the user.
- **Navigation**: Navigate through recommendations.

### Item Page

- **Item Selection**: Dropdown to select items.
- **Item Profile**: Displays item metadata.
- **Top-N Similar Items**: List of top-N similar items.
- **Navigation**: Navigate through similar items.

## Recommender Models

- **User Recommender**: Factorization Machines, Neural Collaborative Filtering, etc.
- **Item Similarity**: Calculated on demand when an item is selected.

## Dependencies
_ all required packages in `requirements.txt` please run this : 
```bash
pip install -r requirements.txt
```


