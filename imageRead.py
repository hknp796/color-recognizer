import cv2
import numpy as np
import math

# Load the input image
image = cv2.imread('path/small.png')



# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect circles using HoughCircles method
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20, 
                            param1=50, param2=30, minRadius=10, maxRadius=40)
one_color_circles = []

if circles is not None:
    for circle in circles[0]:
        x, y, r = circle
        cropped_img = blur[int(y-r):int(y+r), int(x-r):int(x+r)]
        std = np.std(cropped_img)
        if std < 20:
            one_color_circles.append(circle)


# If no circles are detected, exit the program
if circles is None:
    print("No circles detected")
    exit()

# Convert the (x, y) coordinates and radius of the circles to integers
circles = np.round(circles[0, :]).astype("int")

# Create a list to store the color and position of each circle
circle_info = []

# Loop through each detected circle
for (x, y, r) in circles:
    # Extract the region of interest (ROI) within the circle
    roi = image[y - r:y + r, x - r:x + r]

    # Calculate the mean color of the ROI
    mean_color = cv2.mean(roi)

    # Identify the color of the circle based on the mean color
    if mean_color[0] > mean_color[1] and mean_color[0] > mean_color[2]:
        color = "p"
    elif mean_color[1] > mean_color[0] and mean_color[1] > mean_color[2]:
        color = "t"
    else:
        color = "b"

    # Add the color and position of the circle to the circle_info list
    if color == "p": # blue circles
        circle_info.append((color, x, y))

        # Draw the circle and color label on the output image
        cv2.circle(image, (x, y), r, (0, 0, 0), 2)
        cv2.putText(image, color, (x - 20, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0,0), 2)
    elif color == "b": #Red   circles
        circle_info.append((color, x, y))

        # Draw the circle and color label on the output image
        cv2.circle(image, (x, y), r, (0, 0, 0), 2)
        cv2.putText(image, color, (x - 20, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0,0), 2)
    elif color == "t": #green  circles
        circle_info.append((color, x, y))

        # Draw the circle and color label on the output image
        cv2.circle(image, (x, y), r, (0, 0, 0), 2)
        cv2.putText(image, color, (x - 20, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
        
# Sort the detected circles by their position (from left to right)
circle_info = sorted(circle_info, key=lambda x: (x[1],x[2]))        

num_circles_per_group = 6
num_groups = len(circle_info) // num_circles_per_group

for i in range(num_groups):
    start_index = i * num_circles_per_group
    end_index = start_index + num_circles_per_group
    group_circles = circle_info[start_index:end_index]

    # Calculate the average value of x for the group of circles
    group_x_sum = sum(circle[1] for circle in group_circles)
    group_x_avg = math.trunc(group_x_sum / num_circles_per_group)

    # Assign the average value of x to x for each circle in the group
    for j, (color, x, y) in enumerate(group_circles):
        circle_info[start_index + j] = (color, group_x_avg, y)

circle_info = sorted(circle_info, key=lambda x: (x[1],x[2]))        

# Print the color and position of each circle
for i, (color, x, y) in enumerate(circle_info):
    print("Circle {}: color={}, position=({}, {})".format(i+1, color, x, y))

# for i, (color, x, y) in enumerate(circle_info):
#     color_str = str(color)
#     print("{},index:{}".format(color_str,i+1))


# Show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)