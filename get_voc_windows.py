import os, sys
import shutil
from tqdm import tqdm
import xml.etree.ElementTree as ET


classes = ["hat", "person","helmet"]
sets = ["train", "val", "test"]

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw  # x_center
    y = y * dh  # y_center
    w = w * dw  # width
    h = h * dh  # height
    return (x, y, w, h)


def parse_xml(xml_path, dst_label_path):
    anno_xml = xml_path
    anno_txt = dst_label_path
    if os.path.exists(anno_xml):
        xml = open(anno_xml, 'r',encoding='utf-8')
        txt = open(anno_txt, 'w', encoding='utf-8')
        tree = ET.parse(xml)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            cls = obj.find('name').text
            difficult = obj.find('difficult').text
            if cls not in classes or difficult == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            bbox = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text))
            yolo_bbox = convert((w, h), bbox)
            yolo_anno = str(cls_id) + " " + " ".join([str(i) for i in yolo_bbox]) + '\n'
            txt.write(yolo_anno)
        xml.close()
        txt.close()
    else:
        print(anno_xml, "文件不存在")

def copy_to(src, dst):
    shutil.copyfile(src, dst)

for s in sets:
    name_path = "VOC2028/ImageSets/Main/{}.txt".format(s)
    f = open(name_path,"r")
    names = f.readlines()
    f.close()
    for name in tqdm(names):
        name = name.replace('\n', '').replace('\r', '')
        image_path = r"VOC2028/JPEGImages/{}.jpg".format(name)
        xml_path = r"VOC2028/Annotations/{}.xml".format(name)
        dst_image_path = r"SHWD/images/{}/{}.jpg".format(s, name)
        dst_label_path = r"SHWD/labels/{}/{}.txt".format(s, name)
        if os.path.exists(image_path) and os.path.exists(xml_path):
            parse_xml(xml_path, dst_label_path)
            if not os.path.exists(dst_image_path):
                copy_to(image_path, dst_image_path)
            else:
                print(dst_image_path, "文件已存在")
        else:
            print(image_path, xml_path)
