from PIL import Image

from Measurements.measurements import Measurements
from Image.image import ImageManipulation

im = Image.open('src/test1.jpg')

# im = im.crop((400, 405, 800, 800))

im = im.convert("RGB")

pixel_map = im.load()
width, height = im.size


measurements = Measurements()
image_manipulation = ImageManipulation()

im, measurement_points = measurements.detect_measurement_points(width, height, im)
lines = measurements.detect_measurement_lines(measurement_points)
quotation_points = measurements.detect_quotation_points(lines, measurement_points)
measurements.draw_lines_between_all_image_points(lines, im)

quotation_points = image_manipulation.insert_points_text(im, quotation_points)

# print(quotation_points)
line_coordinates = measurements.get_line_coordinates(quotation_points['P1'], quotation_points['P2'])
intersection_coordinates = measurements.detect_intersection_of_line_with_measurements_lines(im, line_coordinates)
# print(line_coordinates)
print(intersection_coordinates)
total_distance = 0

measurements.calculate_distance_between_first_and_last_points(im, intersection_coordinates[0], intersection_coordinates[1])

# for i in range(len(intersection_coordinates) - 3):
#     total_distance += measurements.calculate_distance_between_two_points(im, intersection_coordinates[i+1], intersection_coordinates[i+2])

print(total_distance)
# im.show()
# first_point = input('Enter first point: ')
# second_point = input('Enter second point: ')
#
# print(first_point, quotation_points[first_point])
# measurements.calculate_distance_between_two_points(quotation_points[first_point], quotation_points[second_point])
#

im.show()
