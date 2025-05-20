# NBA Player and Team Analysis Dashboard

This project is a Streamlit application that displays NBA player and team statistics, allowing users to analyze and compare various performance metrics.

## Features

*   **Team Ratings:** Displays a sortable list of all NBA teams with their Offensive Rating, Defensive Rating, and Net Rating.
*   **Team-Specific Player Ratings:** Allows users to select an NBA team and view the ratings (Offensive, Defensive, Net) and Games Played (GP) for all players on that team.
*   **Player Search:** Provides up to five input fields to search for specific players by name across the league and displays their ratings.
*   **All Player Ratings:** Shows a sortable list of all players in the league (who have played a minimum number of games) with their Offensive Rating, Defensive Rating, and Net Rating.

## How to Run

1.  Ensure you have Python and pip installed.
2.  Install Streamlit and other dependencies:
    ```bash
    pip install streamlit pandas nba_api
    ```
3.  Navigate to the project's root directory in your terminal.
4.  Run the application:
    ```bash
    streamlit run main.py
    ```

## Data Source

The application fetches NBA statistics using the [nba_api](https://github.com/swar/nba_api) Python library, which interfaces with stats.nba.com.
