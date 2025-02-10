from nicegui import ui
import requests

def get_top_team_name(league_id: str) -> str:
    """
    Fetch the standings for the given FPL classic league ID and return the name of the top team.
    
    Parameters:
        league_id (str): The league ID to query.
        
    Returns:
        str: The name of the top team, or an error message if something goes wrong.
    """
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        return f"Error fetching data: {e}"
    
    try:
        data = response.json()
        results = data["standings"]["results"]
        if not results:
            return "No teams found in this league."
        top_team = results[0]
        return top_team.get("entry_name", "Unknown Team")
    except (KeyError, ValueError) as e:
        return f"Error processing JSON data: {e}"

def fetch_and_display_team():
    league_id = league_id_input.value.strip()
    if not league_id:
        result_label.set_text("Please enter a league id.")
        return

    top_team = get_top_team_name(league_id)
    result_label.set_text(f"Top team in the league: {top_team}")

# Create UI elements
ui.markdown("# FPL Top Team Finder")
ui.markdown("Enter your FPL classic league ID below and click the button to see the top team:")

with ui.row().classes("items-center gap-4"):
    league_id_input = ui.input(label="League ID", placeholder="e.g., 123456")
    ui.button("Get Top Team", on_click=fetch_and_display_team)

result_label = ui.label("")

# Run the NiceGUI app
ui.run()
