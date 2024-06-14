import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.stats import norm

# Function to calculate and display the predictions and suggestions
def calculate():
    try:
        # Read and process the scores from the entry field
        scores_str = entry_scores.get()
        scores = list(map(int, scores_str.split(',')))
        
        # Read and process the bookmaker's lines
        lower_bound = float(entry_lower_bound.get())
        upper_bound = float(entry_upper_bound.get())
        
        # Calculate mean and standard deviation
        mean_score = np.mean(scores)
        std_dev = np.std(scores)

        # Determine confidence intervals (e.g., 95% confidence interval)
        z_score = norm.ppf(0.975)  # 95% confidence
        margin_of_error = z_score * std_dev
        lower_conf_bound = mean_score - margin_of_error
        upper_conf_bound = mean_score + margin_of_error

        # Assessing the bookmaker's line
        if lower_conf_bound <= lower_bound and upper_conf_bound >= upper_bound:
            line_comment = "Bookmaker's line\n is within the expected range."
        else:
            line_comment = "Bookmaker's line\n is outside the expected range."

        # Count scores exceeding lower bound
        exceeds_lower = sum(score > lower_bound for score in scores)

        # Count scores below upper bound
        below_upper = sum(score < upper_bound for score in scores)

        # Calculate frequencies
        total_games = len(scores)
        exceed_lower_freq = exceeds_lower / total_games
        below_upper_freq = below_upper / total_games

        # Determine variability comment
        if std_dev > 10:
            variability_comment = "High variability in scores.\n The team's performance is unpredictable."
        else:
            variability_comment = "Low variability in scores.\n The team maintains a consistent performance range."

        # Adjusted betting suggestion based on frequency and variability
        if exceed_lower_freq >= 0.6 and below_upper_freq < 0.6 and std_dev <= 10:
            bet_suggestion = f"Bet on 'Over' {lower_bound}"
        elif below_upper_freq >= 0.6 and exceed_lower_freq < 0.6 and std_dev <= 10:
            bet_suggestion = f"Bet on 'Under' {upper_bound}"
        else:
            bet_suggestion = "The team's performance\n is too unpredictable for a confident bet."

        # Display the results
        label_mean_score.config(text=f"Mean Score: {mean_score:.2f}")
        label_std_dev.config(text=f"Standard Deviation: {std_dev:.2f}")
        label_conf_interval.config(text=f"95% Confidence Interval: {lower_conf_bound:.2f} to {upper_conf_bound:.2f}")
        label_line_comment.config(text=f"Assessment: {line_comment}")
        label_exceed_lower_freq.config(text=f"Scores exceeding {lower_bound}: {exceeds_lower} times ({exceed_lower_freq:.2%})")
        label_below_upper_freq.config(text=f"Scores below {upper_bound}: {below_upper} times ({below_upper_freq:.2%})")
        label_variability_comment.config(text=f"Variability Comment: {variability_comment}")
        label_bet_suggestion.config(text=f"Betting Suggestion: {bet_suggestion}")
        
    except Exception as e:
        messagebox.showerror("Error", "Please enter valid scores and bookmaker's lines.")

# Create the main window
root = tk.Tk()
root.title("Basketball Score Predictor")

# Create and place the widgets using grid
label_instruction = tk.Label(root, text="Enter scores separated by commas:")
label_instruction.grid(row=0, column=0, sticky='w', padx=5, pady=2)

entry_scores = tk.Entry(root, width=30)
entry_scores.grid(row=1, column=0, sticky='w', padx=5, pady=2)
#entry_scores.insert(0, "95,103,99,109,102,111,92,98,72,102")  # Default scores

label_lower_bound_instruction = tk.Label(root, text="Enter lower bookmaker's line:")
label_lower_bound_instruction.grid(row=2, column=0, sticky='w', padx=5, pady=2)

entry_lower_bound = tk.Entry(root, width=20)
entry_lower_bound.grid(row=3, column=0, sticky='w', padx=5, pady=2)
#entry_lower_bound.insert(0, "96.5")  # Default lower bound

label_upper_bound_instruction = tk.Label(root, text="Enter upper bookmaker's line:")
label_upper_bound_instruction.grid(row=4, column=0, sticky='w', padx=5, pady=2)

entry_upper_bound = tk.Entry(root, width=20)
entry_upper_bound.grid(row=5, column=0, sticky='w', padx=5, pady=2)
#entry_upper_bound.insert(0, "100.5")  # Default upper bound

button_calculate = tk.Button(root, text="Calculate", command=calculate)
button_calculate.grid(row=6, column=0, sticky='w', padx=5, pady=5)

label_mean_score = tk.Label(root, text="Mean Score: ")
label_mean_score.grid(row=7, column=0, sticky='w', padx=5, pady=2)

label_std_dev = tk.Label(root, text="Standard Deviation: ")
label_std_dev.grid(row=8, column=0, sticky='w', padx=5, pady=2)

label_conf_interval = tk.Label(root, text="95% Confidence Interval: ")
label_conf_interval.grid(row=9, column=0, sticky='w', padx=5, pady=2)

label_line_comment = tk.Label(root, text="Assessment: ")
label_line_comment.grid(row=10, column=0, sticky='w', padx=5, pady=2)

label_exceed_lower_freq = tk.Label(root, text="Scores exceeding lower bound: ")
label_exceed_lower_freq.grid(row=11, column=0, sticky='w', padx=5, pady=2)

label_below_upper_freq = tk.Label(root, text="Scores below upper bound: ")
label_below_upper_freq.grid(row=12, column=0, sticky='w', padx=5, pady=2)

label_variability_comment = tk.Label(root, text="Variability Comment: ")
label_variability_comment.grid(row=13, column=0, sticky='w', padx=5, pady=2)

label_bet_suggestion = tk.Label(root, text="Betting Suggestion: ")
label_bet_suggestion.grid(row=14, column=0, sticky='w', padx=5, pady=2)

# Adjust window size and position
root.geometry("700x1000")

# Run the application
root.mainloop()

