from collections import Counter
# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
    # opponent_history is persistent across calls for a single game.
    # We'll use opponent_history[0] to store our internal state (tracker dictionary).
    # And `actual_opponent_moves` (stored within the tracker) to hold the opponent's R, P, S moves.

    # Initialize state for a new game or if history is empty
    if not opponent_history:
        # opponent_history[0] will be our internal state dictionary
        opponent_history.append({'pattern_tracker': {}, 'num_rounds': 0, 'actual_opponent_moves': []})

    tracker = opponent_history[0] # Our internal state dictionary
    actual_opponent_moves = tracker['actual_opponent_moves'] # This is the list for opponent's R, P, S moves
    pattern_tracker = tracker['pattern_tracker']
    num_rounds = tracker['num_rounds']

    # Update number of rounds
    tracker['num_rounds'] += 1

    # Add the current prev_play to our actual_opponent_moves list, if it's a valid move.
    # 'prev_play' will be '' for the very first round of a game.
    if prev_play in ['R', 'P', 'S']:
        actual_opponent_moves.append(prev_play)

    # Define look-back depth for patterns
    k = 4 # How many previous opponent moves to consider for a pattern

    # Update patterns based on the outcome of the *previous* round.
    # We need `k` moves for the pattern itself and 1 for the consequence.
    if len(actual_opponent_moves) > k:
        # The sequence is (O1, O2, O3, O4) -> O5
        observed_sequence = "".join(actual_opponent_moves[-(k+1):-1])
        next_opponent_move_in_pattern = actual_opponent_moves[-1]

        if observed_sequence not in pattern_tracker:
            pattern_tracker[observed_sequence] = Counter() # Counter imported at file level
        pattern_tracker[observed_sequence][next_opponent_move_in_pattern] += 1

    # Now, make a guess for *this* round.
    guess = "R" # Default guess if no other logic applies

    # If we have enough history to form a sequence to predict from
    if len(actual_opponent_moves) >= k:
        current_prediction_sequence = "".join(actual_opponent_moves[-k:])

        if current_prediction_sequence in pattern_tracker:
            # Predict the most common move that followed this sequence
            predicted_opponent_move = pattern_tracker[current_prediction_sequence].most_common(1)[0][0]
            # Counter that predicted move
            if predicted_opponent_move == "R":
                guess = "P"
            elif predicted_opponent_move == "P":
                guess = "S"
            else: # "S"
                guess = "R"
        else:
            # If the exact k-length pattern is new, fall back to counter overall most frequent move.
            if actual_opponent_moves:
                overall_counts = Counter(actual_opponent_moves)
                most_frequent_overall = overall_counts.most_common(1)[0][0]
                if most_frequent_overall == "R":
                    guess = "P"
                elif most_frequent_overall == "P":
                    guess = "S"
                else: # "S"
                    guess = "R"
    else:
        # For very early rounds (less than k valid opponent moves), fall back to counter overall most frequent move
        if actual_opponent_moves:
            overall_counts = Counter(actual_opponent_moves)
            most_frequent_overall = overall_counts.most_common(1)[0][0]
            if most_frequent_overall == "R":
                guess = "P"
            elif most_frequent_overall == "P":
                guess = "S"
            else: # "S"
                guess = "R"

    return guess
