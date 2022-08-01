import torch
from torch.nn import Conv2d, Sequential, ModuleList, ReLU
from ..nn.resnet50 import ResNet, Bottleneck

from .ssd import SSD
from .predictor import Predictor
from .config import resnet_ssd_config as config

def get_resnet50_base_layer():
    model = ResNet(Bottleneck, [3, 4, 6, 3])
    features = list([model.conv1, model.bn1, model.relu, model.maxpool, model.layer1, model.layer2, model.layer3, model.layer4])    
    base_net = Sequential(*features)
    return base_net

def create_resnet50_ssd(num_classes, is_test=False):
#     resnet50 = ResNet(Bottleneck, [3, 4, 6, 3])
#     del resnet50.fc
#     base_net = resnet50
    base_net = get_resnet50_base_layer()

    source_layer_indexes = [
        7,
        len(base_net),
    ]
    extras = ModuleList([
        Sequential(
            Conv2d(in_channels=2048, out_channels=256, kernel_size=1),
            ReLU(),
            Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=2, padding=1),
            ReLU()
        ),
        Sequential(
            Conv2d(in_channels=512, out_channels=128, kernel_size=1),
            ReLU(),
            Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1),
            ReLU()
        ),
        Sequential(
            Conv2d(in_channels=256, out_channels=128, kernel_size=1),
            ReLU(),
            Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1),
            ReLU()
        ),
        Sequential(
            Conv2d(in_channels=256, out_channels=128, kernel_size=1),
            ReLU(),
            Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1),
            ReLU()
        )
    ])
    #modification
    regression_headers = ModuleList([
        Conv2d(in_channels=1024, out_channels=1 * 5, kernel_size=3, padding=1),
        Conv2d(in_channels=2048, out_channels=1 * 5, kernel_size=3, padding=1),
        Conv2d(in_channels=512, out_channels=1 * 5, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * 5, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * 5, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * 5, kernel_size=3, padding=1), # TODO: change to kernel_size=1, padding=0?
    ])

    classification_headers = ModuleList([
        Conv2d(in_channels=1024, out_channels=1 * num_classes, kernel_size=3, padding=1),
        Conv2d(in_channels=2048, out_channels=1 * num_classes, kernel_size=3, padding=1),
        Conv2d(in_channels=512, out_channels=1 * num_classes, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * num_classes, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * num_classes, kernel_size=3, padding=1),
        Conv2d(in_channels=256, out_channels=1 * num_classes, kernel_size=3, padding=1), # TODO: change to kernel_size=1, padding=0?
    ])

    return SSD(num_classes, base_net, source_layer_indexes,
               extras, classification_headers, regression_headers, is_test=is_test, config=config)


def create_resnet50_ssd_predictor(net, candidate_size=200, nms_method=None, sigma=0.5, device=None):
    predictor = Predictor(net, config.image_size, config.image_mean,
                          config.image_std,
                          nms_method=nms_method,
                          iou_threshold=config.iou_threshold,
                          candidate_size=candidate_size,
                          sigma=sigma,
                          device=device)
    return predictor
