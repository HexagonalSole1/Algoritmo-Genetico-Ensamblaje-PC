# component_browser_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk


def setup_component_browser_tab(gui):
    """Set up the component browser tab for exploring available components"""
    # Create the tab
    browser_frame = ttk.Frame(gui.notebook)
    gui.notebook.add(browser_frame, text=" Component Browser ")
    
    # Configure the grid
    browser_frame.grid_columnconfigure(1, weight=1)
    browser_frame.grid_rowconfigure(1, weight=1)
    
    # Top controls frame
    controls_frame = ttk.Frame(browser_frame)
    controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    
    ttk.Label(controls_frame, text="Component Browser", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    # Component type selection
    ttk.Label(controls_frame, text="Component Type:").pack(side=tk.LEFT, padx=10, pady=5)
    gui.component_type_var = tk.StringVar(value="cpu")
    component_types = ["cpu", "gpu", "ram", "storage", "motherboard", "psu", "cooling", "case"]
    component_type_dropdown = ttk.Combobox(controls_frame, textvariable=gui.component_type_var, 
                                         values=component_types, width=12,
                                         state="readonly")
    component_type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Search bar
    ttk.Label(controls_frame, text="Search:").pack(side=tk.LEFT, padx=10, pady=5)
    gui.search_var = tk.StringVar()
    search_entry = ttk.Entry(controls_frame, textvariable=gui.search_var, width=20)
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    search_button = ctk.CTkButton(controls_frame, text="Search", command=lambda: search_components(gui))
    search_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Reset filters button
    reset_button = ctk.CTkButton(controls_frame, text="Reset Filters", command=lambda: reset_component_filters(gui))
    reset_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Left pane - filters
    filters_frame = ttk.LabelFrame(browser_frame, text="Filters")
    filters_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)
    
    # Price range filter
    ttk.Label(filters_frame, text="Price Range:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    price_filter_frame = ttk.Frame(filters_frame)
    price_filter_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    
    ttk.Label(price_filter_frame, text="Min:").grid(row=0, column=0, sticky="w")
    gui.price_filter_min_var = tk.StringVar(value="0")
    price_filter_min_entry = ttk.Entry(price_filter_frame, textvariable=gui.price_filter_min_var, width=8)
    price_filter_min_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
    
    ttk.Label(price_filter_frame, text="Max:").grid(row=0, column=2, sticky="w")
    gui.price_filter_max_var = tk.StringVar(value="50000")
    price_filter_max_entry = ttk.Entry(price_filter_frame, textvariable=gui.price_filter_max_var, width=8)
    price_filter_max_entry.grid(row=0, column=3, sticky="w", padx=5, pady=2)
    
    # Apply price filter button
    apply_price_button = ctk.CTkButton(price_filter_frame, text="Apply", command=lambda: apply_price_filter(gui))
    apply_price_button.grid(row=0, column=4, padx=5, pady=2)
    
    # Brand filter
    ttk.Label(filters_frame, text="Brand:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    
    gui.brand_filter_var = tk.StringVar(value="All")
    gui.brand_filter_list = ttk.Combobox(filters_frame, textvariable=gui.brand_filter_var, values=["All"], width=15)
    gui.brand_filter_list.grid(row=3, column=0, sticky="w", padx=10, pady=2)
    gui.brand_filter_list.bind("<<ComboboxSelected>>", lambda e: apply_brand_filter(gui))
    
    # Component-specific filters frame
    gui.specific_filters_frame = ttk.LabelFrame(filters_frame, text="Specific Filters")
    gui.specific_filters_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
    
    # Right pane - component list
    list_frame = ttk.Frame(browser_frame)
    list_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    
    # Component list with details
    columns = ('name', 'details', 'performance', 'price')
    gui.components_browser = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
    
    # Define headings and columns
    gui.components_browser.heading('name', text='Name')
    gui.components_browser.heading('details', text='Details')
    gui.components_browser.heading('performance', text='Performance')
    gui.components_browser.heading('price', text='Price')
    
    gui.components_browser.column('name', width=200, anchor='w')
    gui.components_browser.column('details', width=300, anchor='w')
    gui.components_browser.column('performance', width=100, anchor='center')
    gui.components_browser.column('price', width=100, anchor='e')
    
    # Scrollbars
    vscrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=gui.components_browser.yview)
    hscrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=gui.components_browser.xview)
    gui.components_browser.configure(yscroll=vscrollbar.set, xscroll=hscrollbar.set)
    
    # Pack components
    gui.components_browser.grid(row=0, column=0, sticky="nsew")
    vscrollbar.grid(row=0, column=1, sticky="ns")
    hscrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    list_frame.grid_columnconfigure(0, weight=1)
    list_frame.grid_rowconfigure(0, weight=1)
    
    # Create context menu (right-click menu) for component browser
    gui.component_context_menu = tk.Menu(gui.components_browser, tearoff=0)
    gui.component_context_menu.add_command(label="View Details", command=lambda: view_component_details(gui))
    gui.component_context_menu.add_command(label="Add to Current Build", command=lambda: add_component_to_build(gui))
    gui.component_context_menu.add_command(label="Compare with Current", command=lambda: compare_with_current(gui))
    
    # Asignar funciones al objeto gui
    gui.search_components = search_components
    gui.apply_price_filter = apply_price_filter
    gui.apply_brand_filter = apply_brand_filter
    gui.reset_component_filters = reset_component_filters
    gui.update_specific_filters = update_specific_filters
    gui.update_brand_filter_list = update_brand_filter_list
    gui.apply_specific_filters = apply_specific_filters
    gui.view_component_details = view_component_details
    gui.add_component_to_build = add_component_to_build
    gui.compare_with_current = compare_with_current
    gui.replace_from_comparison = replace_from_comparison
    gui.show_component_context_menu = show_component_context_menu
    gui.get_component_browser_data = get_component_browser_data
    gui.update_component_browser = update_component_browser


def reset_component_filters(gui):
    # Función simple para restablecer filtros
    gui.status_bar.config(text="Filtros restablecidos (implementación pendiente)")


def view_component_details(gui):
    # Función simple para ver detalles
    gui.status_bar.config(text="Ver detalles (implementación pendiente)")

def add_component_to_build(gui):
    # Función simple para añadir a la construcción
    gui.status_bar.config(text="Componente añadido (implementación pendiente)")

def compare_with_current(gui):
    # Función simple para comparar
    gui.status_bar.config(text="Comparación (implementación pendiente)")

def replace_from_comparison(gui, dialog, component_type, values):
    # Función simple para reemplazar desde comparación
    pass

def show_component_context_menu(gui, event):
    """Show context menu for component browser"""
    # Get selected item
    item = gui.components_browser.identify_row(event.y)
    if not item:
        return
        
    # Select the item
    gui.components_browser.selection_set(item)
    
    # Show context menu
    gui.component_context_menu.post(event.x_root, event.y_root)

def update_component_browser(gui, event=None):
    # Función simple para actualizar el navegador
    component_type = gui.component_type_var.get()
    gui.status_bar.config(text=f"Navegador actualizado con {component_type}")

def update_specific_filters(gui, component_type):
    """Update the component-specific filter options"""
    # Clear existing filters
    for widget in gui.specific_filters_frame.winfo_children():
        widget.destroy()
    
    # Add filters based on component type
    if component_type == 'cpu':
        # Add CPU-specific filters
        ttk.Label(gui.specific_filters_frame, text="Min Cores:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.cpu_cores_var = tk.StringVar(value="0")
        cpu_cores_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.cpu_cores_var, width=5)
        cpu_cores_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(gui.specific_filters_frame, text="Integrated Graphics:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        gui.cpu_igpu_var = tk.BooleanVar(value=False)
        cpu_igpu_check = ttk.Checkbutton(gui.specific_filters_frame, variable=gui.cpu_igpu_var)
        cpu_igpu_check.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
    elif component_type == 'gpu':
        # Add GPU-specific filters
        ttk.Label(gui.specific_filters_frame, text="Min VRAM (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.gpu_vram_var = tk.StringVar(value="0")
        gpu_vram_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.gpu_vram_var, width=5)
        gpu_vram_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(gui.specific_filters_frame, text="Ray Tracing:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        gui.gpu_rt_var = tk.BooleanVar(value=False)
        gpu_rt_check = ttk.Checkbutton(gui.specific_filters_frame, variable=gui.gpu_rt_var)
        gpu_rt_check.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
    elif component_type == 'ram':
        # Add RAM-specific filters
        ttk.Label(gui.specific_filters_frame, text="Min Capacity (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.ram_capacity_var = tk.StringVar(value="0")
        ram_capacity_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.ram_capacity_var, width=5)
        ram_capacity_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(gui.specific_filters_frame, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        gui.ram_type_var = tk.StringVar(value="Any")
        ram_type_combo = ttk.Combobox(gui.specific_filters_frame, textvariable=gui.ram_type_var, 
                                    values=["Any", "DDR4", "DDR5"], width=10, state="readonly")
        ram_type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
    elif component_type == 'storage':
        # Add Storage-specific filters
        ttk.Label(gui.specific_filters_frame, text="Min Capacity (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.storage_capacity_var = tk.StringVar(value="0")
        storage_capacity_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.storage_capacity_var, width=5)
        storage_capacity_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(gui.specific_filters_frame, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        gui.storage_type_var = tk.StringVar(value="Any")
        storage_type_combo = ttk.Combobox(gui.specific_filters_frame, textvariable=gui.storage_type_var, 
                                        values=["Any", "SSD", "HDD"], width=10, state="readonly")
        storage_type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
    # Add apply filters button for all component types
    apply_button = ctk.CTkButton(gui.specific_filters_frame, text="Apply Filters", 
                               command=lambda: gui.apply_specific_filters() if hasattr(gui, 'apply_specific_filters') else None,
                               width=20)
    apply_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def update_brand_filter_list(gui, component_type, components):
    """Update the brand filter dropdown based on available components"""
    # Extract all unique brands
    brands = set()
    for component in components:
        # Extract brand from name (usually the first word)
        name_parts = component["name"].split()
        if name_parts:
            brands.add(name_parts[0])
    
    # Update dropdown values
    brands_list = ["All"] + sorted(list(brands))
    gui.brand_filter_list.configure(values=brands_list)
    gui.brand_filter_var.set("All")

def get_component_browser_data(gui, component_type):
    # Devolver datos de ejemplo
    return [
        {"name": "Componente 1", "details": "Detalles 1", "performance": "90/100", "price": "$100"},
        {"name": "Componente 2", "details": "Detalles 2", "performance": "80/100", "price": "$200"},
        {"name": "Componente 3", "details": "Detalles 3", "performance": "70/100", "price": "$300"}
    ]

def search_components(gui):
    """Search for components matching the search term"""
    # Get selected component type
    component_type = gui.component_type_var.get()
    
    # Get search term
    search_term = gui.search_var.get().lower()
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Get all components of this type
    components = gui.get_component_browser_data(component_type)
    
    # Filter by search term if provided
    if search_term:
        filtered_components = []
        for component in components:
            if (search_term in component["name"].lower() or 
                search_term in component["details"].lower()):
                filtered_components.append(component)
        components = filtered_components
    
    # Add filtered components to browser
    for component in components:
        gui.components_browser.insert('', 'end', values=(
            component["name"],
            component["details"],
            component["performance"],
            component["price"]
        ))
    
    # Update status
    gui.status_bar.config(text=f"Found {len(components)} matching components")

def apply_price_filter(gui):
    """Apply price filter to component browser"""
    # Get selected component type
    component_type = gui.component_type_var.get()
    
    # Get price range
    try:
        min_price = float(gui.price_filter_min_var.get())
        max_price = float(gui.price_filter_max_var.get())
    except ValueError:
        messagebox.showinfo("Invalid Price", "Please enter valid numbers for price range.")
        return
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Get all components of this type
    components = gui.get_component_browser_data(component_type)
    
    # Filter by price range
    filtered_components = []
    for component in components:
        # Parse price string (remove $ and convert to float)
        price = float(component["price"].replace('$', ''))
        if min_price <= price <= max_price:
            filtered_components.append(component)
    
    # Add filtered components to browser
    for component in filtered_components:
        gui.components_browser.insert('', 'end', values=(
            component["name"],
            component["details"],
            component["performance"],
            component["price"]
        ))
    
    # Update status
    gui.status_bar.config(text=f"Found {len(filtered_components)} components in price range")

def apply_brand_filter(gui, event=None):
    """Apply brand filter to component browser"""
    # Get selected component type
    component_type = gui.component_type_var.get()
    
    # Get selected brand
    brand = gui.brand_filter_var.get()
    
    # If "All" selected, reset to show all brands
    if brand == "All":
        gui.update_component_browser()
        return
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Get all components of this type
    components = gui.get_component_browser_data(component_type)
    
    # Filter by brand
    filtered_components = []
    for component in components:
        # Extract brand from name (usually the first word)
        name_parts = component["name"].split()
        if name_parts and name_parts[0] == brand:
            filtered_components.append(component)
    
    # Add filtered components to browser
    for component in filtered_components:
        gui.components_browser.insert('', 'end', values=(
            component["name"],
            component["details"],
            component["performance"],
            component["price"]
        ))
    
    # Update status
    gui.status_bar.config(text=f"Found {len(filtered_components)} {brand} components")

def apply_specific_filters(gui):
    """Apply component-specific filters"""
    # Get selected component type
    component_type = gui.component_type_var.get()
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Get all components of this type
    components = gui.get_component_browser_data(component_type)
    
    # Apply filters based on component type
    filtered_components = components
    
    if component_type == 'cpu':
        # Filter by cores
        try:
            min_cores = int(gui.cpu_cores_var.get())
            temp_filtered = []
            for component in filtered_components:
                # Extract cores from details (e.g., "24 cores, 5.6GHz")
                cores_text = component["details"].split(',')[0].strip()
                try:
                    cores = int(cores_text.split()[0])
                    if cores >= min_cores:
                        temp_filtered.append(component)
                except (ValueError, IndexError):
                    # If can't parse cores, include component anyway
                    temp_filtered.append(component)
            filtered_components = temp_filtered
        except (ValueError, IndexError):
            pass
        
        # Filter by integrated graphics if checked
        if hasattr(gui, 'cpu_igpu_var') and gui.cpu_igpu_var.get():
            filtered_components = [c for c in filtered_components if "iGPU" in c["details"]]
            
    elif component_type == 'gpu':
        # Filter by VRAM
        try:
            min_vram = int(gui.gpu_vram_var.get())
            temp_filtered = []
            for component in filtered_components:
                # Extract VRAM from details (e.g., "24GB GDDR6X")
                vram_text = component["details"].split()[0].strip()
                try:
                    vram = int(vram_text.replace('GB', ''))
                    if vram >= min_vram:
                        temp_filtered.append(component)
                except (ValueError, IndexError):
                    # If can't parse VRAM, include component anyway
                    temp_filtered.append(component)
            filtered_components = temp_filtered
        except (ValueError, IndexError):
            pass
        
        # Filter by ray tracing if checked
        if hasattr(gui, 'gpu_rt_var') and gui.gpu_rt_var.get():
            filtered_components = [c for c in filtered_components if "RTX" in c["name"]]