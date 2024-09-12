from flask import Flask, render_template, request, send_file
import numpy as np
import svgwrite
from svgpathtools import svg2paths
import os

app = Flask(__name__)

# Function to generate spiral and G-code
def generate_spiral(num_turns, spacing, num_points, scale_factor, degree, feed_rate, delay_start, inner_radius):

    if os.path.exists('spiral.svg'):
        os.remove('spiral.svg')
    if os.path.exists('spiral.gcode'):
        os.remove('spiral.gcode')
    rotation_angle = np.radians(degree)  # Convert degrees to radians

    # Calculate scale factor for DPI
    dpi = 96  # Default DPI

    # Generate spiral points with inner radius
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    r = inner_radius + spacing * theta * scale_factor

    # Convert to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Rotate the spiral by applying a 2D rotation matrix
    x_rotated = x * np.cos(rotation_angle) - y * np.sin(rotation_angle)
    y_rotated = x * np.sin(rotation_angle) + y * np.cos(rotation_angle)

    # Shift the spiral to the positive quadrant
    x_min = np.min(x_rotated)
    y_min = np.min(y_rotated)
    x_shifted = x_rotated - x_min
    y_shifted = y_rotated - y_min

    # Create SVG drawing
    dwg = svgwrite.Drawing('spiral.svg', profile='tiny', size=('500px', '500px'))

    # Draw the spiral using polyline
    points = list(zip(x_shifted, y_shifted))
    dwg.add(dwg.polyline(points, stroke='black', fill='none', stroke_width=1))

    # Save as SVG file
    dwg.save()

    # Load the SVG file and extract paths
    paths, attributes = svg2paths('spiral.svg')
    
    scale_factor = 25.4 / dpi  # Converts inches to mm based on DPI

    # Function to convert paths to G-code
    def convert_paths_to_gcode(paths, feed_rate, scale_factor, delay_start):
        gcode = []
        for path in paths:
            for segment in path:
                # Scale the points by the scale factor
                start = segment.start * scale_factor
                end = segment.end * scale_factor
                gcode.append(f"G21\nG90\nG0 X{start.real:.3f} Y{start.imag:.3f}\nM40\nG4 P{delay_start }")
                gcode.append(f"G1 F{feed_rate} ")
                break
            break
        for path in paths:
            for segment in path:
                start = segment.start * scale_factor
                end = segment.end * scale_factor

                gcode.append(f"G1 X{start.real:.3f} Y{start.imag:.3f}")
                gcode.append(f"G1 X{end.real:.3f} Y{end.imag:.3f}")

        gcode.append(f"G4 P0.00001\nM37\nG1 X0 Y0")
        return gcode

    # Convert paths to G-code
    gcode = convert_paths_to_gcode(paths, feed_rate, scale_factor, delay_start)

    # Save the G-code to a file
    with open('spiral.gcode', 'w') as f:
        for line in gcode:
            f.write(line + '\n')

    return 'spiral.svg', 'spiral.gcode'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input from form
        num_turns = float(request.form['num_turns'])
        spacing = float(request.form['spacing'])
        num_points = int(request.form['num_points'])
        scale_factor = float(request.form['scale_factor'])
        degree = int(request.form['degree'])
        feed_rate = int(request.form['feed_rate'])
        delay_start = float(request.form['delay_start'])
        inner_radius = float(request.form['inner_radius'])  # New parameter

        # Generate spiral and G-code
        svg_file, gcode_file = generate_spiral(num_turns, spacing, num_points, scale_factor, degree, feed_rate, delay_start, inner_radius)

        return render_template('result.html', svg_file=svg_file, gcode_file=gcode_file)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
