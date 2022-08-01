import numpy as np
import logging
import pathlib
import xml.etree.ElementTree as ET
import cv2
import os


class VOCDataset:

    def __init__(self, root, transform=None, target_transform=None, is_test=False, keep_difficult=False, label_file=None):
        """Dataset for VOC data.
        Args:
            root: the root of the VOC2007 or VOC2012 dataset, the directory contains the following sub-directories:
                Annotations, ImageSets, JPEGImages, SegmentationClass, SegmentationObject.
        """
        self.root = pathlib.Path(root)
        self.transform = transform
        self.target_transform = target_transform
        if is_test:
            image_sets_file = self.root / "ImageSets/Main/test.txt"
        else:
            image_sets_file = self.root / "ImageSets/Main/trainval.txt"
        self.ids = VOCDataset._read_image_ids(image_sets_file)
        self.keep_difficult = keep_difficult

        # if the labels file exists, read in the class names
        label_file_name = self.root / "labels.txt"

        if os.path.isfile(label_file_name):
            class_string = ""
            with open(label_file_name, 'r') as infile:
                for line in infile:
                    class_string += line.rstrip()

            # classes should be a comma separated list
            
            classes = class_string.split(',')
            # prepend BACKGROUND as first class
            classes.insert(0, 'BACKGROUND')
            classes  = [ elem.replace(" ", "") for elem in classes]
            self.class_names = tuple(classes)
            logging.info("VOC Labels read from file: " + str(self.class_names))

        else:
            logging.info("No labels file, using default VOC classes.")
            self.class_names = ('BACKGROUND','vertebral')


        self.class_dict = {class_name: i for i, class_name in enumerate(self.class_names)}

    def __getitem__(self, index):
        #print("[Debug] getitem function:... ")      ### Modification ###
        image_id = self.ids[index]
        boxes, labels, is_difficult = self._get_annotation(image_id)
        if not self.keep_difficult:
            boxes = boxes[is_difficult == 0]
            labels = labels[is_difficult == 0]
        image = self._read_image(image_id)
        #print("voc", boxes)
        #print("voc", boxes.shape)
        if self.transform:
            #print('[boxes shape]: ', boxes)         ### Modification ###
            
#             print("voc2.0", boxes)
#             print("voc2.0", boxes.shape)
            image, boxes, labels = self.transform(image, boxes, labels)
#             print("voc2", boxes)
#             print("voc2", boxes.shape)
        if self.target_transform:
            boxes, labels = self.target_transform(boxes, labels)
            
#             print("voc3", boxes)
#             print("voc3", boxes.shape)
        return image, boxes, labels

    def get_image(self, index):
        image_id = self.ids[index]
        image = self._read_image(image_id)
        if self.transform:
            image, _ = self.transform(image)
        return image

    def get_annotation(self, index):
        image_id = self.ids[index]
        return image_id, self._get_annotation(image_id)

    def __len__(self):
        return len(self.ids)

    @staticmethod
    def _read_image_ids(image_sets_file):
        ids = []
        with open(image_sets_file) as f:
            for line in f:
                ids.append(line.rstrip())
        return ids

    def _get_annotation(self, image_id):
        annotation_file = self.root / f"Annotations/{image_id}.xml"
        #print(self.ids)
        #print(">>> annotation:  ", annotation_file)
        objects = ET.parse(annotation_file).findall("object")
        boxes = []
        labels = []
        is_difficult = []
        for object in objects:
            #print(object)
            class_name = object.find('name').text.lower().strip()
            class_name = 'vertebral'
            #print(class_name)
            # we're only concerned with clases in our list
            if class_name in self.class_dict:
                # ----> Begin original code for Bounding Box ...
                ''' 
                bbox = object.find('bndbox')
                #print(bbox)
                # VOC dataset format follows Matlab, in which indexes start from 0
                x1 = float(bbox.find('xmin').text) - 1
                y1 = float(bbox.find('ymin').text) - 1
                x2 = float(bbox.find('xmax').text) - 1
                y2 = float(bbox.find('ymax').text) - 1
                              
                boxes.append([x1, y1, x2, y2])
                #print(boxes)
                ''' 
                #print(object.find('difficult'))
                # <--- End original code for Bounding Box ...
                
                # ----> Begin modification for Rotated Bounding Box ... 
                robbox = object.find('robndbox')
                #print(robbox)
                # VOC dataset format follows Matlab, in which indexes start from 0
                cx = float(robbox.find('cx').text)# - 1
                cy = float(robbox.find('cy').text)# - 1
                w = float(robbox.find('w').text)# - 1
                h = float(robbox.find('h').text)# - 1
                angle = float(robbox.find('angle').text)# - 1
                              
                boxes.append([cx, cy, w, h, angle])
                # <--- End modification for Rotated Bounding Box ...
                
                labels.append(self.class_dict[class_name])
                is_difficult_str = object.find('difficult').text
                is_difficult.append(int(is_difficult_str) if is_difficult_str else 0)

        return (np.array(boxes, dtype=np.float32),
                np.array(labels, dtype=np.int64),
                np.array(is_difficult, dtype=np.uint8))

    def _read_image(self, image_id):
        image_file = self.root / f"JPEGImages/{image_id}.jpg"
        #print("[image file]: ", image_file)
        image = cv2.imread(str(image_file))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image



