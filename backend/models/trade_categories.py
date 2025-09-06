# Nigerian Market Trade Categories
# Comprehensive list of trades and services for the Nigerian marketplace

NIGERIAN_TRADE_CATEGORIES = [
    "Building",
    "Concrete Works", 
    "Tiling",
    "CCTV & Security Systems",
    "Door & Window Installation",
    "Air Conditioning & Refrigeration",
    "Renovations",
    "Relocation/Moving",
    "Painting",
    "Carpentry",
    "General Handyman Work",
    "Bathroom Fitting",
    "Generator Services",
    "Home Extensions",
    "Scaffolding",
    "Waste Disposal",
    "Flooring",
    "Plastering/POP",
    "Cleaning",
    "Electrical Repairs",
    "Solar & Inverter Installation",
    "Plumbing",
    "Welding",
    "Furniture Making",
    "Interior Design",
    "Roofing",
    "Locksmithing",
    "Recycling"
]

# For validation purposes
def validate_trade_category(category: str) -> bool:
    """Validate if a trade category is in the approved list"""
    return category in NIGERIAN_TRADE_CATEGORIES

def get_all_categories() -> list:
    """Get all available trade categories"""
    return NIGERIAN_TRADE_CATEGORIES.copy()

# Category groupings for better UX
TRADE_CATEGORY_GROUPS = {
    "Construction & Building": [
        "Building",
        "Concrete Works",
        "Home Extensions", 
        "Renovations",
        "Scaffolding"
    ],
    "Interior & Finishing": [
        "Tiling",
        "Flooring",
        "Painting",
        "Plastering/POP",
        "Bathroom Fitting",
        "Interior Design",
        "Furniture Making"
    ],
    "Installation & Repair": [
        "Door & Window Installation",
        "Air Conditioning & Refrigeration",
        "CCTV & Security Systems",
        "Solar & Inverter Installation",
        "Generator Services"
    ],
    "Utilities & Systems": [
        "Electrical Repairs",
        "Plumbing",
        "Welding",
        "Locksmithing"
    ],
    "General Services": [
        "General Handyman Work",
        "Carpentry",
        "Roofing",
        "Cleaning",
        "Relocation/Moving",
        "Waste Disposal",
        "Recycling"
    ]
}