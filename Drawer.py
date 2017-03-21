from PIL import Image, ImageDraw
from Attractor import Attractor

def draw(thing, image_width, image_height, file_name):
    image = Image.new("RGBA", (image_width, image_height))
    draw = ImageDraw.Draw(image)

    for i in range(len(thing.points)):
        x, y, z = thing.points[i]
        ix = image_width * (x - thing.xmin) / (thing.xmax - thing.xmin)
        iy = image_height * (y - thing.ymin) / (thing.ymax - thing.ymin)
        if i > 100:
            draw.point([ix, iy], fill="black")
    image.save(file_name + ".png", "PNG")

def create_attractor(iterations, dt):
    attr = Attractor()
    attr.points.append([0.1, 0, 0]) #starting coordinates

    #constants in lorenz attractor
    a = 10.0
    b = 28.0
    c = 8/3

    for i in range(iterations):
        x0, y0, z0 = attr.points[-1]

        #update system of equations
        x = x0 + dt * a * (y0 - x0)
        y = y0 + dt * (x0 * (b - z0) - y0)
        z = z0 + dt * (x0 * y0 - c * z0)
        attr.points.append((x, y, z))
        attr.update_bounds(x, y)
    return attr


attractor = create_attractor(50000, .01)
draw(attractor, 800, 800, "test")