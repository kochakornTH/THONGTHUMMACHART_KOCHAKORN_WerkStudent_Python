import cv2
import numpy as np

# Detection
def detect_rectangle(image_path, color):
    """
    Detects the boundaries of a rectangle of a given color in an image.

    Args:
        image_path: Path to the image file.
        color: Color to detect ('red', 'blue', 'green', 'yellow', 'purple')

    Returns:
        A tuple containing the coordinates of the top-left corner (x1, y1) 
        and the bottom-right corner (x2, y2) of the rectangle, 
        or None if no rectangle of the specified color is found.
    """

    # Load the image
    img = cv2.imread(image_path)

    # Check if image was loaded successfully
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return None

    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color bounds in HSV
    if color == 'red':
        lower = np.array([0, 50, 50])
        upper = np.array([10, 255, 255])
        lower2 = np.array([170, 50, 50])
        upper2 = np.array([180, 255, 255])
    elif color == 'blue':
        lower = np.array([90, 50, 50])
        upper = np.array([130, 255, 255])
    elif color == 'orange':
        lower = np.array([10, 50, 50])  
        upper = np.array([25, 255, 255])
    elif color == 'cyan':
        lower = np.array([80, 50, 50])
        upper = np.array([100, 255, 255])
    elif color == 'green':
        lower = np.array([40, 50, 50])
        upper = np.array([80, 255, 255])
    elif color == 'purple':
        lower = np.array([130, 50, 50])
        upper = np.array([160, 255, 255])
    elif color == 'yellow':
        lower = np.array([20, 50, 50])
        upper = np.array([40, 255, 255])
    elif color == 'brown':
        lower = np.array([10, 50, 50]) 
        upper = np.array([30, 255, 150]) 
    else:
        print(f"Invalid color: {color}. Supported colors: 'red', 'blue', 'green', 'yellow', 'purple','orange','cyan','pink'")
        return None

    # Create a mask for the specified color
    if color == 'red':
        mask1 = cv2.inRange(hsv, lower, upper)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, lower, upper)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the most area (assuming it's the rectangle)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Find the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Calculate coordinates of top-left and bottom-right corners
        x1, y1 = x, y
        x2, y2 = x + w, y + h

        # Get image dimensions
        height, width, _ = img.shape

        return (x1, y1), (x2, y2), (0, 0), (width, height) 

    else:
        return None