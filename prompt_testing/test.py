import ast

notepad = "{'functions': 'ticket_availability, parking_recommendation', 'user_requests': '- Are there any tickets left for the opening speech tonight? And can I park by the castle?\\n'}"



parsed = ast.literal_eval(notepad)

print(parsed['user_requests'])