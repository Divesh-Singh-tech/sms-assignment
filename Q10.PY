# ============================================================
# Q10: IMAGE TRANSFORMATIONS USING LINEAR ALGEBRA
# VS CODE VERSION
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import filedialog


# ============================================================
# STEP 1: SELECT YOUR IMAGE
# ============================================================

root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[
        ("Image Files", "*.jpg *.jpeg *.png"),
        ("All Files", "*.*")
    ]
)

# Check if image was selected
if not file_path:
    print("No image selected!")
    exit()

# Load image
img = Image.open(file_path).convert("RGB")

# Convert image to NumPy array
image = np.array(img)

print("Image loaded successfully!")
print("Image shape:", image.shape)


# ============================================================
# DISPLAY ORIGINAL IMAGE
# ============================================================

plt.figure(figsize=(6, 6))
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")
plt.show()


# ============================================================
# STEP 2: DEFINE MATRICES
# ============================================================

# A1 = Scaling
A1 = np.array([
    [2, 0],
    [0, 0.5]
])

# A2 = 90 Degree Rotation
A2 = np.array([
    [0, -1],
    [1, 0]
])

# A3 = Horizontal Shear
A3 = np.array([
    [1, 1],
    [0, 1]
])

# A4 = Reflection in Y-axis
A4 = np.array([
    [-1, 0],
    [0, 1]
])

# A5 = Projection onto X-axis
A5 = np.array([
    [1, 0],
    [0, 0]
])


# Store all transformations
transformations = {
    "A1 - Scaling": A1,
    "A2 - 90 Degree Rotation": A2,
    "A3 - Horizontal Shear": A3,
    "A4 - Reflection in Y-axis": A4,
    "A5 - Projection onto X-axis": A5
}


# ============================================================
# STEP 3: ANALYZE MATRIX
# Prints T(e1), T(e2), Rank and Information Loss
# ============================================================

def analyze_matrix(A, name):

    # Standard basis vectors
    e1 = np.array([1, 0])
    e2 = np.array([0, 1])

    # Apply transformation
    Te1 = A @ e1
    Te2 = A @ e2

    # Find rank
    rank = np.linalg.matrix_rank(A)

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("\nMatrix:")
    print(A)

    print("\nT(e1) =", Te1)
    print("T(e2) =", Te2)

    print("\nRank =", rank)

    if rank < 2:
        print("Information Lost: YES")
        print("Dimension Lost: YES")
    else:
        print("Information Lost: NO")
        print("Dimension Lost: NO")


# ============================================================
# STEP 4: FUNCTION TO TRANSFORM IMAGE
#
# Coordinates are measured relative to image centre
# ============================================================

def transform_image(image, A):

    height, width = image.shape[:2]

    # Image centre
    cx = width / 2
    cy = height / 2


    # Four corners relative to image centre
    corners = np.array([
        [-cx, -cy],
        [ cx, -cy],
        [-cx,  cy],
        [ cx,  cy]
    ])


    # Transform all corners
    transformed_corners = (A @ corners.T).T


    # Find new boundaries
    min_x = transformed_corners[:, 0].min()
    max_x = transformed_corners[:, 0].max()

    min_y = transformed_corners[:, 1].min()
    max_y = transformed_corners[:, 1].max()


    # Calculate new image size
    new_width = int(np.ceil(max_x - min_x)) + 1
    new_height = int(np.ceil(max_y - min_y)) + 1


    # Prevent zero size
    new_width = max(new_width, 1)
    new_height = max(new_height, 1)


    # Create blank output image
    output = np.zeros(
        (new_height, new_width, 3),
        dtype=np.uint8
    )


    # --------------------------------------------------------
    # Find inverse matrix
    # --------------------------------------------------------

    # If matrix is invertible
    if abs(np.linalg.det(A)) > 1e-10:
        A_inv = np.linalg.inv(A)

    # If matrix is singular, use pseudo-inverse
    else:
        A_inv = np.linalg.pinv(A)


    # ========================================================
    # MAP OUTPUT PIXELS BACK TO ORIGINAL IMAGE
    # ========================================================

    for y_new in range(new_height):

        for x_new in range(new_width):

            # Point in transformed coordinate system
            transformed_point = np.array([
                x_new + min_x,
                y_new + min_y
            ])


            # Find corresponding original point
            original_point = A_inv @ transformed_point


            # Convert to original image coordinates
            x_old = int(round(original_point[0] + cx))
            y_old = int(round(original_point[1] + cy))


            # Copy pixel if it is inside image
            if (
                0 <= x_old < width
                and
                0 <= y_old < height
            ):

                output[y_new, x_new] = image[y_old, x_old]


    return output


# ============================================================
# STEP 5: APPLY ALL FIVE MATRICES
# ============================================================

for name, A in transformations.items():

    # Print mathematical analysis
    analyze_matrix(A, name)


    # ========================================================
    # SPECIAL CASE: A5
    # ========================================================

    if name == "A5 - Projection onto X-axis":

        print("\nTRUE MATRIX A5:")
        print(A5)

        print("\nTrue transformation:")
        print("All points are projected onto the x-axis.")

        print("\nFor visualization only:")
        print("A small y-scale of 0.05 is used.")

        # Visualization matrix only
        A_visual = np.array([
            [1, 0],
            [0, 0.05]
        ])

        transformed = transform_image(
            image,
            A_visual
        )

    else:

        # Apply normal transformation
        transformed = transform_image(
            image,
            A
        )


    # ========================================================
    # DISPLAY TRANSFORMED IMAGE
    # ========================================================

    plt.figure(figsize=(8, 6))

    plt.imshow(transformed)

    plt.title(name)

    plt.axis("off")

    plt.show()


print("\nAll transformations completed successfully!")