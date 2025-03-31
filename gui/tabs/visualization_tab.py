# visualization_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import os

def setup_visualization_tab(gui):
    """Set up the visualization tab for displaying charts and graphs"""
    # Create the tab
    visualization_frame = ttk.Frame(gui.notebook)
    gui.notebook.add(visualization_frame, text=" Visualization ")
    
    # Configure the grid
    visualization_frame.grid_columnconfigure(0, weight=1)
    visualization_frame.grid_rowconfigure(1, weight=1)
    
    # Top controls frame
    controls_frame = ttk.Frame(visualization_frame)
    controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    ttk.Label(controls_frame, text="Performance Visualization", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    # Chart type selection
    ttk.Label(controls_frame, text="Chart Type:").pack(side=tk.LEFT, padx=10, pady=5)
    gui.chart_type_var = tk.StringVar(value="radar")
    chart_types = ["radar", "bar", "heatmap", "evolution"]
    chart_type_dropdown = ttk.Combobox(controls_frame, textvariable=gui.chart_type_var, 
                                     values=chart_types, width=10,
                                     state="readonly")
    chart_type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
    chart_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_visualization(gui, e))
    
    # Export button
    export_button = ctk.CTkButton(controls_frame, text="Export Chart", 
                                command=lambda: export_chart(gui))
    export_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Main visualization area
    gui.visualization_area = ttk.Frame(visualization_frame)
    gui.visualization_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # Create a figure for matplotlib
    gui.figure = Figure(figsize=(10, 6), dpi=100)
    gui.plot = gui.figure.add_subplot(111)
    
    # Create canvas for matplotlib figure
    gui.chart_canvas = FigureCanvasTkAgg(gui.figure, gui.visualization_area)
    gui.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add placeholder text on the plot
    gui.plot.text(0.5, 0.5, "Generate a computer to visualize performance data", 
                 horizontalalignment='center', verticalalignment='center',
                 transform=gui.plot.transAxes, fontsize=14)
    gui.plot.axis('off')
    gui.chart_canvas.draw()
    
    # Attach visualization functions to gui object
    gui.update_visualization = update_visualization
    gui.create_radar_chart = create_radar_chart
    gui.create_bar_chart = create_bar_chart
    gui.create_heatmap_chart = create_heatmap_chart
    gui.create_evolution_chart = create_evolution_chart
    gui.export_chart = export_chart


def update_visualization(gui, event=None):
    """Update the visualization based on selected chart type"""
    if not hasattr(gui, 'current_computer') or not hasattr(gui, 'stats'):
        return
    
    # Clear the figure
    gui.plot.clear()
    
    # Get selected chart type
    chart_type = gui.chart_type_var.get()
    
    if chart_type == "radar":
        create_radar_chart(gui)
    elif chart_type == "bar":
        create_bar_chart(gui)
    elif chart_type == "heatmap":
        create_heatmap_chart(gui)
    elif chart_type == "evolution":
        create_evolution_chart(gui)
    
    # Redraw the canvas
    gui.chart_canvas.draw()


def create_radar_chart(gui):
    """Create a radar chart of performance metrics"""
    # Get performance metrics
    if not hasattr(gui, 'current_computer'):
        return
            
    performance = gui.current_computer.estimated_performance
    
    # Categories for radar chart
    categories = ['Gaming', 'Productivity', 'Content Creation', 'Development']
    
    # Values for each category
    values = [
        performance.get('gaming', 0),
        performance.get('productivity', 0),
        performance.get('content_creation', 0),
        performance.get('development', 0)
    ]
    
    # Add the first value to close the circular graph
    categories.append(categories[0])
    values.append(values[0])
    
    # Convert to radians for plot
    angles = np.linspace(0, 2*np.pi, len(categories)-1, endpoint=False).tolist()
    angles.append(angles[0])
    
    # Create polar subplot
    gui.plot = gui.figure.add_subplot(111, polar=True)
    
    # Create radar chart
    gui.plot.plot(angles, values, marker='o', linestyle='-', linewidth=2, color=gui.accent_color)
    
    # Fill area
    gui.plot.fill(angles, values, alpha=0.25, color=gui.accent_color)
    
    # Set category labels
    gui.plot.set_xticks(angles[:-1])
    gui.plot.set_xticklabels(categories[:-1])
    
    # Set y-axis limits
    gui.plot.set_ylim(0, 100)
    
    # Add title
    gui.plot.set_title("Performance Radar Chart")


def create_bar_chart(gui):
    """Create a bar chart of performance metrics"""
    # Get performance metrics
    if not hasattr(gui, 'current_computer'):
        return
        
    performance = gui.current_computer.estimated_performance
    
    # Categories and values
    categories = ['Gaming', 'Productivity', 'Content Creation', 'Development']
    values = [
        performance.get('gaming', 0),
        performance.get('productivity', 0),
        performance.get('content_creation', 0),
        performance.get('development', 0)
    ]
    
    # Create bar chart
    bars = gui.plot.bar(categories, values, color=gui.accent_color)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        gui.plot.text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{height:.1f}', ha='center', va='bottom')
    
    # Add labels and title
    gui.plot.set_xlabel('Performance Category')
    gui.plot.set_ylabel('Score (0-100)')
    gui.plot.set_title('Performance by Category')
    gui.plot.set_ylim(0, 110)  # Allow space for labels
    gui.plot.grid(axis='y', linestyle='--', alpha=0.7)


def create_heatmap_chart(gui):
    """Create a heatmap comparing component quality"""
    # Define components and quality scores
    if not hasattr(gui, 'current_computer'):
        return
        
    # Define components and their quality scores (0-10)
    components = ['CPU', 'GPU', 'RAM', 'Storage', 'Motherboard', 'PSU', 'Cooling', 'Case']
    
    # Calculate quality scores based on price and performance
    quality_scores = [
        min(10, gui.current_computer.cpu.performance / 10),
        min(10, (gui.current_computer.gpu.power / 10) if gui.current_computer.gpu else 
            gui.current_computer.cpu.integrated_graphics_power / 10),
        min(10, gui.current_computer.ram.capacity / 8 + gui.current_computer.ram.frequency / 1000),
        min(10, gui.current_computer.storage.capacity / 500 + 
            (5 if gui.current_computer.storage.type == "SSD" else 0)),
        min(10, gui.current_computer.motherboard.price / 1000 * 5),
        min(10, gui.current_computer.psu.capacity / 100),
        min(10, getattr(gui.current_computer.cooling, 'cooling_capacity', 100) / 100),
        min(10, gui.current_computer.case.price / 500 * 5)
    ]
    
    # Create heatmap data
    heatmap_data = np.array(quality_scores).reshape(1, -1)
    
    # Create heatmap
    im = gui.plot.imshow(heatmap_data, cmap='viridis', aspect='auto')
    
    # Add colorbar
    cbar = gui.figure.colorbar(im, ax=gui.plot, orientation='vertical', pad=0.01)
    cbar.set_label('Quality Score (0-10)')
    
    # Configure axes
    gui.plot.set_yticks([])
    gui.plot.set_xticks(np.arange(len(components)))
    gui.plot.set_xticklabels(components, rotation=45, ha='right')
    
    # Add value labels
    for i, score in enumerate(quality_scores):
        gui.plot.text(i, 0, f'{score:.1f}', ha='center', va='center', 
                     color='white', fontweight='bold')
    
    # Add title
    gui.plot.set_title('Component Quality Heatmap')


def create_evolution_chart(gui):
    """Create a chart showing the evolution of fitness during optimization"""
    if not hasattr(gui, 'stats') or 'best_fitness_history' not in gui.stats:
        gui.plot.text(0.5, 0.5, "No evolution data available", 
                     horizontalalignment='center', verticalalignment='center',
                     transform=gui.plot.transAxes, fontsize=14)
        return
        
    # Get evolution data
    generations = range(len(gui.stats['best_fitness_history']))
    best_fitness = gui.stats['best_fitness_history']
    
    # Check if we have average and worst fitness data
    has_avg = 'avg_fitness_history' in gui.stats and len(gui.stats['avg_fitness_history']) > 0
    has_worst = 'worst_fitness_history' in gui.stats and len(gui.stats['worst_fitness_history']) > 0
    
    # Plot best fitness
    gui.plot.plot(generations, best_fitness, 'g-', label='Best Fitness', linewidth=2)
    
    # Plot average fitness if available
    if has_avg:
        avg_fitness = gui.stats['avg_fitness_history']
        gui.plot.plot(generations, avg_fitness, 'b-', label='Average Fitness')
    
    # Plot worst fitness if available
    if has_worst:
        worst_fitness = gui.stats['worst_fitness_history']
        gui.plot.plot(generations, worst_fitness, 'r-', label='Worst Fitness')
    
    # Add labels and title
    gui.plot.set_xlabel('Generation')
    gui.plot.set_ylabel('Fitness Score')
    gui.plot.set_title('Fitness Evolution Over Generations')
    gui.plot.legend()
    gui.plot.grid(True)


def export_chart(gui):
    """Export the current visualization chart to a file"""
    if not hasattr(gui, 'figure'):
        messagebox.showinfo("No Chart", "No chart to export.")
        return
        
    # Ask for file name
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")])
    
    if not file_path:
        return
        
    # Save the figure
    try:
        gui.figure.savefig(file_path, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Export Successful", f"Chart exported to: {file_path}")
        gui.status_bar.config(text=f"Chart exported to: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Error exporting chart: {str(e)}")
        gui.status_bar.config(text="Error exporting chart")