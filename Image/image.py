from PIL import ImageDraw


class ImageManipulation:
    def __init__(self):
        super(ImageManipulation, self).__init__()

    def insert_points_text(self, photo, quotation_points):
        marker = 1

        quotation_points_updated = {}

        image_with_text = ImageDraw.Draw(photo)
        for point in quotation_points:
            image_with_text.text((point[0] - 30, point[1] - 30), f"P{marker}", font_size=25, fill=(255, 0, 0))
            quotation_points_updated[f"P{marker}"] = point
            marker += 1

        return quotation_points_updated
