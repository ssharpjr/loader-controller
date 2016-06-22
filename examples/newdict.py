# instead of

    if color == 'red':
        lcd.set_color(1.0, 0.0, 0.0)  # Red
    elif color == 'green':
        lcd.set_color(0.0, 1.0, 0.0)  # Green
    elif color == 'blue':
        lcd.set_color(0.0, 0.0, 1.0)  # Blue
    elif color == 'white':
        lcd.set_color(1.0, 1.0, 1.0)  # White
    elif color == 'off':
        lcd.set_color(0.0, 0.0, 0.0)  # Off
    else:
        lcd.set_color(0.0, 0.0, 0.0)  # Off

# you may use

colors = {
        'red': (1.0, 0.0, 0.0),
        'green': (0.0, 1.0, 0.0),
        ...
        'off': (0.0, 0.0, 0.0),
        }

    c = colors.get(color, colors['off'])
    lcd.set_color(*c)
