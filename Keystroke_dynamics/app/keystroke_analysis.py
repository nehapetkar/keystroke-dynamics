# keystroke_analysis.py

def calculate_dwell_time(keystrokes):
    # Calculate dwell time (time between key press and release)
    dwell_times = []
    for i in range(len(keystrokes) - 1):
        if keystrokes[i]['event'] == 'p' and keystrokes[i + 1]['event'] == 'r':
            dwell_time = keystrokes[i + 1]['time'] - keystrokes[i]['time']
            dwell_times.append(dwell_time)
    return dwell_times

def calculate_flight_time(keystrokes):
    # Calculate flight time (time between release of one key and press of the next key)
    flight_times = []
    for i in range(len(keystrokes) - 1):
        if keystrokes[i]['event'] == 'r' and keystrokes[i + 1]['event'] == 'p':
            flight_time = keystrokes[i + 1]['time'] - keystrokes[i]['time']
            flight_times.append(flight_time)
    return flight_times

def calculate_digraph_latency(keystrokes):
    # Calculate digraph latency (time between release of one key and press of the next key)
    digraph_latencies = []
    for i in range(len(keystrokes) - 1):
        if keystrokes[i]['event'] == 'r' and keystrokes[i + 1]['event'] == 'p':
            digraph_latency = keystrokes[i + 1]['time'] - keystrokes[i]['time']
            digraph_latencies.append(digraph_latency)
    return digraph_latencies

def calculate_typing_speed(keystrokes, paragraph_length):
    # Calculate typing speed (characters per minute)
    total_time = keystrokes[-1]['time'] - keystrokes[0]['time']
    characters_typed = sum(1 for k in keystrokes if k['event'] == 'p')
    typing_speed = (characters_typed / total_time) * 60000  # Convert to characters per minute
    return typing_speed
