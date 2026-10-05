import os
import random
from PIL import Image

import torch
from torch.utils.data import Dataset


class TrashDataset(Dataset):
    """
    Adaptador de TrashNet para que pueda usarse con el pipeline
    del notebook de CNN del PDF.

    Por compatibilidad con las funciones de evaluación originales
    del PDF, se utilizan DOS clases:
        0 = glass
        1 = plastic

    Estructura esperada:

    trashnet/
        glass/
            imagen1.jpg
            imagen2.jpg
            ...
        plastic/
            imagen1.jpg
            imagen2.jpg
            ...

    El dataset se divide de forma estratificada por clase en:
        70 % train
        15 % val
        15 % test
    """

    classes = ["glass", "plastic"]

    class_to_idx = {
        "glass": 0,
        "plastic": 1
    }

    def __init__(
        self,
        root,
        split="train",
        transform=None,
        train_ratio=0.70,
        val_ratio=0.15,
        seed=42
    ):
        self.root = root
        self.split = split
        self.transform = transform

        if split not in ("train", "val", "test"):
            raise ValueError("split debe ser 'train', 'val' o 'test'")

        all_samples = []

        for class_name in self.classes:
            class_dir = os.path.join(root, class_name)

            if not os.path.isdir(class_dir):
                raise FileNotFoundError(
                    f"No se encontró la carpeta: {class_dir}"
                )

            files = [
                f for f in os.listdir(class_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]

            files.sort()

            # Semilla independiente por clase para que
            # train/val/test mantengan siempre la misma partición.
            rng = random.Random(seed)
            rng.shuffle(files)

            n = len(files)
            n_train = int(n * train_ratio)
            n_val = int(n * val_ratio)

            if split == "train":
                selected = files[:n_train]

            elif split == "val":
                selected = files[n_train:n_train + n_val]

            else:  # test
                selected = files[n_train + n_val:]

            for filename in selected:
                path = os.path.join(class_dir, filename)
                label = self.class_to_idx[class_name]
                all_samples.append((path, label))

        self.samples = all_samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        path, label = self.samples[index]

        # Se convierte a escala de grises para mantener
        # compatible la CNN del PDF: Conv2d(1, 16, ...).
        image = Image.open(path).convert("L")

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.long)
