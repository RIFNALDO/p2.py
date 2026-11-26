
import cv2
import numpy as np


def apply_filter(image, filter_type):
    """Apply the selected color filter or edge detection mode to a copy of the image."""
    filtered_image = image.copy()

    # OpenCV uses BGR channel order: index 0 = Blue, index 1 = Green, index 2 = Red
    if filter_type == "red_tint":
        filtered_image[:, :, 0] = 0  # Zero out Blue channel
        filtered_image[:, :, 1] = 0  # Zero out Green channel

    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0  # Zero out Blue channel
        filtered_image[:, :, 2] = 0  # Zero out Red channel

    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  # Zero out Green channel
        filtered_image[:, :, 2] = 0  # Zero out Red channel

    elif filter_type == "sobel":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Compute horizontal and vertical gradients
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

        # Take absolute values and convert to 8-bit unsigned integers before combining
        abs_x = np.uint8(np.absolute(sobel_x))
        abs_y = np.uint8(np.absolute(sobel_y))
        combined_sobel = cv2.bitwise_or(abs_x, abs_y)

        # Convert back to 3-channel BGR so imshow displays consistently
        filtered_image = cv2.cvtColor(combined_sobel, cv2.COLOR_GRAY2BGR)

    elif filter_type == "canny":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)
        filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return filtered_image


def main():
    image_path = "example.jpg"  # Replace with your sample image path
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load image from '{image_path}'. Check the file path and try again.")
        return

    filter_type = "original"
    print("Controls:")
    print("  'r' - Red Tint")
    print("  'g' - Green Tint")
    print("  'b' - Blue Tint")
    print("  's' - Sobel Edge Detection")
    print("  'c' - Canny Edge Detection")
    print("  'o' - Original Image")
    print("  'q' - Quit")

    window_name = "Real-Time Image Processing"

    while True:
        processed_image = apply_filter(image, filter_type)
        cv2.imshow(window_name, processed_image)

        key = cv2.waitKey(0) & 0xFF

        if key == ord("r"):
            filter_type = "red_tint"
            print("Active mode: Red Tint")
        elif key == ord("g"):
            filter_type = "green_tint"
            print("Active mode: Green Tint")
        elif key == ord("b"):
            filter_type = "blue_tint"
            print("Active mode: Blue Tint")
        elif key == ord("s"):
            filter_type = "sobel"
            print("Active mode: Sobel Edge Detection")
        elif key == ord("c"):
            filter_type = "canny"
            print("Active mode: Canny Edge Detection")
        elif key == ord("o"):
            filter_type = "original"
            print("Active mode: Original Image")
        elif key == ord("q"):
            print("Exiting program...")
            break
        else:
            print("Invalid key! Please press 'r', 'g', 'b', 's', 'c', 'o', or 'q'.")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()