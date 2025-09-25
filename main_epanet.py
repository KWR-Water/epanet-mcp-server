"""
FastMCP Movie Database Server

A Model Context Protocol server for retrieving movie data from MongoDB.
Compatible with Claude Desktop and other MCP clients.

To run:
    uv run server movie_server stdio

Environment Variables:
    MONGODB_URI: MongoDB connection string (default: mongodb://localhost:27017)
    DATABASE_NAME: Database name (default: moviedb)
    COLLECTION_NAME: Collection name (default: movies)
"""

import os
from mcp.server.fastmcp import FastMCP
from epyt import epanet


# Create MCP server
mcp = FastMCP("Movie Database Server")





##################################################EPANET#####################################################

@mcp.resource("files://models/inp_files")
def get_inp_files() -> str:
    """Checks the 'models' folder and returns a list of all .inp files."""
    try:
        folder_path = "C:/Users/xrism/Documents/GitHub/MCP-Server-Exmample/models"

        # Check if the folder exists
        if not os.path.isdir(folder_path):
            return f"Error: The folder '{folder_path}' does not exist."

        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Filter for files ending with .inp
        inp_files = [file for file in all_files if file.endswith(".inp")]

        if not inp_files:
            return "No .inp files found in the 'models' folder."

        # Format the list for display
        result = "List of .inp files in the 'models' folder:\n\n"
        for i, file in enumerate(inp_files, 1):
            result += f"{i}. {file}\n"

        return result

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def run_epanet_simulation(file_name: str) -> str:
    """
    Runs an EPANET simulation on a specified .inp file and returns the results.
   
    Args:
        file_name (str): The name of the .inp file to simulate.
                         This file must be located in the 'models' directory.
   
    Returns:
        str: A message indicating the success or failure of the simulation,
             along with simulation time, number of nodes, and number of pipes.
    """
   

    # ==========================
   
    try:
        
       
        # Check if the file exists
        if not os.path.exists("models/"+file_name):
            return f"Error: The file '{file_name}' does not exist in the 'models' folder."
           
        # Create a WaterNetworkModel object
        network = epanet("models/"+file_name, display_msg=False, display_warnings=False)
        network.setDemandModel("DDA",0,0,0)
       
        # Measure simulation time
        import time
        start_time = time.time()
        
        # Create a simulator and run the simulation
        results = network.getComputedHydraulicTimeSeries()
        
        # Calculate simulation time
        simulation_time = time.time() - start_time
        
        # Get network statistics

        num_nodes = network.getNodeJunctionCount()
        num_pipes = len(network.getLinkIndex())
       
        return (f"Simulation of '{file_name}' completed successfully.\n"
                f"Simulation time: {simulation_time:.3f} seconds\n"
                f"The model has {num_nodes} nodes and {num_pipes} pipes.")
                
    except Exception as e:
        return f"Error during simulation: {str(e)}"
    



if __name__ == "__main__":
    import asyncio
    mcp.run()