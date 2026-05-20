import nibabel as nib
import numpy as np
from PyQt5.QtWidgets import QMessageBox


def process_images(selected_file1, selected_file2, selected_file3):
    # Load images
    img = nib.load(selected_file1)
    label = nib.load(selected_file2)
    label2 = nib.load(selected_file3)

    # print(img.shape)
    # (矢状面，冠状面，横切面)

    # [矢状100，横切100，冠状]

    # Extract data from images
    image_data = img.get_fdata()
    label_data = label.get_fdata()
    label_data2 = label2.get_fdata()

    print(image_data.shape)

    different_coords = np.argwhere(label_data != label_data2)
    print("Different coordinates:\n", len(different_coords))

    # Calculate midline index
    midline_index = image_data.shape[1] // 2

    # Left kidney analysis
    left_volume = np.sum(label_data[midline_index:, :, :] > 0)
    left_volume2 = np.sum(label_data2[midline_index:, :, :] > 0)

    print('l', left_volume, left_volume2)

    # print('左pixel差异层', different_layers)    # (矢状面，横切面)
    layer_pixels1 = label_data[midline_index:, :, :]
    layer_pixels2 = label_data2[midline_index:, :, :]
    different_coords = np.argwhere(layer_pixels1 != layer_pixels2)
    # different_coords[:, 1] += (midline_index)
    print("LEFT Different coordinates:\n", len(different_coords))




    # Right kidney analysis
    right_pixels = image_data[:midline_index, :, :][label_data[:midline_index, :, :] > 0]
    right_mean = np.mean(right_pixels)
    right_volume = np.sum(label_data[:midline_index, :, :] > 0)
    right_pixels2 = image_data[:midline_index, :, :][label_data[:midline_index, :, :] > 0]
    right_mean2 = np.mean(right_pixels2)
    right_volume2 = np.sum(label_data2[:midline_index, :, :] > 0)

    print('r', right_volume, right_volume2)

    layer_pixels1 = label_data[:midline_index, :, :]
    layer_pixels2 = label_data2[:midline_index, :, :]
    different_coords = np.argwhere(layer_pixels1 != layer_pixels2)
    print("RIGHT Different coordinates:\n", len(different_coords))


def get_different_coords(layer_pixels1, layer_pixels2):
    if not np.array_equal(layer_pixels1, layer_pixels2):
        return np.argwhere(layer_pixels1 != layer_pixels2)
    return None


if __name__ == '__main__':
    image = r'test/test/094_MREimage.nii.gz'
    image_ = r'D:\508\PancreasAPP123 (2)\Chang_Xiu_Ying_data.nii.gz'
    label1 = r'test/test/094_MRE_kidney.nii.gz'
    label2 = r'test/test/094_MRE_kidney_c12.nii.gz'

    image3 = r'test/test1/092_MRE.nii.gz'
    label3 = r'test/test1/092_MRE_pre.nii.gz'
    label3_ = r'test/test1/092_MRE_pre_c18.nii.gz'
    process_images(image, label1, label2)
