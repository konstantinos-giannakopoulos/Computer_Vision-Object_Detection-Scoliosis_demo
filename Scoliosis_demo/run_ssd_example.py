#from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
#from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
#from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
#from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
#from vision.ssd.mobilenetv3_ssd_lite import create_mobilenetv3_large_ssd_lite, create_mobilenetv3_small_ssd_lite
from vision.ssd.resnet50_ssd import create_resnet50_ssd, create_resnet50_ssd_predictor
#from vision.ssd.resnet50_ssd600 import create_resnet50_ssd600, create_resnet50_ssd600_predictor
#from vision.utils.misc import Timer
from vision.utils import box_utils_v2
import cv2
import sys
import os
import pandas as pd

#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)

#def resource_path(relative_path):
#    if getattr(sys, 'frozen', False):
#        # If the application is run as a bundle, the PyInstaller bootloader
#        # extends the sys module by a flag frozen=True and sets the app 
#        # path into variable _MEIPASS'.
#        application_path = sys._MEIPASS
#        return os.path.join(sys._MEIPASS, relative_path)
#    else:
#        application_path = os.path.dirname(os.path.abspath(__file__))
#        return os.path.join(os.path.abspath("."), relative_path)


def resource_path(relative_path):
    application_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(application_path, relative_path)


def main(image_filename,model_option):
    #if len(sys.argv) < 5:
    #    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> <image path>')
    #    sys.exit(0)
    net_type = model_option #'resnet50-ssd' #sys.argv[1]
    model_path = 'utils/frontal/resnet50-ssd-Epoch-40-Loss-1.4795738458633423.pth' #sys.argv[2]
    label_path = 'utils/frontal/voc-model-labels.txt' #sys.argv[3]
    image_path = image_filename #'01-July-2019-91.jpg' #sys.argv[4]
    model_path = resource_path(model_path)
    label_path = resource_path(label_path)
    image_path = resource_path(image_path)
    print("net type: ", net_type)
    print("label: ", label_path)
    print("image: ", image_path)
    print("model: ", model_path)
    class_names = [name.strip() for name in open(label_path).readlines()]
    print("class names: ", class_names)

    if net_type == 'model-1':
        net_type = 'resnet50-ssd'
    elif net_type == 'model-2':
        net_type = 'mb1-ssd'
    #if net_type == 'vgg16-ssd':
    #    net = create_vgg_ssd(len(class_names), is_test=True)
    if net_type == 'mb1-ssd':
         net = create_mobilenetv1_ssd(len(class_names), is_test=True)
         model_path = 'utils/frontal/mb1-ssd-Epoch-35-Loss-1.4262940883636475.pth'
         model_path = resource_path(model_path)
    #elif net_type == 'mb1-ssd-lite':
    #    net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
    #elif net_type == 'mb2-ssd-lite':
    #    net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True)
    #elif net_type == 'mb3-large-ssd-lite':
    #    net = create_mobilenetv3_large_ssd_lite(len(class_names), is_test=True)
    #elif net_type == 'mb3-small-ssd-lite':
    #    net = create_mobilenetv3_small_ssd_lite(len(class_names), is_test=True)
    #elif net_type == 'sq-ssd-lite':
    #    net = create_squeezenet_ssd_lite(len(class_names), is_test=True)
    elif net_type == 'resnet50-ssd':
        net = create_resnet50_ssd(len(class_names), is_test=True)
        model_path = 'utils/frontal/resnet50-ssd-Epoch-40-Loss-1.4795738458633423.pth'
        model_path = resource_path(model_path)
    #elif net_type == 'resnet50-ssd600':
    #    net = create_resnet50_ssd600(len(class_names), is_test=True)
    #else:
    #    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    #    sys.exit(1)
    net.load(model_path)
    
    #if net_type == 'vgg16-ssd':
    #    predictor = create_vgg_ssd_predictor(net, candidate_size=200)
    if net_type == 'mb1-ssd':
         predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
    #elif net_type == 'mb1-ssd-lite':
    #    predictor = create_mobilenetv1_ssd_lite_predictor(net, candidate_size=200)
    #elif net_type == 'mb2-ssd-lite' or net_type == "mb3-large-ssd-lite" or net_type == "mb3-small-ssd-lite":
    #    predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
    #elif net_type == 'sq-ssd-lite':
    #    predictor = create_squeezenet_ssd_lite_predictor(net, candidate_size=200)
    elif net_type == 'resnet50-ssd':
        predictor = create_resnet50_ssd_predictor(net, candidate_size=200)
    #elif net_type == 'resnet50-ssd600':
    #    predictor = create_resnet50_ssd600_predictor(net, candidate_size=200)
    #else:
    #    predictor = create_vgg_ssd_predictor(net, candidate_size=200)
    
    
    orig_image = cv2.imread(image_path)     
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    boxes, labels, probs = predictor.predict(image, 24, 0.3, 0.35)
    # boxes, labels, probs = predictor.predict(image, 24, 0.001, 0.35)
    #print("run", boxes.shape)
    rotated_boxes = box_utils_v2.box2corners_th(boxes)   ### Modification ###
    for i in range(boxes.size(0)):
        box = boxes[i, :]
        rbox = rotated_boxes[i, :]
    #     cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)
        cv2.polylines(orig_image, [rbox.int().numpy()], True, (255, 255, 0), 4)
        #label = f"""{voc_dataset.class_names[labels[i]]}: {probs[i]:.2f}"""
        label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
        cv2.putText(orig_image, label,
                    (int(box[0] + 20), int(box[1] + 40)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,  # font scale
                    (255, 0, 255),
                    4,  # line type
                    cv2.LINE_AA)
    path = 'frontal/output_image.jpg'
    path = resource_path(path)
    cv2.imwrite(path, orig_image)
    boxes = boxes.numpy()
    boxes = pd.DataFrame(boxes, columns=['x_center', 'y_center', 'width', 'height', 'angle'])
    boxes.to_csv(resource_path(r'frontal/output_boxes.csv'), index=False)
    print(f"Found {len(probs)} objects. The output image is {path}")
