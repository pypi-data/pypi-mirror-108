import os, sys, io
from tkinter import *
from PIL import Image, ImageEnhance


def set_white_level(pixel, level):
    if sum(pixel) > level * 255 * 3:
        return (255, 255, 255)
    else:
        return pixel


def autocrop(image):
    box = [0, 0, 0, 0]

    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) != (255, 255, 255):
                box[0] = x
                break
        else:
            continue
        break

    for x in range(image.width - 1, -1, -1):
        for y in range(image.height):
            if image.getpixel((x, y)) != (255, 255, 255):
                box[2] = x
                break
        else:
            continue
        break

    for y in range(image.height):
        for x in range(image.width):
            if image.getpixel((x, y)) != (255, 255, 255):
                box[1] = y
                break
        else:
            continue
        break

    for y in range(image.height - 1, -1, -1):
        for x in range(image.width):
            if image.getpixel((x, y)) != (255, 255, 255):
                box[3] = y
                break
        else:
            continue
        break

    return image.crop(tuple(box))


def apply_filters(im, values):
    if values["brightness"].get() != 1.0:
        im = ImageEnhance.Brightness(im).enhance(values["brightness"].get())
    if values["contrast"].get() != 1.0:
        im = ImageEnhance.Contrast(im).enhance(values["contrast"].get())
    if values["saturation"].get() != 1.0:
        im = ImageEnhance.Color(im).enhance(values["saturation"].get())
    if values["sharpness"].get() != 1.0:
        im = ImageEnhance.Sharpness(im).enhance(values["sharpness"].get())
    if values["white"].get() != 1.0:
        im.putdata([set_white_level(p, values["white"].get()) for p in im.getdata()])
    im = autocrop(im)

    return im


def main():
    window = Tk()

    values = {
        "brightness": DoubleVar(window, 1.0),
        "contrast": DoubleVar(window, 1.0),
        "saturation": DoubleVar(window, 1.0),
        "sharpness": DoubleVar(window, 1.0),
        "white": DoubleVar(window, 1.0),
    }

    im_orig = Image.open(sys.argv[1])
    im_orig.thumbnail((400, 300))

    def run():
        print("Running batch conversion...")
        for file in sys.argv[1:]:
            print(f"Converting {file}...")
            im = apply_filters(Image.open(file), values)
            im.save(file)

    def update(e=None):
        im = apply_filters(im_orig, values)
        b = io.BytesIO()
        im.save(b, "PPM")

        photoimage = PhotoImage(data=b.getvalue())
        img.configure(image=photoimage)
        img.image = photoimage

    window.title("imbaedit")

    img = Label(window, width=400, height=300)
    img.grid(column=0, row=0)

    Scale(
        window,
        from_=0.0,
        to=2.0,
        resolution=0.01,
        orient=HORIZONTAL,
        variable=values["brightness"],
        label="Brightness",
        command=update,
    ).grid(column=0, row=1)

    Scale(
        window,
        from_=0.0,
        to=2.0,
        resolution=0.01,
        orient=HORIZONTAL,
        variable=values["contrast"],
        label="Contrast",
        command=update,
    ).grid(column=0, row=2)

    Scale(
        window,
        from_=0.0,
        to=2.0,
        resolution=0.01,
        orient=HORIZONTAL,
        variable=values["saturation"],
        label="Saturation",
        command=update,
    ).grid(column=0, row=3)

    Scale(
        window,
        from_=0.0,
        to=2.0,
        resolution=0.01,
        orient=HORIZONTAL,
        variable=values["sharpness"],
        label="Sharpness",
        command=update,
    ).grid(column=0, row=4)

    Scale(
        window,
        from_=0.0,
        to=2.0,
        resolution=0.01,
        orient=HORIZONTAL,
        variable=values["white"],
        label="White",
        command=update,
    ).grid(column=0, row=5)

    btn = Button(window, text="Run", font=("Arial Bold", 16), command=run)
    btn.grid(column=0, row=6)

    update()

    window.mainloop()


if __name__ == "__main__":
    main()
