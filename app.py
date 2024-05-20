import threading
import pandas as pd
import amoeba_model
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend


app = Flask(__name__)

model = None


class CustomScript(VisualizationElement):
    """
    A custom visualization element that includes a custom script for the Mesa server.

    Attributes:
        local_includes (list): List of local script files to include.
    """
    local_includes = ["static/custom_script.js"]

    def __init__(self):
        """
        Initialize the CustomScript visualization element.
        """        
        pass

    def render(self, model):
        """
        Render method to comply with VisualizationElement requirements.
        
        Args:
            model (Model): The model instance being visualized.
        
        Returns:
            str: Empty string as this custom element does not need to render anything directly.
        """        
        return ""


@app.route('/')
def index():
    """
    Render the main index page.

    Returns:
        str: Rendered HTML of the index page.
    """    
    return render_template('index.html')


@app.route('/init', methods=['POST'])
def initialize():
    """
    Initialize the model with the given month from the POST request.

    Returns:
        json: JSON response indicating success or failure.
    """    
    global model
    width = 10
    height = 10
    month = int(request.json.get('month', 1))
    model = amoeba_model.AmoebaDivisionModel(width, height, month)
    return jsonify({'message': 'Model initialized with month: {}'.format(month)})


@app.route('/run', methods=['POST'])
def run():
    """
    Run the simulation for the specified number of steps.

    Returns:
        json: JSON response containing the DataFrame and graph image.
    """    
    global model
    steps = int(request.json.get('steps', 1))
    if model is not None:
        amoeba_model.run_simulation(model, steps)
        df = pd.DataFrame(model.data_collector)

        # Get the base64 image
        image_base64 = amoeba_model.visualize_environment(model.data_collector)

        # Send both the DataFrame and the image as JSON
        response = {
            'graph': image_base64,
            'dataframe': df.to_dict(orient='records')

        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Model is not initialized'}), 400


def run_mesa(month):
    """
    Run the Mesa server with the given initial month.

    Args:
        month (int): The initial month for the model.
    """    
    grid = amoeba_model.CanvasGrid(
        amoeba_model.agent_portrayal, 10, 10, 400, 400)
    server = ModularServer(amoeba_model.AmoebaDivisionModel,
                           [grid, CustomScript()],
                           "Amoeba Division Model",
                           {"width": 10, "height": 10, "month": month})
    server.description = ("This is the Amoeba Division Model. It simulates the lifecycle of amoebas in a grid "
                          "environment, showing how different states affect their survival and reproduction. "
                          "Each color in the grid represents a different state of the amoeba, providing a visual "
                          "representation of the population dynamics over time.")
    server.port = 8521  # Set Mesa server on a different port
    server.launch()


@app.route('/start_mesa', methods=['POST'])
def start_mesa():
    """
    Start the Mesa server in a separate thread.

    Returns:
        json: JSON response indicating the server is starting.
    """    
    # Get month from POST data, default to 1
    month = int(request.form.get('month', 1))
    thread = threading.Thread(target=run_mesa, args=(month,))
    thread.daemon = True
    thread.start()
    return jsonify({"message": "Mesa server is starting with month " + str(month) + "..."}), 200


if __name__ == '__main__':
    app.run(debug=True)
