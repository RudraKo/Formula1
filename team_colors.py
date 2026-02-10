"""F1 Team Color Mappings and Visual Constants"""

# Team Colors (Hex codes)
TEAM_COLORS = {
    'Mercedes': '#00D2BE',
    'Ferrari': '#DC0000',
    'Red Bull': '#1E41FF',
    'McLaren': '#FF8700',
    'Alpine': '#0090FF',
    'Aston Martin': '#006F62',
    'AlphaTauri': '#2B4562',
    'Alfa Romeo': '#900000',
    'Haas F1 Team': '#FFFFFF',
    'Williams': '#005AFF',
    # Legacy teams
    'Force India': '#F596C8',
    'Racing Point': '#F596C8',
    'Renault': '#FFF500',
    'Toro Rosso': '#469BFF',
    'Sauber': '#9B0000',
    'Manor Marussia': '#6E0000',
    'Lotus F1': '#FFB800',
    'Caterham': '#005030',
    'Brawn': '#66FF00',
    'Toyota': '#EF1A2D',
    'BMW Sauber': '#1E5BC6',
    'Honda': '#FFFFFF',
    'Super Aguri': '#EF1A2D',
    'Spyker': '#FF8200',
    'MF1': '#EF1A2D',
}

# Status badge colors
STATUS_COLORS = {
    'win': '#FFD700',  # Gold
    'podium': '#C0C0C0',  # Silver
    'dnf': '#FF1801',  # Red
    'fastest_lap': '#00D2BE',  # Cyan
    'pole': '#FFD700',  # Gold
}

# Performance tier colors
PERFORMANCE_COLORS = {
    'excellent': '#00FF00',
    'good': '#7FFF00',
    'average': '#FFD700',
    'poor': '#FF8C00',
    'bad': '#FF1801'
}

def get_team_color(team_name):
    """Get team color with fallback to F1 red"""
    return TEAM_COLORS.get(team_name, '#FF1801')

def get_performance_color(metric_value, thresholds):
    """
    Get performance color based on metric value and thresholds
    
    Args:
        metric_value: The value to evaluate
        thresholds: dict with 'excellent', 'good', 'average', 'poor' threshold values
    
    Returns:
        Color hex code
    """
    if metric_value >= thresholds.get('excellent', 0.8):
        return PERFORMANCE_COLORS['excellent']
    elif metric_value >= thresholds.get('good', 0.6):
        return PERFORMANCE_COLORS['good']
    elif metric_value >= thresholds.get('average', 0.4):
        return PERFORMANCE_COLORS['average']
    elif metric_value >= thresholds.get('poor', 0.2):
        return PERFORMANCE_COLORS['poor']
    else:
        return PERFORMANCE_COLORS['bad']
