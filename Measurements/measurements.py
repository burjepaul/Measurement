import math

from PIL import ImageDraw

from constants import RED_SENSIBILITY_INDEX, DISTANCE_BETWEEN_POINTS_IN_MM


def calculate_measurements_points_coordinates(width, height, pixel_map):
    def dfs(x, y):
        if x < 0 or x >= width or y < 0 or y >= height or pixel_map[x, y] != (0, 255, 0):
            return
        pixel_map[x, y] = (0, 0, 255)  # Mark the visited pixel as blue

        # Explore neighboring pixels
        dfs(x - 1, y)  # Left
        dfs(x + 1, y)  # Right
        dfs(x, y - 1)  # Up
        dfs(x, y + 1)  # Down

    measurement_points = []
    for x in range(width):
        for y in range(height):
            if pixel_map[x, y] == (0, 255, 0):  # If the pixel is green
                dfs(x, y)  # Explore the entire green area
                measurement_points.append([x, y])

    return measurement_points


def increase_detected_points(pixel_map, row, column, increse_pixel):
    for i in range(increse_pixel * 2):
        for j in range(increse_pixel * 2):
            pixel_map[row - increse_pixel + i, column - increse_pixel + j] = (0, 255, 0)


def draw_lines_between_points(image, point1, point2):
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Convert the points to tuples of integers
    point1 = (int(point1[0]), int(point1[1]))
    point2 = (int(point2[0]), int(point2[1]))

    # Draw a blue line between the two points
    line_color = (0, 0, 255)  # Blue color in RGB format
    line_width = 1
    draw.line([point1, point2], fill=line_color, width=line_width)


def find_coordinates_of_blue_neighbours(image, point):
    coordinates = []
    if image.getpixel((point[0], point[1] - 1)) == (0, 0, 255):
        coordinates.append((point[0], point[1] - 1))
    if image.getpixel((point[0] + 1, point[1] - 1)) == (0, 0, 255):
        coordinates.append((point[0] + 1, point[1] - 1))
    if image.getpixel((point[0] - 1, point[1] - 1)) == (0, 0, 255):
        coordinates.append((point[0] - 1, point[1] - 1))
    if image.getpixel((point[0] - 1, point[1])) == (0, 0, 255):
        coordinates.append((point[0] - 1, point[1]))
    if image.getpixel((point[0] - 1, point[1] + 1)) == (0, 0, 255):
        coordinates.append((point[0] - 1, point[1] + 1))
    if image.getpixel((point[0], point[1] + 1)) == (0, 0, 255):
        coordinates.append((point[0], point[1] + 1))
    if image.getpixel((point[0] + 1, point[1] + 1)) == (0, 0, 255):
        coordinates.append((point[0] + 1, point[1] + 1))
    if image.getpixel((point[0] + 1, point[1])) == (0, 0, 255):
        coordinates.append((point[0] + 1, point[1]))
    if image.getpixel((point[0] + 1, point[1] - 1)) == (0, 0, 255):
        coordinates.append((point[0] + 1, point[1] - 1))
    return coordinates


def get_distance_to_intersection_points(image, point):
    starting_coordinates = find_coordinates_of_blue_neighbours(image, point)
    index1 = 0
    index2 = 0
    point_index1 = starting_coordinates[0]
    point_index2 = starting_coordinates[1]

    output_object = {

    }

    while len(find_coordinates_of_blue_neighbours(image, point_index1)) < 3:
        point_index1 = find_coordinates_of_blue_neighbours(image, point_index1)[0]
        index1 += 1

    while len(find_coordinates_of_blue_neighbours(image, point_index2)) < 3:
        point_index2 = find_coordinates_of_blue_neighbours(image, point_index2)[1]
        index2 += 1

    distance_to_first_intersection_point = (index1 * DISTANCE_BETWEEN_POINTS_IN_MM) / (index1 + index2)
    distance_to_second_intersection_point = (index2 * DISTANCE_BETWEEN_POINTS_IN_MM) / (index1 + index2)

    output_object = {
        point_index1: distance_to_first_intersection_point,
        point_index2: distance_to_second_intersection_point
    }
    return output_object


def find_if_two_points_are_neighbours(point1, point2):
    for point_one in point1:
        for point_two in point2:
            if abs(point_one[0] - point_two[0]) <= 1 and abs(point_one[0] - point_two[0]) <= 1:
                return point_one, point_two
    return False


class Measurements:
    def __init__(self):
        super(Measurements, self).__init__()

    def detect_measurement_points(self, width, height, photo):
        pixel_map = photo.load()
        image_with_text = ImageDraw.Draw(photo)

        for i in range(width):
            for j in range(height):
                r, g, b = photo.getpixel((i, j))
                if r > (255 * RED_SENSIBILITY_INDEX/100) and g < (255 * (100-RED_SENSIBILITY_INDEX)/200) and b < (255 * (100-RED_SENSIBILITY_INDEX)/200):
                    try:
                        increase_detected_points(pixel_map, i, j, 2)
                    except:
                        pass
        measurement_points = calculate_measurements_points_coordinates(width, height, pixel_map)

        for pixel in measurement_points:
            image_with_text.text((pixel[0], pixel[1]),
                                 "{programming}, {python}".format(programming=pixel[0], python=pixel[1]), font_size=25,
                                 fill=(255, 0, 0))

        return [photo, measurement_points]

    def detect_measurement_lines(self, measurement_points):
        def sort_measurement_points(points):
            def key_function(subarray):
                return sum(subarray)

            # Use the sorted function to sort the array based on the custom key function
            sorted_arr = sorted(points, key=key_function)

            return sorted_arr

        measurement_points = sort_measurement_points(measurement_points)

        lines = {
            "left_line": [measurement_points[0]],
            "right_line": [measurement_points[-1]],
            "up_line": [measurement_points[0]],
            "down_line": [measurement_points[-1]],
        }

        # remove first and last element of the array which now are in the lines dictionary
        measurement_points = [x for x in measurement_points[1:-1]]

        for point in measurement_points:
            if lines['left_line'][0][0] - 100 < point[0] < lines['left_line'][0][0] + 110:
                lines['left_line'].append(point)
            if lines['up_line'][0][1] - 100 < point[1] < lines['up_line'][0][1] + 110:
                lines['up_line'].append(point)
            if lines['right_line'][0][0] - 66 < point[0] < lines['right_line'][0][0] + 280:
                lines['right_line'].append(point)
            if lines['down_line'][0][1] - 100 < point[1] < lines['down_line'][0][1] + 110:
                lines['down_line'].append(point)

            lines["left_line"] = sorted(lines["left_line"], key=lambda x: x[1])
            lines["right_line"] = sorted(lines["right_line"], key=lambda x: x[1])
            lines["up_line"] = sorted(lines["up_line"], key=lambda x: x[0])
            lines["down_line"] = sorted(lines["down_line"], key=lambda x: x[0])

        return lines

    def draw_lines_between_all_image_points(self, lines, image):
        draw = ImageDraw.Draw(image)
        index = 1
        for left_point in lines["left_line"][1:]:
            left_point = (int(left_point[0]), int(left_point[1]))
            right_point = (int(lines["right_line"][index][0]), int(lines["right_line"][index][1]))
            draw.line([left_point, right_point], fill=(0, 0, 255), width=1)
            index += 1

        index = 1
        for up_point in lines["up_line"][1:]:
            up_point = (int(up_point[0]), int(up_point[1]))
            down_point = (int(lines["down_line"][index][0]), int(lines["down_line"][index][1]))
            draw.line([up_point, down_point], fill=(0, 0, 255), width=1)
            index += 1

    def detect_quotation_points(self, lines, measurement_points):
        quotation_points = []
        points = []

        for line in lines:
            for point in lines[line]:
                if point in measurement_points:
                    points.append(point)

        for point in measurement_points:
            if point not in points:
                quotation_points.append(point)

        return quotation_points

    def detect_intersection_of_line_with_measurements_lines(self, image, line_coordinates):
        intersection_coordinates = [[1, 1]]
        draw = ImageDraw.Draw(image)
        #draw.line([(490, 1403), (3373, 1215)], fill=(0, 255, 0), width=1)
        for point in line_coordinates:
            r, g, b = image.getpixel((point[0], point[1]))
            if r == 0 and g == 0 and b == 255:
                if intersection_coordinates[-1][0] + 1 == point[0] or intersection_coordinates[-1][1] + 1 == point[1]:
                    intersection_coordinates = intersection_coordinates[:-1] + [[point[0], point[1]]]
                else:
                    intersection_coordinates = intersection_coordinates + [[point[0], point[1]]]
        return intersection_coordinates[1:]

    def get_line_coordinates(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        # Calculate the differences in x and y
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # Determine the sign for x and y
        sx = 1 if x2 >= x1 else -1
        sy = 1 if y2 >= y1 else -1

        # Initialize the error term
        error = dx - dy

        # Initialize the current coordinates
        x, y = x1, y1

        # Create a list to store the line coordinates
        coordinates = []

        while True:
            # Append the current coordinates to the list
            coordinates.append((x, y))

            # If we have reached the endpoint, break the loop
            if x == x2 and y == y2:
                break

            # Calculate the next coordinates
            e2 = 2 * error
            if e2 > -dy:
                error -= dy
                x += sx
            if e2 < dx:
                error += dx
                y += sy

        return coordinates
    def calculate_distance_between_first_and_last_points(self, image, point_one, point_two):
        print(point_one, point_two)

    def calculate_distance_between_two_points(self, image, point_one, point_two):
        result = 1
        data1 = get_distance_to_intersection_points(image, point_one)
        data2 = get_distance_to_intersection_points(image, point_two)
        data = {**data1, **data2}
        print(data)
        points1 = list(data1.keys())
        points2 = list(data2.keys())
        common_points = find_if_two_points_are_neighbours(points1, points2)
        if common_points:
            for point in common_points:
                result = result + (data[point] * data[point])
        else:
            closest_point1 = min(abs(points1[0][1] - point_one[1]), abs(points1[1][1] - point_one[1]))
            closest_point2 = min(abs(points1[0][1] - point_two[1]), abs(points1[1][1] - point_two[1]))
            height = abs(closest_point1 - closest_point2)
            if closest_point1 <= closest_point2:
                segment_height = abs(points2[0][1] - points2[1][1])
            else:
                segment_height = abs(points1[0][1] - points1[1][1])

            height_mm = (10 * height)/segment_height

            result = 10*10 + height_mm * height_mm
        return math.sqrt(result)
