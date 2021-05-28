import colorsys
import random
import cv2


def drawBoxes(image_path, label_path):
    """
    This function draw the bounding boxes for any image using the YOLOv4 format, it is used mostly for
    testing that the labels are well generated

    Args:
        image_path (string): Direction of the image
        label_path (string): Direction of the label in YOLOv4 format

    Return:
        Nothing
    """
    image = cv2.imread(image_path)
    bboxes = list()

    with open(label_path) as label:
        for line in label:
            bboxes.append([float(num) for num in line.split()])
    classes = ['Casco', 'F1', 'F2', 'F5', 'Motor', 'Pechera', 'Mano']

    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    num_boxes = len(bboxes)
    out_classes = list()
    out_boxes = list()

    for line in bboxes:
        out_classes.append(line[0])
        out_boxes.append(line[1:])

    for i in range(num_boxes):
        if int(out_classes[i]) < 0 or int(out_classes[i]) > num_classes:
            continue

        xcenter, ycenter, width, height = out_boxes[i]

        xmin = xcenter - width / 2
        xmax = xcenter + width / 2
        ymin = ycenter - height / 2
        ymax = ycenter + height / 2

        xmin = int(xmin * image_w)
        xmax = int(xmax * image_w)
        ymin = int(ymin * image_h)
        ymax = int(ymax * image_h)

        width = xmax - xmin
        height = ymax - ymin
        font_scale = 0.5
        class_ind = int(out_classes[i])
        class_name = classes[class_ind]
        bbox_color = colors[class_ind]
        bbox_thick = int(2 * (image_h + image_w) / 600)
        c1, c2 = (xmin, ymin), (xmin + width, ymin + height)
        image = cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)
        bbox_mess = class_name
        t_size = cv2.getTextSize(bbox_mess, 0, font_scale, thickness=bbox_thick // 4)[0]
        c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
        cv2.rectangle(image, c1, (int(c3[0]), int(c3[1])), bbox_color, -1)  # filled
        cv2.putText(image, bbox_mess, (c1[0], int(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

    cv2.imshow('BoundingBox', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


base_address = "D:\\Documents\\PycharmProjects\\darknet\\data"
imagePath = base_address + "\\Finals\\Validation\\Mano\\render119.jpg"
labelPath = base_address + "\\Finals\\Validation\\Mano\\render119.txt"
drawBoxes(imagePath, labelPath)

