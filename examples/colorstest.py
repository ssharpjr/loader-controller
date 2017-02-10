def colortest(color):
    colors = {
        'red': (1.0, 0.0, 0.0),
        'green': (0.0, 1.0, 0.0),
        'blue': (0.0, 0.0, 1.0),
        'white': (1.0, 1.0, 1.0),
        'off': (0.0, 0.0, 0.0)
        }

    c = colors.get(color)
    print(color + " = " + str(c))


if __name__ == '__main__':
    color = colortest('red')
