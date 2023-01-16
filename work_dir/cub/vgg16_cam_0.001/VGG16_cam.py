# https://pytorch.org/vision/0.8/_modules/torchvision/models/vgg.html#vgg16

import torch
import torch.nn as nn


class VGG(nn.Module):

    def __init__(self, features, num_classes=200):
        super(VGG, self).__init__()
        self.num_classes = num_classes
        self.features = features
        self.w = nn.Conv2d(1024, self.num_classes, 1, bias = False) # conv weight => (num_classes, k, 1, 1)

    def forward(self, x):
        x = self.features(x)

        GAP = self.w(x)
        S_c = torch.mean(GAP.reshape(GAP.shape[0], self.num_classes, -1), 2)

        return S_c, GAP

def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        elif v == 'conv':
            conv2d = nn.Conv2d(in_channels, 1024, kernel_size=3, padding=1, groups=2)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(1024), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = 1024
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


cfgs = {
    'GAP': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'conv'],
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}


def _vgg(cfg, batch_norm, **kwargs):
    model = VGG(make_layers(cfgs[cfg], batch_norm=batch_norm), **kwargs)
    return model


def vgg_gap(**kwargs):
    return _vgg('GAP', False, **kwargs)

def vgg_gap_bn(**kwargs):
    return _vgg('GAP', True, **kwargs)