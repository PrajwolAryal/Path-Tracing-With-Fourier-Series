import math
import cmath
import pygame as pg

def init():
    """Initialization calls"""
    pg.init()
    screen = pg.display.set_mode((800, 600), flags=pg.RESIZABLE)
    return screen, pg.time.Clock()

def coords(x, y, screen):
    """Used to translate the coordinates origin to the center of the screen"""
    return screen.get_width() // 2 + x, screen.get_height() // 2 + y

def dft(signal):
    result = []
    N = len(signal)
    for k in range(N):
        sum = 0+0j
        for n in range(N):
            cnum = signal[n][0]+signal[n][1]*1j
            phi = (2 * math.pi * k * n) / N
            sum += cnum*(math.cos(phi)-math.sin(phi)*1j)
        sum /= N
        amplitude = math.sqrt(sum.real ** 2 + sum.imag ** 2)
        phase = math.atan2(sum.imag, sum.real)

        result.append({
            'x': sum.real,
            'y': sum.imag,
            'frequency': k,
            'amplitude': amplitude,
            'phase': phase
        })

    return sorted(result, key=lambda x: x['amplitude'], reverse=True)

def read_points(filename='contourcoordinates.txt'):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():  # Ignore blank lines
                point = tuple(map(int, line.strip()[1:-2].split(',')))
                points.append(point)
    return points

drawing = read_points()
Signal = [[point[0],point[1]] for point in drawing]

fourier = dft(Signal)

def epi_cycles(screen, x, y, rotation, fourier, time, color):
    for component in fourier:
        prev_x, prev_y = x, y
        freq = component['frequency']
        radius = component['amplitude']
        phase = component['phase']
        x += radius * math.cos(freq * time + phase + rotation)
        y += radius * math.sin(freq * time + phase + rotation)

        pg.draw.circle(screen, color, coords(prev_x, prev_y, screen), radius, 2)
        pg.draw.line(screen, (100, 100, 100), coords(prev_x, prev_y, screen), coords(x, y, screen), 2)
    return x, y

def mainloop(screen: pg.Surface, main_clock: pg.time.Clock):
    background_color = "black"
    run = True

    time = 0
    path = []

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        screen.fill(background_color)

        v1x, v1y = epi_cycles(screen, -200, -100, 0, fourier, time, (100,0,0))
        i = 0
        path.insert(0, (v1x, v1y + 150))
        if len(path) > len(fourier):
            path.pop()
        pg.draw.line(screen, (100, 100, 100), coords(v1x, v1y, screen), coords(path[i][0], path[i][1], screen), 3)
        i += 1

           
        for i in range(1, len(path)):
         pg.draw.line(screen, (100, 100, 100), coords(path[i - 1][0], path[i - 1][1], screen), coords(path[i][0], path[i][1], screen), 3)

        
        dt = (2 * math.pi) / len(fourier)
        time += dt

        pg.display.flip()
        main_clock.tick(100)

def main():
    mainloop(*init())
    pg.quit()

if __name__ == "__main__":
    main()
