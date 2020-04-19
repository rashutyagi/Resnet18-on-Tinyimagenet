import torch
from skimage import io
import numpy as np
from torch.utils.data import Dataset
import random

def alldata(path):
    class_ids = [line.strip() for line in open( path + 'wnids.txt', 'r')]
    id_dict = {x:i for i, x in enumerate(class_ids)}
    all_classes = {line.split('\t')[0] : line.split('\t')[1].strip() for line in open( path + 'words.txt', 'r')}
    class_names = [all_classes[x] for x in class_ids]

    images = []
    labels = []

    # train data
    for value, key in enumerate(class_ids):
        images += [f'{path}train/{key}/images/{key}_{i}.JPEG' for i in range(500)]
        labels += [value for i in range(500)]

    # validation data
    for line in open( path + 'val/val_annotations.txt'):
        img_name, class_id = line.split('\t')[:2]
        images.append(f'{path}val/images/{img_name}')
        labels.append(id_dict[class_id])

    dataset = list(zip(images, labels))
    random.shuffle(dataset)

    return dataset, class_names

class TinyImagenetDataset(Dataset):
    """Tine Imagenet dataset reader."""

    def __init__(self, data, transform=None):
        """
        Args:
            data (string): zipped images and labels.
        """
        self.transform = transform
        self.images, self.labels = zip(*data)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        image = io.imread(self.images[idx], as_gray=False, pilmode="RGB")
        # We don't want one hot encoding here
        # https://pytorch.org/docs/master/nn.functional.html#torch.nn.functional.nll_loss
        #label = np.array([0]*200)
        #label[self.labels[idx]] = 1

        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx] #label
