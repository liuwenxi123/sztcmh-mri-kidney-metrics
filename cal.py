import numpy as np

def calculate_middle_means_original(image_data, label_data):
    """
    从原始图中提取左右肾和全肾中间三层像素均值（原始逻辑封装版）
    """

    first_non_zero_page = None
    last_non_zero_page = None
    first_left_non_zero_page = None
    last_left_non_zero_page = None
    first_right_non_zero_page = None
    last_right_non_zero_page = None

    midline_index = image_data.shape[0] // 2  # 矢状面分界线

    for z in range(label_data.shape[2]):
        # 检查当前冠状面是否有非零标签
        if np.any(label_data[:, :, z] > 0):  # 全肾
            if first_non_zero_page is None:
                first_non_zero_page = z
            last_non_zero_page = z
        if np.any(label_data[:midline_index, :, z] > 0):  # 左肾
            if first_left_non_zero_page is None:
                first_left_non_zero_page = z
            last_left_non_zero_page = z
        if np.any(label_data[midline_index:, :, z] > 0):  # 右肾
            if first_right_non_zero_page is None:
                first_right_non_zero_page = z
            last_right_non_zero_page = z

    mid_index = (first_non_zero_page + last_non_zero_page) / 2
    mid_left_index = (first_left_non_zero_page + last_left_non_zero_page) / 2
    mid_right_index = (first_right_non_zero_page + last_right_non_zero_page) / 2

    coronal_middle_slices = slice(int(mid_index - 1), int(mid_index + 1))  # 中间三层
    coronal_left_middle_slices = slice(int(mid_left_index - 1), int(mid_left_index + 1))  # 中间三层
    coronal_right_middle_slices = slice(int(mid_right_index - 1), int(mid_right_index + 1))  # 中间三层

    # 全肾
    all_kidney_pixels = image_data[:, :, coronal_middle_slices][
        label_data[:, :, coronal_middle_slices] > 0]
    all_kidney_mean = np.mean(all_kidney_pixels) if len(all_kidney_pixels) > 0 else None

    # 左肾
    left_kidney_pixels = image_data[:midline_index, :, coronal_left_middle_slices][
        label_data[:midline_index, :, coronal_left_middle_slices] > 0]
    left_kidney_mean = np.mean(left_kidney_pixels) if len(left_kidney_pixels) > 0 else None

    # 右肾
    right_kidney_pixels = image_data[midline_index:, :, coronal_right_middle_slices][
        label_data[midline_index:, :, coronal_right_middle_slices] > 0]
    right_kidney_mean = np.mean(right_kidney_pixels) if len(right_kidney_pixels) > 0 else None

    return all_kidney_mean, left_kidney_mean, right_kidney_mean
