# component_browser_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
from algorithm.utils.custom_data_manager import CustomDataManager

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
    component_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_component_browser(gui, e))
    
    # Search bar
    ttk.Label(controls_frame, text="Search:").pack(side=tk.LEFT, padx=10, pady=5)
    gui.search_var = tk.StringVar()
    search_entry = ttk.Entry(controls_frame, textvariable=gui.search_var, width=20)
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    search_button = ctk.CTkButton(controls_frame, text="Search", 
                                command=lambda: search_components(gui))
    search_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Reset filters button
    reset_button = ctk.CTkButton(controls_frame, text="Reset Filters", 
                               command=lambda: reset_component_filters(gui))
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
    apply_price_button = ctk.CTkButton(price_filter_frame, text="Apply", 
                                     command=lambda: apply_price_filter(gui),
                                     width=20)
    apply_price_button.grid(row=0, column=4, padx=5, pady=2)
    
    # Brand filter
    ttk.Label(filters_frame, text="Brand:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    
    gui.brand_filter_var = tk.StringVar(value="All")
    gui.brand_filter_list = ttk.Combobox(filters_frame, textvariable=gui.brand_filter_var, 
                                       values=["All"], width=15)
    gui.brand_filter_list.grid(row=3, column=0, sticky="w", padx=10, pady=2)
    gui.brand_filter_list.bind("<<ComboboxSelected>>", lambda e: apply_brand_filter(gui, e))
    
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
    gui.component_context_menu.add_command(label="View Details", 
                                         command=lambda: view_component_details(gui))
    gui.component_context_menu.add_command(label="Add to Current Build", 
                                         command=lambda: add_component_to_build(gui))
    gui.component_context_menu.add_command(label="Compare with Current", 
                                         command=lambda: compare_with_current(gui))
    
    # Bind context menu
    gui.components_browser.bind("<Button-3>", lambda e: show_component_context_menu(gui, e))
    gui.components_browser.bind("<Double-1>", lambda e: view_component_details(gui))
    
    # Attach functions to the gui object
    gui.update_component_browser = update_component_browser
    gui.search_components = search_components
    gui.apply_price_filter = apply_price_filter
    gui.apply_brand_filter = apply_brand_filter
    gui.reset_component_filters = reset_component_filters
    gui.apply_specific_filters = apply_specific_filters
    gui.view_component_details = view_component_details
    gui.add_component_to_build = add_component_to_build
    gui.compare_with_current = compare_with_current
    
    # Initialize the browser with CPUs
    update_component_browser(gui)


def get_component_browser_data(gui, component_type):
    """Get component data for the browser from the data manager"""
    
    # Use CustomDataManager to get real data
    custom_data_manager = CustomDataManager()
    
    # Mapping of methods to get different component types
    component_getters = {
        'cpu': custom_data_manager.get_cpus,
        'gpu': custom_data_manager.get_gpus,
        'ram': custom_data_manager.get_rams,
        'storage': custom_data_manager.get_storages,
        'motherboard': custom_data_manager.get_motherboards,
        'psu': custom_data_manager.get_psus,
        'cooling': custom_data_manager.get_coolings,
        'case': custom_data_manager.get_cases
    }
    
    # Get the components according to type
    getter = component_getters.get(component_type.lower(), lambda: [])
    components = getter()
    
    # Convert to browser data format
    browser_data = []
    
    for component in components:
        try:
            if component_type == 'cpu':
                browser_data.append({
                    "name": f"{component.maker}",
                    "details": f"Performance: {component.performance}, Power: {component.power_consumption}W",
                    "performance": f"{component.performance}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'gpu':
                if component is None:
                    continue
                browser_data.append({
                    "name": f"{component.maker}",
                    "details": f"Power: {component.power}, Power Consumption: {component.power_consumption}W",
                    "performance": f"{component.power}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'ram':
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"{component.capacity}GB {component.type}-{component.frequency}MHz",
                    "performance": f"{min(100, component.frequency/1000 * 20):.0f}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'storage':
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"{component.capacity}GB {component.type}",
                    "performance": f"{min(100, (50 if component.type == 'SSD' else 20))}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'motherboard':
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"RAM: {component.ram_socket_type}, Max RAM: {component.max_ram_capacity}GB",
                    "performance": f"{min(100, component.max_ram_frequency/100):.0f}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'psu':
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"Capacity: {component.capacity}W",
                    "performance": f"{min(100, component.capacity/15):.0f}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'cooling':
                details = getattr(component, 'type', 'Unknown')
                cooling_capacity = getattr(component, 'cooling_capacity', 100)
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"Type: {details}",
                    "performance": f"{min(100, cooling_capacity/2):.0f}/100",
                    "price": f"${component.price:.2f}"
                })
            elif component_type == 'case':
                browser_data.append({
                    "name": f"{component.maker} {component.model}",
                    "details": f"Max GPU Length: {getattr(component, 'max_gpu_length', 'Unknown')}mm",
                    "performance": "N/A",
                    "price": f"${component.price:.2f}"
                })
        except Exception as e:
            print(f"Error processing {component_type} component: {e}")
            continue
            
    return browser_data


def update_component_browser(gui, event=None):
    """Update the component browser with components of the selected type"""
    # Get selected component type
    component_type = gui.component_type_var.get()
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Update component-specific filters
    update_specific_filters(gui, component_type)
    
    # Get components from data manager
    components = get_component_browser_data(gui, component_type)
    
    # Add components to browser
    for component in components:
        gui.components_browser.insert('', 'end', values=(
            component["name"],
            component["details"],
            component["performance"],
            component["price"]
        ))
    
    # Update brand filter dropdown
    update_brand_filter_list(gui, component_type, components)
    
    # Update status
    gui.status_bar.config(text=f"Showing {len(components)} {component_type.upper()} components")


def update_specific_filters(gui, component_type):
    """Update the component-specific filter options"""
    # Clear existing filters
    for widget in gui.specific_filters_frame.winfo_children():
        widget.destroy()
    
    # Add filters based on component type
    if component_type == 'cpu':
        # Add CPU-specific filters
        ttk.Label(gui.specific_filters_frame, text="Has Integrated GPU:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.cpu_igpu_var = tk.BooleanVar(value=False)
        cpu_igpu_check = ttk.Checkbutton(gui.specific_filters_frame, variable=gui.cpu_igpu_var)
        cpu_igpu_check.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(gui.specific_filters_frame, text="Min Performance:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        gui.cpu_perf_var = tk.StringVar(value="0")
        cpu_perf_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.cpu_perf_var, width=5)
        cpu_perf_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
    elif component_type == 'gpu':
        # Add GPU-specific filters
        ttk.Label(gui.specific_filters_frame, text="Min Power:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        gui.gpu_power_var = tk.StringVar(value="0")
        gpu_power_entry = ttk.Entry(gui.specific_filters_frame, textvariable=gui.gpu_power_var, width=5)
        gpu_power_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
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
    
    # Add apply filters button
    apply_button = ctk.CTkButton(gui.specific_filters_frame, text="Apply Filters", 
                               command=lambda: apply_specific_filters(gui),
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
    components = get_component_browser_data(gui, component_type)
    
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
    components = get_component_browser_data(gui, component_type)
    
    # Filter by price range
    filtered_components = []
    for component in components:
        # Parse price string (remove $ and convert to float)
        try:
            price = float(component["price"].replace('$', ''))
            if min_price <= price <= max_price:
                filtered_components.append(component)
        except ValueError:
            continue
    
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
        update_component_browser(gui)
        return
    
    # Clear existing components
    for item in gui.components_browser.get_children():
        gui.components_browser.delete(item)
    
    # Get all components of this type
    components = get_component_browser_data(gui, component_type)
    
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
    components = get_component_browser_data(gui, component_type)
    
    # Apply filters based on component type
    filtered_components = components
    
    if component_type == 'cpu':
        # Filter by integrated GPU if needed
        if hasattr(gui, 'cpu_igpu_var') and gui.cpu_igpu_var.get():
            filtered_components = [c for c in filtered_components if "Integrated" in c["details"]]
        
        # Filter by performance if provided
        if hasattr(gui, 'cpu_perf_var'):
            try:
                min_perf = int(gui.cpu_perf_var.get())
                temp_filtered = []
                for component in filtered_components:
                    # Extract performance from details
                    perf_text = component["performance"].split('/')[0]
                    try:
                        perf = int(float(perf_text))
                        if perf >= min_perf:
                            temp_filtered.append(component)
                    except (ValueError, IndexError):
                        # If can't parse performance, include component anyway
                        temp_filtered.append(component)
                filtered_components = temp_filtered
            except (ValueError, AttributeError):
                pass
    
    elif component_type == 'gpu':
        # Filter by power if provided
        if hasattr(gui, 'gpu_power_var'):
            try:
                min_power = int(gui.gpu_power_var.get())
                temp_filtered = []
                for component in filtered_components:
                    # Extract power from performance
                    power_text = component["performance"].split('/')[0]
                    try:
                        power = int(float(power_text))
                        if power >= min_power:
                            temp_filtered.append(component)
                    except (ValueError, IndexError):
                        # If can't parse power, include component anyway
                        temp_filtered.append(component)
                filtered_components = temp_filtered
            except (ValueError, AttributeError):
                pass
    
    elif component_type == 'ram':
        # Filter by capacity if provided
        if hasattr(gui, 'ram_capacity_var'):
            try:
                min_capacity = int(gui.ram_capacity_var.get())
                temp_filtered = []
                for component in filtered_components:
                    # Extract capacity from details (e.g., "32GB DDR5-6000")
                    details = component["details"]
                    try:
                        capacity_text = details.split('GB')[0].strip()
                        capacity = int(capacity_text)
                        if capacity >= min_capacity:
                            temp_filtered.append(component)
                    except (ValueError, IndexError):
                        # If can't parse capacity, include component anyway
                        temp_filtered.append(component)
                filtered_components = temp_filtered
            except (ValueError, AttributeError):
                pass
        
        # Filter by RAM type if not "Any"
        if hasattr(gui, 'ram_type_var') and gui.ram_type_var.get() != "Any":
            ram_type = gui.ram_type_var.get()
            filtered_components = [c for c in filtered_components if ram_type in c["details"]]
    
    elif component_type == 'storage':
        # Filter by capacity if provided
        if hasattr(gui, 'storage_capacity_var'):
            try:
                min_capacity = int(gui.storage_capacity_var.get())
                temp_filtered = []
                for component in filtered_components:
                    # Extract capacity from details (e.g., "2TB NVMe SSD")
                    details = component["details"]
                    try:
                        capacity_text = details.split('GB')[0].strip()
                        capacity = int(capacity_text)
                        if capacity >= min_capacity:
                            temp_filtered.append(component)
                    except (ValueError, IndexError):
                        # If can't parse capacity, include component anyway
                        temp_filtered.append(component)
                filtered_components = temp_filtered
            except (ValueError, AttributeError):
                pass
        
        # Filter by storage type if not "Any"
        if hasattr(gui, 'storage_type_var') and gui.storage_type_var.get() != "Any":
            storage_type = gui.storage_type_var.get()
            filtered_components = [c for c in filtered_components if storage_type in c["details"]]
    
    # Add filtered components to browser
    for component in filtered_components:
        gui.components_browser.insert('', 'end', values=(
            component["name"],
            component["details"],
            component["performance"],
            component["price"]
        ))
    
    # Update status
    gui.status_bar.config(text=f"Found {len(filtered_components)} components after applying filters")


def reset_component_filters(gui):
    """Reset all component filters to defaults"""
    # Reset price filter
    gui.price_filter_min_var.set("0")
    gui.price_filter_max_var.set("50000")
    
    # Reset brand filter
    gui.brand_filter_var.set("All")
    
    # Reset search field
    gui.search_var.set("")
    
    # Reset component-specific filters
    component_type = gui.component_type_var.get()
    if component_type == 'cpu':
        if hasattr(gui, 'cpu_igpu_var'):
            gui.cpu_igpu_var.set(False)
        if hasattr(gui, 'cpu_perf_var'):
            gui.cpu_perf_var.set("0")
    elif component_type == 'gpu':
        if hasattr(gui, 'gpu_power_var'):
            gui.gpu_power_var.set("0")
    elif component_type == 'ram':
        if hasattr(gui, 'ram_capacity_var'):
            gui.ram_capacity_var.set("0")
        if hasattr(gui, 'ram_type_var'):
            gui.ram_type_var.set("Any")
    elif component_type == 'storage':
        if hasattr(gui, 'storage_capacity_var'):
            gui.storage_capacity_var.set("0")
        if hasattr(gui, 'storage_type_var'):
            gui.storage_type_var.set("Any")
    
    # Refresh the component browser
    update_component_browser(gui)
    
    # Update status
    gui.status_bar.config(text="Filters reset to defaults")


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


def view_component_details(gui):
    """View details of selected component in browser"""
    selection = gui.components_browser.selection()
    if not selection:
        return
        
    # Get selected item
    item = gui.components_browser.item(selection[0])
    values = item['values']
    
    # Create details dialog
    details_dialog = ctk.CTkToplevel(gui.master)
    details_dialog.title(f"Component Details: {values[0]}")
    details_dialog.geometry("500x400")
    details_dialog.transient(gui.master)
    details_dialog.grab_set()
    
    # Create details text
    details_text = scrolledtext.ScrolledText(details_dialog, wrap=tk.WORD, width=60, height=20)
    details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add component details
    details_text.insert(tk.END, f"Name: {values[0]}\n\n", "heading")
    details_text.insert(tk.END, f"Details: {values[1]}\n\n")
    details_text.insert(tk.END, f"Performance: {values[2]}\n\n")
    details_text.insert(tk.END, f"Price: {values[3]}\n\n")
    
    # Add additional information based on component type
    component_type = gui.component_type_var.get()
    details_text.insert(tk.END, "Additional Information:\n", "heading")
    
    if component_type == 'cpu':
        details_text.insert(tk.END, "CPUs provide the primary processing power for your system.\n")
        details_text.insert(tk.END, "Higher performance scores generally mean better overall speed.\n")
        details_text.insert(tk.END, "Consider power consumption for thermal and PSU requirements.\n")
    elif component_type == 'gpu':
        details_text.insert(tk.END, "GPUs handle graphics processing and some compute workloads.\n")
        details_text.insert(tk.END, "Higher power values typically mean better gaming performance.\n")
        details_text.insert(tk.END, "Consider power consumption requirements when selecting a PSU.\n")
    elif component_type == 'ram':
        details_text.insert(tk.END, "RAM provides temporary working memory for your system.\n")
        details_text.insert(tk.END, "Higher capacity allows for more simultaneous tasks.\n")
        details_text.insert(tk.END, "Higher frequency generally provides better performance.\n")
    elif component_type == 'storage':
        details_text.insert(tk.END, "Storage devices provide permanent data storage.\n")
        details_text.insert(tk.END, "SSDs provide much faster access than HDDs.\n")
        details_text.insert(tk.END, "NVMe SSDs are faster than SATA SSDs for most tasks.\n")
    
    # Add styling
    details_text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
    
    # Disable editing
    details_text.config(state=tk.DISABLED)
    
    # Add close button
    close_button = ctk.CTkButton(details_dialog, text="Close", 
                               command=details_dialog.destroy)
    close_button.pack(pady=10)


def add_component_to_build(gui):
    """Add selected component from browser to current build"""
    selection = gui.components_browser.selection()
    if not selection:
        return
        
    # Get selected item
    item = gui.components_browser.item(selection[0])
    values = item['values']
    
    # Check if we have a current computer
    if not hasattr(gui, 'current_computer'):
        messagebox.showinfo("No Computer", "Please generate a computer first.")
        return
        
    # Get component type
    component_type = gui.component_type_var.get()
    
    # Confirm replacement
    confirm = messagebox.askyesno("Confirm Addition", 
                                f"Do you want to replace the current {component_type} with {values[0]}?")
    
    if confirm:
        # This would update the computer object in a complete implementation
        messagebox.showinfo("Component Added", 
                          f"The {component_type} would be replaced with {values[0]} ({values[3]}).\n\n"
                          "This feature will be fully implemented in a future update.")
        gui.status_bar.config(text=f"Added {values[0]} to build")


def compare_with_current(gui):
    """Compare selected component with current build's component"""
    selection = gui.components_browser.selection()
    if not selection:
        return
        
    # Get selected item
    item = gui.components_browser.item(selection[0])
    values = item['values']
    
    # Check if we have a current computer
    if not hasattr(gui, 'current_computer'):
        messagebox.showinfo("No Computer", "Please generate a computer first.")
        return
        
    # Get component type
    component_type = gui.component_type_var.get()
    
    # Create comparison dialog
    compare_dialog = ctk.CTkToplevel(gui.master)
    compare_dialog.title(f"Component Comparison: {component_type}")
    compare_dialog.geometry("700x500")
    compare_dialog.transient(gui.master)
    compare_dialog.grab_set()
    
    # Create comparison frame
    compare_frame = ttk.Frame(compare_dialog)
    compare_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Configure grid
    compare_frame.grid_columnconfigure(0, weight=1)
    compare_frame.grid_columnconfigure(1, weight=1)
    
    # Add headers
    ttk.Label(compare_frame, text="Current Component", font=("TkDefaultFont", 12, "bold")).grid(
        row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(compare_frame, text="Selected Component", font=("TkDefaultFont", 12, "bold")).grid(
        row=0, column=1, sticky="w", padx=10, pady=5)
    
    # Create component details text areas
    current_text = scrolledtext.ScrolledText(compare_frame, wrap=tk.WORD, width=40, height=20)
    current_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    selected_text = scrolledtext.ScrolledText(compare_frame, wrap=tk.WORD, width=40, height=20)
    selected_text.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    
    # Get current component details
    current_component_text = "No current component available."
    current_component = None
    
    if component_type == 'cpu':
        current_component = gui.current_computer.cpu
    elif component_type == 'gpu':
        current_component = gui.current_computer.gpu
    elif component_type == 'ram':
        current_component = gui.current_computer.ram
    elif component_type == 'storage':
        current_component = gui.current_computer.storage
    elif component_type == 'motherboard':
        current_component = gui.current_computer.motherboard
    elif component_type == 'psu':
        current_component = gui.current_computer.psu
    elif component_type == 'cooling':
        current_component = gui.current_computer.cooling
    elif component_type == 'case':
        current_component = gui.current_computer.case
    
    # Add current component details
    if current_component:
        current_text.insert(tk.END, f"Name: {str(current_component)}\n\n", "heading")
        
        # Get all attributes
        attributes = vars(current_component)
        
        # Insert all attributes
        current_text.insert(tk.END, "Specifications:\n", "heading")
        for key, value in attributes.items():
            # Skip certain attributes for readability
            if key in ['fitness']:
                continue
            
            # Format the key name
            formatted_key = key.replace('_', ' ').title()
            
            # Format the value based on type
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            elif isinstance(value, bool):
                formatted_value = "Yes" if value else "No"
            else:
                formatted_value = str(value)
            
            current_text.insert(tk.END, f"{formatted_key}: {formatted_value}\n")
    else:
        current_text.insert(tk.END, current_component_text)
    
    # Add selected component details
    selected_text.insert(tk.END, f"Name: {values[0]}\n\n", "heading")
    selected_text.insert(tk.END, f"Details: {values[1]}\n\n")
    selected_text.insert(tk.END, f"Performance: {values[2]}\n\n")
    selected_text.insert(tk.END, f"Price: {values[3]}\n\n")
    
    # Add styling
    current_text.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
    selected_text.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
    
    # Disable editing
    current_text.config(state=tk.DISABLED)
    selected_text.config(state=tk.DISABLED)
    
    # Add comparison metrics
    metrics_frame = ttk.LabelFrame(compare_dialog, text="Comparison Metrics")
    metrics_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Use a grid for metrics
    metrics_frame.grid_columnconfigure(0, weight=1)
    metrics_frame.grid_columnconfigure(1, weight=1)
    metrics_frame.grid_columnconfigure(2, weight=1)
    
    # Add metric headers
    ttk.Label(metrics_frame, text="Metric", font=("TkDefaultFont", 10, "bold")).grid(
        row=0, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(metrics_frame, text="Current", font=("TkDefaultFont", 10, "bold")).grid(
        row=0, column=1, sticky="w", padx=5, pady=2)
    ttk.Label(metrics_frame, text="Selected", font=("TkDefaultFont", 10, "bold")).grid(
        row=0, column=2, sticky="w", padx=5, pady=2)
    
    # Add buttons
    buttons_frame = ttk.Frame(compare_dialog)
    buttons_frame.pack(fill=tk.X, pady=10)
    
    replace_button = ctk.CTkButton(buttons_frame, text="Replace Component", 
                                 command=lambda: replace_component(gui, compare_dialog, 
                                                                component_type, values))
    replace_button.pack(side=tk.RIGHT, padx=10)
    
    close_button = ctk.CTkButton(buttons_frame, text="Close", 
                               command=compare_dialog.destroy)
    close_button.pack(side=tk.RIGHT, padx=10)


def replace_component(gui, dialog, component_type, values):
    """Replace component from comparison dialog"""
    # This would normally update the computer object
    # For now, just show a message
    messagebox.showinfo("Component Replaced", 
                      f"The {component_type} would be replaced with {values[0]} ({values[3]}).\n\n"
                      "This feature will be fully implemented in a future update.")
    
    # Close the dialog
    dialog.destroy()
    
    # Update status
    gui.status_bar.config(text=f"Replaced {component_type} with {values[0]}")