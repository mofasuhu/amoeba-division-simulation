# Amoeba Division Simulation

This project simulates the lifecycle of amoebas in a grid environment, showing how different states affect their survival and reproduction. The simulation includes a web interface for user interaction and a Python backend for simulation logic. 

## Features

- **Amoeba Lifecycle Simulation**: Models the states of amoebas (intact, encysted, excysted, divided, stressed, dividing) in a grid environment.
- **Dynamic Environmental Conditions**: Simulates changes in water quality and temperature based on the month.
- **Visualization**: Provides graphical representation of amoeba states and environmental conditions over time.
- **Interactive Web Interface**: Allows users to initialize the model, run simulations, and view results.

## Technologies Used

- **Python**: Backend simulation logic.
- **Flask**: Web framework for the backend.
- **JavaScript**: For client-side interactions and AJAX requests.
- **jQuery**: Simplified JavaScript interactions.
- **Matplotlib and Seaborn**: For plotting and visualizing data.
- **Mesa**: Agent-based modeling framework.
- **HTML/CSS**: For structuring and styling the web interface.

## Project Structure

```plaintext
.
├── amoeba_model.py         # Contains the core simulation logic
├── app.py                  # Flask application to run the simulation server
├── static
│   └── custom_script.js    # Custom JavaScript for client-side functionality
├── templates
│   └── index.html          # Main HTML file for the web interface
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/amoeba-division-simulation.git
    cd amoeba-division-simulation
    ```

2. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Simulation

1. **Start the Flask server:**
    ```sh
    python app.py
    ```

2. **Open your web browser and navigate to:**
    ```
    http://127.0.0.1:5000
    ```

3. **Initialize the Model:**
    - Enter the initial month (1-12) and click "Initialize Model".

4. **Run the Simulation:**
    - Enter the number of simulation steps and click "Run Simulation".
    - View the results (graph and table) on the web page.

5. **Start Mesa Server (Optional):**
    - Enter the initial month (1-12) for Mesa and click "Run Mesa".
    - This will start the Mesa server on port 8521 for further visualizations.

## Code Overview

### `amoeba_model.py`

- **Amoeba Class**: Represents an amoeba with different lifecycle states.
- **Environment Class**: Manages environmental conditions like water quality and temperature.
- **AmoebaDivisionModel Class**: The main model handling the simulation.
- **Visualization Functions**: Functions to visualize the simulation data.

### `app.py`

- **Flask Routes**:
  - `/`: Renders the main index page.
  - `/init`: Initializes the model.
  - `/run`: Runs the simulation for a specified number of steps.
  - `/start_mesa`: Starts the Mesa server in a separate thread.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The [Mesa framework](https://mesa.readthedocs.io/en/stable/) for agent-based modeling.
- [Flask](https://flask.palletsprojects.com/) for providing a lightweight WSGI web application framework.
- [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/) for data visualization.
