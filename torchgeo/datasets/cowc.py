"""The `Cars Overhead With Context (COWC) <https://gdo152.llnl.gov/cowc/>`_ data set
is a large set of annotated cars from overhead. It is useful for training a device
such as a deep neural network to learn to detect and/or count cars.

The dataset has the following attributes:

1. Data from overhead at 15 cm per pixel resolution at ground (all data is EO).
2. Data from six distinct locations: Toronto, Canada; Selwyn, New Zealand;
   Potsdam and Vaihingen, Germany; Columbus, Ohio and Utah, United States.
3. 32,716 unique annotated cars. 58,247 unique negative examples.
4. Intentional selection of hard negative examples.
5. Established baseline for detection and counting tasks.
6. Extra testing scenes for use after validation.

If you use this dataset in your research, please cite the following paper:

* https://doi.org/10.1007/978-3-319-46487-9_48
"""

import abc
import bz2
import csv
import os
import tarfile
from typing import Any, Callable, List, Optional, Tuple

from PIL import Image
from torchvision.datasets import VisionDataset
from torchvision.datasets.utils import (
    check_integrity,
    download_url,
)


class _COWC(VisionDataset, abc.ABC):
    """Abstract base class for all COWC datasets."""

    @property
    @abc.abstractmethod
    def base_folder(self) -> str:
        """Subdirectory to find/store dataset in."""
        pass

    @property
    @abc.abstractmethod
    def base_url(self) -> str:
        """Base URL to download dataset from."""
        pass

    @property
    @abc.abstractmethod
    def filenames(self) -> List[str]:
        """List of files to download."""
        pass

    @property
    @abc.abstractmethod
    def md5s(self) -> List[str]:
        """List of MD5 checksums of files to download."""
        pass

    @property
    @abc.abstractmethod
    def filename(self) -> str:
        """Filename containing train/test split and target labels."""
        pass

    def __init__(
        self,
        root: str = "data",
        split: str = "train",
        transform: Optional[Callable[[Image.Image], Any]] = None,
        target_transform: Optional[Callable[[int], Any]] = None,
        transforms: Optional[Callable[[Image.Image, int], Tuple[Any, Any]]] = None,
        download: bool = False,
    ) -> None:
        """Initialize a new COWC dataset instance.

        Parameters:
            root: root directory where dataset can be found
            split: one of "train" or "test"
            transform: a function/transform that takes in a PIL image and returns a
                transformed version
            target_transform: a function/transform that takes in the target and
                transforms it
            transforms: a function/transform that takes input sample and its target as
                entry and returns a transformed version
            download: if True, download dataset and store it in the root directory

        Raises:
            AssertionError: if ``split`` argument is invalid
            RuntimeError: if ``download=False`` and data is not found, or checksums
                don't match
        """
        assert split in ["train", "test"]

        super().__init__(root, transforms, transform, target_transform)

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. "
                + "You can use download=True to download it"
            )

        self.images = []
        self.targets = []
        with open(
            os.path.join(self.root, self.base_folder, self.filename.format(split)),
            newline="",
        ) as f:
            reader = csv.reader(f, delimiter=" ")
            for row in reader:
                self.images.append(row[0])
                self.targets.append(row[1])

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """Return an index within the dataset.

        Parameters:
            index: index to return

        Returns:
            data and label at that index
        """
        image = self._load_image(index)
        target = int(self.targets[index])

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self) -> int:
        """Return the number of data points in the dataset.

        Returns:
            length of the dataset
        """
        return len(self.targets)

    def _load_image(self, index: int) -> Image.Image:
        """Load a single image.

        Parameters:
            index: index to return

        Returns:
            the image
        """
        return Image.open(
            os.path.join(
                self.root,
                self.base_folder,
                self.images[index],
            )
        ).convert("RGB")

    def _check_integrity(self) -> bool:
        """Check integrity of dataset.

        Returns:
            True if dataset MD5s match, else False
        """
        for filename, md5 in zip(self.filenames, self.md5s):
            if not check_integrity(
                os.path.join(self.root, self.base_folder, filename), md5
            ):
                return False
        return True

    def download(self) -> None:
        """Download the dataset and extract it."""

        if self._check_integrity():
            print("Files already downloaded and verified")
            return

        for filename, md5 in zip(self.filenames, self.md5s):
            download_url(
                self.base_url + filename,
                os.path.join(self.root, self.base_folder),
                filename=filename,
                md5=md5,
            )
            if filename.endswith(".tbz"):
                with tarfile.open(
                    os.path.join(self.root, self.base_folder, filename)
                ) as tar:
                    tar.extractall(os.path.join(self.root, self.base_folder))
            elif filename.endswith(".bz2"):
                filepath = os.path.join(self.root, self.base_folder, filename)
                with bz2.BZ2File(filepath) as old_fh:
                    data = old_fh.read()
                    with open(filepath[:-4], "wb") as new_fh:
                        new_fh.write(data)


class COWCDetection(_COWC):
    """COWC Dataset for car detection."""

    base_folder = "cowc_detection"
    base_url = (
        "https://gdo152.llnl.gov/cowc/download/cowc/datasets/patch_sets/detection/"
    )
    filenames = [
        "COWC_train_list_detection.txt.bz2",
        "COWC_test_list_detection.txt.bz2",
        "COWC_Detection_Toronto_ISPRS.tbz",
        "COWC_Detection_Selwyn_LINZ.tbz",
        "COWC_Detection_Potsdam_ISPRS.tbz",
        "COWC_Detection_Vaihingen_ISPRS.tbz",
        "COWC_Detection_Columbus_CSUAV_AFRL.tbz",
        "COWC_Detection_Utah_AGRC.tbz",
    ]
    md5s = [
        "c954a5a3dac08c220b10cfbeec83893c",
        "c6c2d0a78f12a2ad88b286b724a57c1a",
        "11af24f43b198b0f13c8e94814008a48",
        "22fd37a86961010f5d519a7da0e1fc72",
        "bf053545cc1915d8b6597415b746fe48",
        "23945d5b22455450a938382ccc2a8b27",
        "f40522dc97bea41b10117d4a5b946a6f",
        "195da7c9443a939a468c9f232fd86ee3",
    ]
    filename = "COWC_{split}_list_detection.txt"


class COWCCounting(_COWC):
    """COWC Dataset for car counting."""

    base_folder = "cowc_counting"
    base_url = (
        "https://gdo152.llnl.gov/cowc/download/cowc/datasets/patch_sets/counting/"
    )
    filenames = [
        "COWC_train_list_64_class.txt.bz2",
        "COWC_test_list_64_class.txt.bz2",
        "COWC_Counting_Toronto_ISPRS.tbz",
        "COWC_Counting_Selwyn_LINZ.tbz",
        "COWC_Counting_Potsdam_ISPRS.tbz",
        "COWC_Counting_Vaihingen_ISPRS.tbz",
        "COWC_Counting_Columbus_CSUAV_AFRL.tbz",
        "COWC_Counting_Utah_AGRC.tbz",
    ]
    md5s = [
        "187543d20fa6d591b8da51136e8ef8fb",
        "930cfd6e160a7b36db03146282178807",
        "bc2613196dfa93e66d324ae43e7c1fdb",
        "ea842ae055f5c74d0d933d2194764545",
        "19a77ab9932b722ef52b197d70e68ce7",
        "4009c1e420566390746f5b4db02afdb9",
        "daf8033c4e8ceebbf2c3cac3fabb8b10",
        "777ec107ed2a3d54597a739ce74f95ad",
    ]
    filename = "COWC_{split}_list_64_class.txt"


# TODO: add COCW-M datasets:
#
# * https://gdo152.llnl.gov/cowc/download/cowc-m/datasets/
# * https://github.com/LLNL/cowc
#
# Same as COCW datasets, but instead of binary classification there are 4 car classes:
#
# 1. Sedan
# 2. Pickup
# 3. Other
# 4. Unknown
#
# May need new abstract base class. Will need subclasses for different patch sizes.
