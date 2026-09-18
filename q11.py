# ============================================================
# Q11: INTERACTIVE IMAGE TRANSFORMATION TOOLBOX
# VS CODE VERSION
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import filedialog


# ============================================================
# STEP 1: UPLOAD / SELECT IMAGE
# ============================================================

print("Select a JPG or PNG image.")

# Create tkinter window
root = tk.Tk()

# Hide the main tkinter window
root.withdraw()

# Open file selection window
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[
        ("Image Files", "*.jpg *.jpeg *.png"),
        ("All Files", "*.*")
    ]
)


# Check whether user selected an image
if not file_path:
    print("No image selected!")
    exit()


# Load original image
original_image = Image.open(file_path).convert("RGB")

# Current working image
current_image = original_image.copy()

print("\nImage uploaded successfully!")


# ============================================================
# FUNCTION: DISPLAY IMAGE
# ============================================================

def display_image(image, title):

    plt.figure(figsize=(8, 6))

    plt.imshow(image)

    plt.title(title)

    plt.axis("off")

    plt.show()


# Display original image
display_image(
    original_image,
    "Original Image"
)


# ============================================================
# FUNCTION: MATRIX TRANSFORMATION
#
# Pixel coordinates are treated relative
# to the centre of the image.
# ============================================================

def matrix_transform(image, A):

    # Convert PIL image to NumPy array
    image_array = np.array(image)

    # Get image dimensions
    height, width = image_array.shape[:2]


    # Image centre
    cx = width / 2
    cy = height / 2


    # ========================================================
    # FIND IMAGE CORNERS RELATIVE TO IMAGE CENTRE
    # ========================================================

    corners = np.array([
        [-cx, -cy],
        [ cx, -cy],
        [-cx,  cy],
        [ cx,  cy]
    ])


    # ========================================================
    # TRANSFORM CORNERS
    #
    # x' = A x
    # ========================================================

    transformed_corners = (A @ corners.T).T


    # ========================================================
    # FIND NEW IMAGE BOUNDARIES
    # ========================================================

    min_x = transformed_corners[:, 0].min()
    max_x = transformed_corners[:, 0].max()

    min_y = transformed_corners[:, 1].min()
    max_y = transformed_corners[:, 1].max()


    # ========================================================
    # CALCULATE NEW IMAGE SIZE
    # ========================================================

    new_width = int(np.ceil(max_x - min_x)) + 1

    new_height = int(np.ceil(max_y - min_y)) + 1


    # Prevent invalid size
    new_width = max(new_width, 1)
    new_height = max(new_height, 1)


    # ========================================================
    # CREATE OUTPUT IMAGE
    # ========================================================

    output = np.zeros(
        (new_height, new_width, 3),
        dtype=np.uint8
    )


    # ========================================================
    # FIND INVERSE MATRIX
    # ========================================================

    # If matrix is invertible
    if abs(np.linalg.det(A)) > 1e-10:

        A_inv = np.linalg.inv(A)

    # If matrix is singular
    else:

        A_inv = np.linalg.pinv(A)


    # ========================================================
    # INVERSE MAPPING
    #
    # For every output pixel, find the corresponding
    # pixel in the original image.
    # ========================================================

    for y_new in range(new_height):

        for x_new in range(new_width):


            # Coordinate relative to transformed origin
            transformed_point = np.array([
                x_new + min_x,
                y_new + min_y
            ])


            # Find original coordinate
            original_point = A_inv @ transformed_point


            # Convert back to image pixel coordinates
            x_old = int(
                round(original_point[0] + cx)
            )

            y_old = int(
                round(original_point[1] + cy)
            )


            # Check image boundaries
            if (
                0 <= x_old < width
                and
                0 <= y_old < height
            ):

                output[y_new, x_new] = \
                    image_array[y_old, x_old]


    # Convert NumPy array back to PIL Image
    return Image.fromarray(output)


# ============================================================
# MAIN INTERACTIVE TOOLBOX
# ============================================================

while True:


    # ========================================================
    # DISPLAY MENU
    # ========================================================

    print("\n" + "=" * 50)

    print("IMAGE TRANSFORMATION TOOLBOX")

    print("=" * 50)

    print("1. Rotate")

    print("2. Resize")

    print("3. Flip")

    print("4. Shear")

    print("5. Custom Matrix")

    print("6. Reset")

    print("7. Exit")


    # Get user choice
    choice = input(
        "\nEnter your choice (1-7): "
    )


    # ========================================================
    # OPTION 1: ROTATE
    # ========================================================

    if choice == "1":

        # Get angle
        angle = float(
            input(
                "Enter rotation angle in degrees: "
            )
        )


        # Rotate image
        current_image = current_image.rotate(
            angle,
            expand=True
        )


        # Display result
        display_image(
            current_image,
            f"Rotated by {angle} degrees"
        )


    # ========================================================
    # OPTION 2: RESIZE
    # ========================================================

    elif choice == "2":

        # Get resize factor
        factor = float(
            input(
                "Enter resize factor "
                "(2 = double, 0.5 = half): "
            )
        )


        # Get current size
        width, height = current_image.size


        # Calculate new size
        new_width = int(
            width * factor
        )

        new_height = int(
            height * factor
        )


        # Resize image
        current_image = current_image.resize(
            (new_width, new_height)
        )


        # Display result
        display_image(
            current_image,
            f"Resized by factor {factor}"
        )


    # ========================================================
    # OPTION 3: FLIP
    # ========================================================

    elif choice == "3":

        print("\nFlip Options:")

        print("1. Horizontal Flip")

        print("2. Vertical Flip")


        # Get flip choice
        flip_choice = input(
            "Choose flip type (1 or 2): "
        )


        # Horizontal flip
        if flip_choice == "1":

            current_image = \
                current_image.transpose(
                    Image.Transpose.FLIP_LEFT_RIGHT
                )


            display_image(
                current_image,
                "Horizontal Flip"
            )


        # Vertical flip
        elif flip_choice == "2":

            current_image = \
                current_image.transpose(
                    Image.Transpose.FLIP_TOP_BOTTOM
                )


            display_image(
                current_image,
                "Vertical Flip"
            )


        else:

            print(
                "Invalid flip option!"
            )


    # ========================================================
    # OPTION 4: SHEAR
    # ========================================================

    elif choice == "4":

        # Get shear factor
        shear_factor = float(
            input(
                "Enter horizontal shear factor: "
            )
        )


        # Horizontal shear matrix
        #
        # A = [1  k]
        #     [0  1]
        #

        A = np.array([
            [1, shear_factor],
            [0, 1]
        ])


        # Apply matrix transformation
        current_image = matrix_transform(
            current_image,
            A
        )


        # Display result
        display_image(
            current_image,
            f"Horizontal Shear (factor = {shear_factor})"
        )


    # ========================================================
    # OPTION 5: CUSTOM MATRIX
    # ========================================================

    elif choice == "5":

        print(
            "\nEnter the values of a 2x2 matrix:"
        )

        print(
            "[ a  b ]"
        )

        print(
            "[ c  d ]"
        )


        # Get matrix values
        a = float(
            input("Enter a: ")
        )

        b = float(
            input("Enter b: ")
        )

        c = float(
            input("Enter c: ")
        )

        d = float(
            input("Enter d: ")
        )


        # Create matrix
        A = np.array([
            [a, b],
            [c, d]
        ])


        # Print matrix
        print("\nCustom Matrix:")

        print(A)


        # Standard basis vectors
        e1 = np.array([1, 0])

        e2 = np.array([0, 1])


        # Apply transformation
        print(
            "\nT(e1) =",
            A @ e1
        )

        print(
            "T(e2) =",
            A @ e2
        )


        # Print rank
        print(
            "\nRank(A) =",
            np.linalg.matrix_rank(A)
        )


        # Apply custom transformation
        current_image = matrix_transform(
            current_image,
            A
        )


        # Display result
        display_image(
            current_image,
            "Custom Matrix Transformation"
        )


    # ========================================================
    # OPTION 6: RESET
    # ========================================================

    elif choice == "6":

        # Restore original image
        current_image = original_image.copy()


        print(
            "\nImage reset successfully!"
        )


        # Display original image
        display_image(
            current_image,
            "Reset: Original Image"
        )


    # ========================================================
    # OPTION 7: EXIT
    # ========================================================

    elif choice == "7":

        print(
            "\nExiting Image Transformation Toolbox..."
        )

        break


    # ========================================================
    # INVALID INPUT
    # ========================================================

    else:

        print(
            "\nInvalid choice!"
        )

        print(
            "Please enter a number from 1 to 7."
        )


# ============================================================
# END OF PROGRAM
# ============================================================