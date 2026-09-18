<img width="299" height="168" alt="images" src="https://github.com/user-attachments/assets/5e7c03fd-9976-4ef8-adbf-3393ac5f447d" />


EXPLAINATION
Q10 
An image is selected from the computer using a file selection window. The image is converted into a NumPy array so that it can be processed using Python. The pixel coordinates are considered relative to the centre of the image.

Five different transformation matrices are used to transform the image. For each matrix, the program calculates T(e1) and T(e2) by multiplying the matrix with the standard basis vectors. It also calculates the rank of the matrix using NumPy. The rank helps to identify whether any dimension or information is lost during the transformation.

The program finds the corners of the image and transforms them to calculate the new image size. An inverse matrix is used to find the corresponding original pixel for each output pixel. This helps to create the transformed image.

The first matrix performs scaling, which increases the width and decreases the height of the image. The second matrix rotates the image by 90 degrees. The third matrix applies horizontal shear, which changes the position of pixels in the horizontal direction. The fourth matrix reflects the image along the y-axis. The fifth matrix projects the image onto the x-axis, which causes information in the y-direction to be lost.

For the fifth matrix, a small nonzero y-scale is used only for displaying the image properly. The actual projection matrix remains unchanged.

Q11 
In this question, an interactive image transformation toolbox is developed using Python. The program allows the user to select a JPG or PNG image from the computer using a file selection window. The selected image is loaded using the Pillow library and displayed using Matplotlib.

The toolbox provides different options such as Rotate, Resize, Flip, Shear, Custom Matrix, Reset and Exit. The user can select an option from the menu and enter the required values.

The rotate option changes the angle of the image, while the resize option changes its size according to the given factor. The flip option allows the user to flip the image horizontally or vertically. The shear option uses a transformation matrix to change the horizontal position of the pixels.

The custom matrix option allows the user to enter the values of a 2×2 matrix. The program then calculates T(e1), T(e2) and the rank of the matrix before applying the transformation to the image.

The reset option restores the original image, so the user can start again without selecting the image another time. The toolbox uses NumPy for matrix calculations, Pillow for image processing, Matplotlib for displaying images and Tkinter for selecting the image file.

The main purpose of this toolbox is to understand how mathematical transformation matrices can be used in practical image processing.
