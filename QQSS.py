import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

# Function to calculate state probabilities from the qubit state
def calculate_probabilities(alpha, beta):
    p0 = np.abs(alpha)**2  # Probability of |0>
    p1 = np.abs(beta)**2   # Probability of |1>
    total_prob = p0 + p1
    
    # Normalize the probabilities to ensure they sum to 1
    p0 /= total_prob
    p1 /= total_prob
    return p0, p1

# Function to calculate the classical bit state based on probabilities
def measure_classical_bit(p0, p1):
    return np.random.choice([0, 1], p=[p0, p1])

# Function to apply a quantum gate (example: Pauli-X Gate)
def apply_gate(state):
    # Example gate: Pauli-X gate (flips the state)
    alpha, beta = state
    new_alpha = beta  # Pauli-X flips the |0> and |1> coefficients
    new_beta = alpha
    return new_alpha, new_beta

# Function to plot the Bloch sphere with qubit state
def bloch_sphere(ax, phi, theta, color='color', alpha=0.3):
    # Create the spherical coordinates for the Bloch Sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    # Create a light source to add some dynamic lighting effects to the sphere
    light_source = LightSource(azdeg=0, altdeg=65)
    topography = np.sqrt(x**2 + y**2 + z**2)

    # Apply lighting to the sphere surface with partial transparency and light color
    ax.plot_surface(x, y, z, rstride=5, cstride=5, facecolors=light_source.shade(topography, cmap=cm.plasma), 
                linewidth=0, alpha=0.2, shade=True)
                

    # Dotted equator
    theta_eq = np.linspace(0, 2 * np.pi, 50)
    x_eq = np.cos(theta_eq)
    y_eq = np.sin(theta_eq)
    ax.plot(x_eq, y_eq, 0, linestyle=':', color='magenta', linewidth=0.50)

    # Qubit state vector (the arrow)
    xq = np.sin(theta) * np.cos(phi)
    yq = np.sin(theta) * np.sin(phi)
    zq = np.cos(theta)
    ax.quiver(0, 0, 0, xq, yq, zq, color=color, arrow_length_ratio=0.15, linewidth=2, alpha=0.9)
    ax.plot([xq], [yq], [zq], marker='o', markersize=6, color=color, alpha=0.9)

    # Dotted axes (X, Y, Z) from the center with glowing effect
    ax.plot([0, 1], [0, 0], [0, 0], linestyle=':', color='#FF0000', linewidth=0.50)  # x-axis
    ax.plot([0, 0], [0, 1], [0, 0], linestyle=':', color='#00FF00', linewidth=0.50)  # y-axis
    ax.plot([0, 0], [0, 0], [0, 1], linestyle=':', color='#0000FF', linewidth=0.50)  # z-axis

    # Set the axes and make them visible with lines and grid
    ax.grid(True, color='white', linestyle='--', linewidth=0.5)

    # Label the axes with enhanced fonts
    ax.text(1.1, 0, 0, 'x', color='black', fontsize=10, alpha=0.7)
    ax.text(0, 1.1, 0, 'z', color='black', fontsize=10, alpha=0.7)
    ax.text(0, 0, 1.1, 'y', color='black', fontsize=10, alpha=0.7)

    # label of '0' and '1' for superposition
    ax.text(0, 0, 0.9, '0', color='#FF1493', fontsize=13, fontweight='bold',alpha=0.7)
    ax.text(0, 0, -1.1, '1', color='#FF1493', fontsize=13, fontweight='bold',alpha=0.7)

    ax.text(-0.1320,-0.6086,-1.0417, 'bloch sphere', color='magenta', fontsize=13, fontweight='bold',alpha=0.7)

    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_facecolor('white')  # Change background color to white for better contrast

# Function to calculate the quantum state (e.g., for a 2-qubit system)
def calculate_quantum_state(p0, p1, classical_bit_state):
    if classical_bit_state == 0:
        return '|00>' if p0 > p1 else '|01>'
    elif classical_bit_state == 1:
        return '|10>' if p0 > p1 else '|11>'
    return '|00>'

# Create the figure with a subplot to display calculations
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(121, projection='3d')  # Bloch sphere on the left
ax_text = fig.add_subplot(122)  # Text display on the right

# Set the title of the simulation
fig.suptitle("Quantum Qubit Superposition Simulation", fontsize=20, fontweight='bold', color='#FF1493', y=0.95, ha='center')

# Add title above the Bloch sphere
ax.set_title("Quantum Qubit Superposition", fontsize=18, color='gold', fontweight='bold')

# Initial state (alpha and beta based on theta, phi)
alpha = 0.88  # Initial amplitude for |0>
beta = -0.35 + 0.31j  # Initial amplitude for |1>

# Gate type (for display purposes)
gate_type = "Pauli-X Gate"  # Example gate used

# Calculate initial probabilities
p0, p1 = calculate_probabilities(alpha, beta)
classical_bit_state = measure_classical_bit(p0, p1)

# Calculate quantum state based on classical bit state
quantum_state = calculate_quantum_state(p0, p1, classical_bit_state)

# Apply a gate (e.g., Pauli-X Gate)
new_alpha, new_beta = apply_gate((alpha, beta))
new_p0, new_p1 = calculate_probabilities(new_alpha, new_beta)
new_classical_bit_state = measure_classical_bit(new_p0, new_p1)

# Calculate quantum state after applying the gate
new_quantum_state = calculate_quantum_state(new_p0, new_p1, new_classical_bit_state)

# Animation loop control flag
running = True

# Function to handle the window close event
def on_close(event):
    global running
    running = False

# Connect the window close event to the handler
fig.canvas.mpl_connect('close_event', on_close)

# Animation loop (continuously update the Bloch sphere and calculation display)
while running:
    # Update phi and theta with random increments based on the previous state
    dphi = np.random.randn() * 0.1  # Random change in phi
    dtheta = np.random.randn() * 0.1  # Random change in theta
    phi = np.random.rand() * 2 * np.pi  # Random azimuthal angle
    theta = np.arccos(np.random.rand() * 2 - 1)  # Random polar angle

    # Update the state based on new phi and theta
    alpha = np.cos(theta / 2)
    beta = np.exp(1j * phi) * np.sin(theta / 2)

    # Calculate probabilities and classical bit state for the updated qubit state
    p0, p1 = calculate_probabilities(alpha, beta)
    classical_bit_state = measure_classical_bit(p0, p1)

    # Calculate quantum state based on classical bit state
    quantum_state = calculate_quantum_state(p0, p1, classical_bit_state)

    # Apply a gate (for example, a Pauli-X Gate) and recalculate
    new_alpha, new_beta = apply_gate((alpha, beta))
    new_p0, new_p1 = calculate_probabilities(new_alpha, new_beta)
    new_classical_bit_state = measure_classical_bit(new_p0, new_p1)

    # Calculate quantum state after applying the gate
    new_quantum_state = calculate_quantum_state(new_p0, new_p1, new_classical_bit_state)

    # Clear and redraw the Bloch sphere with updated state
    ax.clear()
    bloch_sphere(ax, phi, theta, color='#FF1493')  # Highlight the qubit state vector with cyan color

    # Update the text display with the current results
    ax_text.clear()
    ax_text.axis('off')  # Hide axes for the text plot

    # Use bold and color formatting to highlight important information
    

    ax_text.text(0, 0.9, f"Qubit Initial State: ({alpha:.2f}+{beta.imag:.2f}j)|0> + ({beta.real:.2f}+{beta.imag:.2f}j)|1>", fontsize=12, fontweight='bold', color='magenta')
    ax_text.text(0, 0.8, f"Qubit Probabilities: |0>: {p0:.2f}, |1>: {p1:.2f}", fontsize=12, color='yellow')
    ax_text.text(0, 0.7, f"Classical Bit State: {classical_bit_state}", fontsize=12, color='lime')

    # Add the quantum state value below
    ax_text.text(0, 0.6, f"Quantum State: {quantum_state}", fontsize=12, color='cyan')
    # Add QUBIT STATE at specific coordinates
    ax_text.text(0.437, 0.989, "QUBIT STATE", fontsize=18, color='#32CD32', fontweight='bold', ha='center')
    # Add gate type at specific coordinates
    ax_text.text(0.435, 0.502, f"GATE TYPE: {gate_type}", fontsize=18, color='#32CD32', fontweight='bold', ha='center')

    # Gate results and probabilities (move calculations down by 2 inches)
    ax_text.text(0, 0.4, f"Gate Result: ({new_alpha:.2f}+{new_beta.imag:.2f}j)|0> + ({new_beta.real:.2f}+{new_beta.imag:.2f}j)|1>", fontsize=12, color='magenta',fontweight='bold')
    ax_text.text(0, 0.3, f"Gate Probabilities: |0>: {new_p0:.2f}, |1>: {new_p1:.2f}", fontsize=12, color='yellow')
    ax_text.text(0, 0.2, f"Gate Classical Bit State: {new_classical_bit_state}", fontsize=12, color='lime')
    ax_text.text(0, 0.1, f"Gate Quantum State: {new_quantum_state}", fontsize=12, color='cyan')

    plt.draw()
    plt.pause(0.1)  # Adjust for animation speed

plt.show()
