def validate_application_requirements(computer, app_requirements):
    """
    Valida si una configuración de computadora cumple con los requisitos de una aplicación.
    
    Args:
        computer (Computer): La configuración de computadora a validar
        app_requirements (dict): Requisitos de la aplicación
    
    Returns:
        dict: Resultados de la validación con detalles de cumplimiento
    """
    validation_results = {
        "overall_compatible": True,
        "details": {}
    }
    
    # Validar requisitos de CPU
    if 'cpu' in app_requirements:
        cpu_reqs = app_requirements['cpu']
        cpu_validation = {
            "compatible": True,
            "messages": []
        }
        
        if 'performance_min' in cpu_reqs:
            if computer.cpu.performance < cpu_reqs['performance_min']:
                cpu_validation["compatible"] = False
                cpu_validation["messages"].append(
                    f"Rendimiento de CPU insuficiente. Requiere: {cpu_reqs['performance_min']}, Actual: {computer.cpu.performance}"
                )
        
        if 'cores_min' in cpu_reqs:
            if computer.cpu.cores < cpu_reqs['cores_min']:
                cpu_validation["compatible"] = False
                cpu_validation["messages"].append(
                    f"Número de núcleos insuficiente. Requiere: {cpu_reqs['cores_min']}, Actual: {computer.cpu.cores}"
                )
        
        validation_results["details"]["cpu"] = cpu_validation
        validation_results["overall_compatible"] &= cpu_validation["compatible"]
    
    # Validar requisitos de GPU
    if 'gpu' in app_requirements:
        gpu_reqs = app_requirements['gpu']
        gpu_validation = {
            "compatible": True,
            "messages": []
        }
        
        # Si no hay GPU dedicada, usar información de gráficos integrados
        gpu_power = computer.gpu.power if computer.gpu else computer.cpu.integrated_graphics_power
        gpu_vram = computer.gpu.vram if computer.gpu else 0
        
        if 'power_min' in gpu_reqs:
            if gpu_power < gpu_reqs['power_min']:
                gpu_validation["compatible"] = False
                gpu_validation["messages"].append(
                    f"Potencia de GPU insuficiente. Requiere: {gpu_reqs['power_min']}, Actual: {gpu_power}"
                )
        
        if 'vram_min' in gpu_reqs:
            if gpu_vram < gpu_reqs['vram_min']:
                gpu_validation["compatible"] = False
                gpu_validation["messages"].append(
                    f"VRAM insuficiente. Requiere: {gpu_reqs['vram_min']} GB, Actual: {gpu_vram} GB"
                )
        
        validation_results["details"]["gpu"] = gpu_validation
        validation_results["overall_compatible"] &= gpu_validation["compatible"]
    
    # Validar requisitos de RAM
    if 'ram' in app_requirements:
        ram_reqs = app_requirements['ram']
        ram_validation = {
            "compatible": True,
            "messages": []
        }
        
        if 'capacity_min' in ram_reqs:
            if computer.ram.capacity < ram_reqs['capacity_min']:
                ram_validation["compatible"] = False
                ram_validation["messages"].append(
                    f"Capacidad de RAM insuficiente. Requiere: {ram_reqs['capacity_min']} GB, Actual: {computer.ram.capacity} GB"
                )
        
        if 'frequency_min' in ram_reqs:
            if computer.ram.frequency < ram_reqs['frequency_min']:
                ram_validation["compatible"] = False
                ram_validation["messages"].append(
                    f"Frecuencia de RAM insuficiente. Requiere: {ram_reqs['frequency_min']} MHz, Actual: {computer.ram.frequency} MHz"
                )
        
        validation_results["details"]["ram"] = ram_validation
        validation_results["overall_compatible"] &= ram_validation["compatible"]
    
    # Validar requisitos de almacenamiento
    if 'storage' in app_requirements:
        storage_reqs = app_requirements['storage']
        storage_validation = {
            "compatible": True,
            "messages": []
        }
        
        if 'capacity_min' in storage_reqs:
            if computer.storage.capacity < storage_reqs['capacity_min']:
                storage_validation["compatible"] = False
                storage_validation["messages"].append(
                    f"Capacidad de almacenamiento insuficiente. Requiere: {storage_reqs['capacity_min']} GB, Actual: {computer.storage.capacity} GB"
                )
        
        if 'type' in storage_reqs:
            if computer.storage.type.lower() != storage_reqs['type'].lower():
                storage_validation["compatible"] = False
                storage_validation["messages"].append(
                    f"Tipo de almacenamiento incorrecto. Requiere: {storage_reqs['type']}, Actual: {computer.storage.type}"
                )
        
        validation_results["details"]["storage"] = storage_validation
        validation_results["overall_compatible"] &= storage_validation["compatible"]
    
    return validation_results

def display_validation_results(validation_results):
    """
    Genera un mensaje de texto con los resultados de la validación.
    
    Args:
        validation_results (dict): Resultados de la validación
    
    Returns:
        str: Mensaje de texto con los resultados
    """
    if validation_results["overall_compatible"]:
        message = "✅ ¡La configuración CUMPLE con todos los requisitos!\n\n"
    else:
        message = "❌ La configuración NO CUMPLE con algunos requisitos:\n\n"
    
    for component, details in validation_results["details"].items():
        if details["compatible"]:
            message += f"✅ {component.upper()} - Compatible\n"
        else:
            message += f"❌ {component.upper()} - Incompatible\n"
            for issue in details["messages"]:
                message += f"   • {issue}\n"
        message += "\n"
    
    return message