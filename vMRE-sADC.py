import os
import numpy as np
import nibabel as nib
import pandas as pd

vMRE_label_directory = r'D:\508\ZhongYiYuan\Data-T\label\cortex'

b_type = '200-800'
vMRE_image_directory1 = r'D:\508\ZhongYiYuan\Data-T\vMRE'
sADC_image_directory1 = r'D:\508\ZhongYiYuan\Data-T\sADC'
vMRE_image_directory = os.path.join(vMRE_image_directory1, b_type)
sADC_image_directory = os.path.join(vMRE_image_directory1, b_type)

thresholds = 0
result_path = r'D:\508\ZhongYiYuan\Data-T'
name = 'cortexROI'

# 获取所有图像文件
vMRE_image_files = [f for f in os.listdir(vMRE_image_directory) if f.endswith('.nii.gz') or f.endswith('.nii')]
vMRE_label_files = [f for f in os.listdir(vMRE_label_directory) if f.endswith('.nii.gz') or f.endswith('.nii')]
sADC_image_files = [f for f in os.listdir(sADC_image_directory) if f.endswith('.nii.gz') or f.endswith('.nii')]

# 创建一个DataFrame来保存结果
result_df = pd.DataFrame()

# 遍历每个图像文件
for i in range(len(vMRE_image_files)):
    # 构建图像文件路径和对应的标签文件路径
    vMRE_image_file_path = os.path.join(vMRE_image_directory, vMRE_image_files[i])
    vMRE_label_file_path = os.path.join(vMRE_label_directory, vMRE_label_files[i])
    sADC_image_file_path = os.path.join(sADC_image_directory, sADC_image_files[i])

    # 读取图像和标签数据
    vMRE_image = nib.load(vMRE_image_file_path).get_fdata()
    vMRE_label = nib.load(vMRE_label_file_path).get_fdata()
    sADC_image = nib.load(sADC_image_file_path).get_fdata()

    # 获取标签中像素值为1的位置
    label_positions = np.nonzero(vMRE_label)    # 原始标签
    vMRE_original_image = vMRE_image[label_positions]   # 原始vMRE图像
    sADC_original_image = sADC_image[label_positions]   # 原始sADC图像

    # 获取 原始vMRE 中为0的位置
    zero_positions = np.where(vMRE_original_image <= thresholds)

    # 删除这些位置的点（置零），得到一个新的标签
    new_label_data = np.copy(vMRE_label)
    new_label_data[
        label_positions[0][zero_positions], label_positions[1][zero_positions], label_positions[2][zero_positions]] = 0

    # 获取新标签中的覆盖信息
    vMRE_overlay_data = vMRE_image[new_label_data.nonzero()]   # 新vMRE图像
    sADC_overlay_data = sADC_image[new_label_data.nonzero()]   # 新sADC图像

    # 统计像素点
    n_vMRE = np.count_nonzero(vMRE_overlay_data)    # vMRE像素点总数
    n_sADC = np.count_nonzero(sADC_overlay_data)
    n_loss = np.count_nonzero(vMRE_original_image) - n_vMRE     # 被筛掉的像素点数

    # 计算像素均值
    vMRE_original_mean = f"{np.mean(vMRE_original_image):.6f}"
    sADC_original_mean = f"{np.mean(sADC_original_image):.9f}"
    vMRE_new_mean = f"{np.mean(vMRE_overlay_data):.6f}"
    sADC_new_mean = f"{np.mean(sADC_overlay_data):.9f}"

    prefix = '_'.join(vMRE_image_files[i].split('_')[:2])   # 病人编号
    print(prefix)

    print('未筛选vMRE ROI均值：', str(vMRE_original_mean))
    print('未筛选sADC ROI均值：', str(sADC_original_mean))
    print('已筛选vMRE ROI均值：', str(vMRE_new_mean))
    print('已筛选sADC ROI均值：', str(sADC_new_mean))
    print('像素点总数：', str(n_vMRE))
    print('不符合的像素点总数：', str(n_loss))

    prefix = '_'.join(vMRE_image_files[i].split('_')[:2])   # 病人编号


    # 将结果添加到DataFrame中
    result_df = pd.concat([result_df, pd.DataFrame({
        'Image_File': [prefix],
        'origin_vMRE': [vMRE_original_mean],
        'origin_sADC': [sADC_original_mean],
        'new_vMRE': [vMRE_new_mean],
        'new_sADC': [sADC_new_mean],
    })])

# 将结果保存到Excel表格
result_name = name + '.xlsx'
result_file = os.path.join(result_path, result_name)

result_df.to_excel(result_file, index=False)
