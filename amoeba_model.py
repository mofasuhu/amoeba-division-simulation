import warnings
from io import BytesIO
import base64
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa import Agent, Model
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class Amoeba(Agent):
    """
    An agent representing an amoeba in the simulation.
    
    Attributes:
        state (str): Current state of the amoeba (e.g., intact, encysted).
        dividing_next_step (bool): Flag to indicate if the amoeba is in the process of division.
    """    
    def __init__(self, unique_id, model):
        """
        Initialize an Amoeba agent.
        
        Args:
            unique_id (int): Unique identifier for the agent.
            model (Model): The model instance this agent belongs to.
        """        
        super().__init__(unique_id, model)
        self.state = 'intact'  # initial state
        self.dividing_next_step = False  # Flag to delay division completion

    def step(self):
        """
        The step function for the agent, called at each time step.
        Handles state transitions based on environmental conditions.
        """
        if self.model.environment.is_encystment_condition():
            self.state = 'encysted'
        elif self.model.environment.is_excystment_condition() and self.state == 'encysted':
            self.state = 'excysted'

        # Handle division process
        if self.state == 'excysted' or self.model.environment.is_div_condition() or self.dividing_next_step:
            self.divide_if_possible()

    def divide_if_possible(self):
        """
        Handle the division process of the amoeba.
        """        
        if self.dividing_next_step:
            # Attempt to complete the division
            if self.model.grid.is_cell_empty(self.new_position):
                self.model.grid.place_agent(self.new_amoeba, self.new_position)
                self.model.schedule.add(self.new_amoeba)
                self.new_amoeba.state = 'intact'
                self.state = 'divided'
            else:
                self.state = 'stressed'  # Space no longer empty, cannot divide
            self.dividing_next_step = False
        elif self.model.environment.is_div_condition():
            x, y = self.pos
            new_positions = self.model.grid.get_neighborhood(
                (x, y), moore=True, include_center=False)
            empty_positions = [
                pos for pos in new_positions if self.model.grid.is_cell_empty(pos)]
            if empty_positions:
                self.state = 'dividing'
                self.new_position = self.random.choice(empty_positions)
                self.new_amoeba = Amoeba(self.model.next_id(), self.model)
                self.dividing_next_step = True
            else:
                self.state = 'stressed'


class Environment:
    """
    Class representing the environment in the simulation.
    
    Attributes:
        month (int): Current month of the simulation.
        water_quality (int): Current water quality.
        temperature (int): Current temperature.
        temperature_description (str): Description of the current temperature (e.g., sub-zero).
    """
    def __init__(self, month):
        """
        Initialize the environment with the given month.
        
        Args:
            month (int): The initial month (1-12).
        """
        self.month = month
        self.update_conditions()

    def update_conditions(self):
        """
        Update the environmental conditions (water quality and temperature).
        """
        self.adjust_water_quality()
        self.adjust_temperature()

    def adjust_water_quality(self):
        """
        Adjust water quality based on the current month.
        """        
        # Water quality varies significantly with seasons
        if self.month in [12, 1, 2]:  # Winter months
            self.water_quality = np.random.randint(
                0, 50)  # Lower quality in winter
        elif self.month in [6, 7, 8]:  # Summer months
            self.water_quality = np.random.randint(
                50, 100)  # Higher quality in summer
        else:  # Spring and Autumn
            self.water_quality = np.random.randint(75, 100)  # Optimal quality

    def adjust_temperature(self):
        """
        Adjust temperature based on the current month.
        """        
        if self.month in [12, 1, 2]:
            # Example numeric value for sub-zero
            self.temperature = np.random.randint(-20, 10)
            self.temperature_description = "sub-zero"
        elif self.month in [6, 7, 8]:
            # Example numeric value for extreme hot
            self.temperature = np.random.randint(30, 60)
            self.temperature_description = "extreme hot"
        else:
            # Example numeric value for normal
            self.temperature = np.random.randint(15, 25)
            self.temperature_description = "normal"

    def is_encystment_condition(self):
        """
        Determine if conditions are suitable for encystment.
        
        Returns:
            bool: True if conditions are suitable for encystment, False otherwise.
        """        
        return self.water_quality < 50 or self.temperature_description in ["sub-zero", "extreme hot"]

    def is_excystment_condition(self):
        """
        Determine if conditions are suitable for excystment.
        
        Returns:
            bool: True if conditions are suitable for excystment, False otherwise.
        """        
        return self.water_quality >= 50 and self.temperature_description == "normal"

    def is_div_condition(self):
        """
        Determine if conditions are suitable for division.
        
        Returns:
            bool: True if conditions are suitable for division, False otherwise.
        """        
        return self.water_quality >= 50 and self.temperature_description == "normal"

    def increment_month(self):
        """
        Increment the month, looping back to January after December.
        """        
        self.month = 1 if self.month == 12 else self.month + 1


def collect_data(model):
    """
    Collect data from the model at the current step.
    
    Args:
        model (AmoebaDivisionModel): The model instance to collect data from.
    
    Returns:
        dict: A dictionary containing the collected data.
    """    
    data = {
        'step': model.schedule.steps,
        'intact': sum(1 for a in model.schedule.agents if a.state == 'intact'),
        'dividing': sum(1 for a in model.schedule.agents if a.state == 'dividing'),
        'divided': sum(1 for a in model.schedule.agents if a.state == 'divided'),
        'encysted': sum(1 for a in model.schedule.agents if a.state == 'encysted'),
        'excysted': sum(1 for a in model.schedule.agents if a.state == 'excysted'),
        'stressed': sum(1 for a in model.schedule.agents if a.state == 'stressed'),
        'water_quality': model.environment.water_quality,
        'temperature': model.environment.temperature,
        'month': model.environment.month
    }
    return data


class AmoebaDivisionModel(Model):
    """
    The main model for the amoeba division simulation.
    
    Attributes:
        grid (SingleGrid): The grid where agents are placed.
        schedule (RandomActivation): The scheduler to manage agent activation.
        environment (Environment): The environment of the simulation.
        data_collector (list): List to store data collected at each step.
    """
    def __init__(self, width, height, month):
        """
        Initialize the model with the given parameters.
        
        Args:
            width (int): The width of the grid.
            height (int): The height of the grid.
            month (int): The initial month (1-12).
        """
        super().__init__()
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.environment = Environment(month)
        self.data_collector = []  # List to store data from each step

        # Initial amoeba placement
        amoeba = Amoeba(1, self)
        self.grid.place_agent(amoeba, (np.random.randint(
            1, width), np.random.randint(1, height)))
        self.schedule.add(amoeba)

    def step(self):
        """
        Advance the model by one step.
        """        
        self.schedule.step()
        self.environment.update_conditions()
        self.environment.increment_month()  # To cycle through seasonal changes

        # Collect and store data at the current step
        current_data = collect_data(self)
        self.data_collector.append(current_data)


def agent_portrayal(agent):
    """
    Define the portrayal of agents for visualization.
    
    Args:
        agent (Amoeba): The agent to portray.
    
    Returns:
        dict: A dictionary defining the agent's portrayal.
    """    
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Layer": 0, "w": 1, "h": 1}

    color_map = {
        'intact': 'green',
        'encysted': 'blue',
        'excysted': 'lightblue',
        'divided': 'red',
        'stressed': 'orange',
        'dividing': 'yellow'
    }
    portrayal["Color"] = color_map.get(agent.state, 'grey')
    return portrayal


# Setup the grid for visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


def visualize_environment(data_collector):
    """
    Visualize the environmental conditions over time.
    
    Args:
        data_collector (list): List of collected data.
    
    Returns:
        str: Base64 encoded image of the visualization.
    """    
    # Convert the list of dictionaries to a DataFrame for easier plotting
    data = pd.DataFrame(data_collector)

    # Plotting the environmental conditions over time
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=data, x='step', y='water_quality', label='Water Quality')
    sns.lineplot(data=data, x='step', y='temperature', label='Temperature', estimator=None)
    plt.title('Environmental Conditions Over Time')
    plt.xlabel('Simulation Step')
    plt.ylabel('Condition Value')
    plt.legend()

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Close the plot to release resources
    buf.seek(0)
    # Encode the image to base64 string
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64


def run_simulation(model, steps):
    """
    Run the simulation for a given number of steps.
    
    Args:
        model (AmoebaDivisionModel): The model instance to run.
        steps (int): The number of steps to run the simulation.
    """    
    for _ in range(steps):  # Use the steps provided by the user
        model.step()


def reset_model(width, height):
    """
    Reset the model with a new initial month.
    
    Args:
        width (int): The width of the grid.
        height (int): The height of the grid.
    
    Returns:
        AmoebaDivisionModel: A new model instance with the specified parameters.
    """    
    new_month = int(input("Enter the new month (1-12) for the model reset: "))
    new_month = max(1, min(12, new_month))
    return AmoebaDivisionModel(width, height, new_month)


def main():
    """
    Main function to run the simulation interactively.
    """    
    initial_month = int(input("Enter the initial month (1-12): "))
    simulation_steps = int(input("Enter the number of simulation steps: "))

    initial_month = max(1, min(12, initial_month))

    model = AmoebaDivisionModel(width=10, height=10, month=initial_month)
    run_simulation(model, simulation_steps)
    visualize_environment(model.data_collector)

    # Ask if the user wants to reset the model
    while input("Do you want to reset the model? (yes/no): ").lower() == 'yes':
        model = reset_model(10, 10)  # Reset model with new month
        simulation_steps = int(input("Enter the number of simulation steps: "))
        run_simulation(model, simulation_steps)
        visualize_environment(model.data_collector)
