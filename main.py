import matplotlib.pyplot as plt
import pyautogui
import time

# Set up the plot
plt.ion()  # Turn on interactive mode
figure, ax = plt.subplots()
line, = ax.plot([], [], 'b-', linewidth=1)  # For the line connecting dots
current_position_dot = ax.scatter([], [], s=100, color='red')  # For the current cursor position dot
plt.gca().invert_yaxis()  # Invert y-axis to match screen coordinates

x_data, y_data = [], []

# Initialize flag to track if the first movement has been processed
first_movement_processed = False

def update_limits(x_data, y_data):
    margin = 10  # Add a small margin to make sure points are not on the edge
    ax.set_xlim(min(x_data) - margin, max(x_data) + margin)
    ax.set_ylim(min(y_data) - margin, max(y_data) + margin)

def add_perpendicular_line(x_data, y_data):
    global first_movement_processed  # Access the global flag
    if len(x_data) >= 2 and not first_movement_processed:
        # Calculate direction of movement
        dx = x_data[-1] - x_data[-2]
        dy = y_data[-1] - y_data[-2]
        # Calculate a perpendicular direction
        perp_dx, perp_dy = -dy, dx
        # Normalize the perpendicular vector
        length = (perp_dx**2 + perp_dy**2)**0.5
        if length != 0:
            perp_dx, perp_dy = (perp_dx / length) * 20, (perp_dy / length) * 20  # Adjust the length of the line as needed
            # Calculate the endpoints of the perpendicular line
            x_center, y_center = x_data[-1], y_data[-1]
            x_start, y_start = x_center - perp_dx / 2, y_center - perp_dy / 2
            x_end, y_end = x_center + perp_dx / 2, y_center + perp_dy / 2
            # Add a new green line for the first movement direction
            ax.plot([x_start, x_end], [y_start, y_end], 'g-', linewidth=2)
            first_movement_processed = True  # Update flag to prevent further perpendicular lines

try:
    while True:
        x, y = pyautogui.position()  # Get current cursor position
        x_data.append(x)
        y_data.append(y)
        line.set_data(x_data, y_data)  # Update the line data
        
        # Update the scatter plot to show only the current position as a red dot
        current_position_dot.set_offsets([[x, y]])
        
        if x_data and y_data:  # Check if there are any points to avoid error on min/max calculation
            update_limits(x_data, y_data)
            add_perpendicular_line(x_data, y_data)  # Call this function to possibly add a perpendicular line
        
        plt.draw()
        plt.pause(0.1)  # Pause to update the graph and allow for UI interaction

except KeyboardInterrupt:
    plt.close('all')
