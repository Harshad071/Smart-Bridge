import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img


def draw_lane_lines(img, lines, color=(0, 0, 255), thickness=5):
    left_line_points = []
    right_line_points = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
            
            if slope < -0.5:
                left_line_points.extend([(x1, y1), (x2, y2)])
            elif slope > 0.5:
                right_line_points.extend([(x1, y1), (x2, y2)])
    
    draw_long_line(img, left_line_points, color, thickness)
    draw_long_line(img, right_line_points, color, thickness)


def draw_long_line(img, points, color, thickness):
    if len(points) > 0:
        x_coords, y_coords = zip(*points)
        poly_fit = np.polyfit(y_coords, x_coords, deg=1)
        slope, intercept = poly_fit
        
        start_y = img.shape[0]
        end_y = int(start_y * 0.6)  # Adjusted to vary the line length dynamically
        
        # Limiting the x-coordinates based on perspective
        start_x = max(0, min(int(slope * start_y + intercept), img.shape[1]))
        end_x = max(0, min(int(slope * end_y + intercept), img.shape[1]))
        
        cv2.line(img, (start_x, start_y), (end_x, end_y), color, thickness)


# Function to process each frame or image
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    height, width = edges.shape
    region_vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height)
    ]
    
    masked_edges = region_of_interest(edges, np.array([region_vertices], np.int32))
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=100)
    
    line_image = np.zeros_like(frame)
    draw_lane_lines(line_image, lines)
    
    final_output = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    return final_output
