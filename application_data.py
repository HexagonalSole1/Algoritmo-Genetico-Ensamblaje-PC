"""
Base de datos de requisitos recomendados para aplicaciones específicas.
"""

# Diccionario de aplicaciones por categoría
APPLICATION_DATA = {
    "juegos": {
        "fortnite": {
            "name": "Fortnite",
            "requirements": {
                "cpu": {
                    "performance_min": 40,
                    "cores_min": 4,
                    "recommended_models": ["Intel i5-7300U", "AMD Ryzen 3 3300X"]
                },
                "gpu": {
                    "power_min": 40,
                    "vram_min": 4,
                    "recommended_models": ["NVIDIA GTX 1060", "AMD Radeon RX 570"]
                },
                "ram": {
                    "capacity_min": 8,
                    "frequency_min": 2666
                },
                "storage": {
                    "capacity_min": 100,
                    "type": "SSD"
                }
            },
            "performance_targets": {
                "resolution": "1080p",
                "fps_target": 60,
                "quality_preset": "Medium"
            }
        },
        "valorant": {
            "name": "Valorant",
            "requirements": {
                "cpu": {
                    "performance_min": 30,
                    "cores_min": 4
                },
                "gpu": {
                    "power_min": 30,
                    "vram_min": 1
                },
                "ram": {
                    "capacity_min": 4
                },
                "storage": {
                    "capacity_min": 20
                }
            }
        },
        "warzone": {
            "name": "Call of Duty: Warzone",
            "requirements": {
                "cpu": {
                    "performance_min": 55,
                    "cores_min": 6
                },
                "gpu": {
                    "power_min": 60,
                    "vram_min": 8
                },
                "ram": {
                    "capacity_min": 16
                },
                "storage": {
                    "capacity_min": 175
                }
            }
        }
    },
    "diseño gráfico": {
        "photoshop": {
            "name": "Adobe Photoshop",
            "requirements": {
                "cpu": {"performance_min": 50},
                "ram": {"capacity_min": 16},
                "gpu": {"power_min": 30}
            }
        },
        "illustrator": {
            "name": "Adobe Illustrator",
            "requirements": {
                "cpu": {"performance_min": 45},
                "ram": {"capacity_min": 16},
                "gpu": {"power_min": 25}
            }
        }
    },
    "edición de video": {
        "premiere": {
            "name": "Adobe Premiere Pro",
            "requirements": {
                "cpu": {"performance_min": 60},
                "gpu": {"power_min": 50},
                "ram": {"capacity_min": 32}
            }
        },
        "davinci": {
            "name": "DaVinci Resolve",
            "requirements": {
                "cpu": {"performance_min": 65},
                "gpu": {"power_min": 60},
                "ram": {"capacity_min": 32}
            }
        }
    }
}

def get_applications_for_category(category):
    """Obtiene las aplicaciones disponibles para una categoría"""
    category_data = APPLICATION_DATA.get(category, {})
    return [{"id": app_id, "name": app_data["name"]} for app_id, app_data in category_data.items()]

def get_application_requirements(category, app_id):
    """Obtiene los requisitos para una aplicación específica"""
    if category in APPLICATION_DATA and app_id in APPLICATION_DATA[category]:
        return APPLICATION_DATA[category][app_id]
    return None