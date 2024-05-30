from database import DatabaseConnection

# Create an instance of DatabaseConnection
db = DatabaseConnection("chat_history.db")


# Define your get_level_leaderboard function
def get_level_leaderboard():
    query = """
        SELECT discord_id, level
        FROM players
        ORDER BY level DESC
        LIMIT 10
    """
    # Remove the db.close() line from here
    leaderboard_data = db.fetchall(query)
    return leaderboard_data


# Use the function
leaderboard_data = get_level_leaderboard()


