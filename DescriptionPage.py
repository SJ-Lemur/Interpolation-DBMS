import tkinter as tk
from tkinter import font
from tkinter import PhotoImage

class PolynomialInterpolationPage():

    def __init__(self, root):
        root.configure(bg='#2e2e2e')  # Set background color

        # Create a frame for layout management
        frame = tk.Frame(root, bg='#2e2e2e')
        frame.pack(fill='both')

        # Define custom fonts
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        subtitle_font = font.Font(family="Helvetica", size=18, slant="italic")
        normal_font = font.Font(family="Helvetica", size=14)

        # Add title text
        title_label = tk.Label(
            frame, 
            text="What is Polynomial Interpolation?", 
            font=title_font, 
            fg="#ffffff", 
            bg='#2e2e2e', 
            pady=20
        )
        title_label.pack()

        """
        # Add subtitle text
        subtitle_label = tk.Label(
            frame, 
            text="A simple app to showcase text styles", 
            font=subtitle_font, 
            fg="#00bfff", 
            bg='#2e2e2e'
        )
        subtitle_label.pack()
        """
        # Add normal text
        normal_label = tk.Label(
            frame, 
            text="A process that approximates a polynomial that passes through a set of data points. So the goal here is to find some polynomial that passes through a set of given data points so we can make  estimations of the data points trend or at least study the given points and see what can we learn from the data.", 
            font=normal_font, 
            fg="#ffffff", 
            bg='#2e2e2e', 
            pady=10,
            wraplength=560
        )
        normal_label.pack()

         # Add subtitle text
        subtitle_label = tk.Label(
            frame, 
            text="Example", 
            font=subtitle_font, 
            fg="#00bfff", 
            bg='#2e2e2e'
        )
        subtitle_label.pack()

        # Add another piece of normal text
        another_label = tk.Label(
            frame, 
            text="Interpolation by parabola. The points (0,1), (2,2), and (3,4) are interpolated by the function P(x)=(1/2)x^2 -(1/2)x+1", 
            font=normal_font, 
            fg="#ff5733", 
            bg='#2e2e2e',
            wraplength=560
        )
        another_label.pack()
        #Add the interpolation graph image
        image_label = tk.Label(root)
        image_label.pack(pady=10)

        image_path = "InterpolationExamples/Interpolation.png"
        img = PhotoImage(file=image_path)
        image_label.config(image=img)
        image_label.image = img

        # Start the Tkinter event loop

"""
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Polynomial Interpolation DBMS")
    root.geometry("800x500")
    PolynomialInterpolationPage(root)
"""