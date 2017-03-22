import numpy
from PIL import Image, ImageDraw
import imageio
import os

def create_lorenz(iterations, dt):
    points = []
    points.append([0.1, 0, 0]) #starting coordinates

    #constants in a canonical lorenz attractor
    a = 10.0
    b = 28.0
    c = 8/3

    for i in range(iterations):
        x0, y0, z0 = points[-1]

        #update lorenz system of equations
        x = x0 + dt * a * (y0 - x0)
        y = y0 + dt * (x0 * (b - z0) - y0)
        z = z0 + dt * (x0 * y0 - c * z0)
        points.append((x, y, z))

    return points


def draw(points, bounds, width, height):
    xmin, xmax, ymin, ymax = bounds
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)

    for i in range(len(points)):
        x, y, z = points[i]
        ix = width * (x - xmin) / (xmax - xmin)
        iy = height * (y - ymin) / (ymax - ymin)
        if i > 100: #we want to draw only after the system has stabilized a little
            draw.point([ix, iy], fill='red')
    return image


def rotate_y(points, theta):
    new_points = []

    sinY = numpy.sin(theta)
    cosY = numpy.cos(theta)
    for x, y, z in points:
        x = x * cosY + z * sinY
        z = -x * sinY + z * cosY
        new_points.append([x, y, z])

    return new_points

def translate(points, dx, dy, dz):
    new_points = []
    for x, y, z in points:
        new_points.append([x+dx, y+dy, z+dz])
    return new_points


attractor = create_lorenz(50000, .01)
attractor = translate(attractor, 0, 0, -20)

n = 60
images = []

if not os.path.exists("output"):
        os.makedirs("output")

for i in range(0, n):
    print(i)
    points = rotate_y(attractor, (i/n) * (numpy.pi*2))

    #using some magic numbers for the drawing bounds, found by trial and error
    image = draw(points, [-35, 35, -27, 27], 500, 500)
    image.save("output/%03d"%i + ".jpg", "JPEG")
    images.append(imageio.imread("output/%03d"%i + ".jpg"))

print("Saving image sequence...")
imageio.mimsave('lorenz.gif', images, 'GIF', **{'duration': 1/15})