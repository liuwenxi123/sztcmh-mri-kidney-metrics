import os
import nibabel as nib
from cal import calculate_middle_means_original  # 修改为你保存函数的模块名

# 图像和标签路径（请根据系统换成绝对路径或转义反斜杠）
images_dir = r'Z:\data\LWX\ZhongYiYuan\data\2025_0612-tmp\MRE106-123image\images'
labels_dir = r'Z:\data\LWX\ZhongYiYuan\data\2025_0612-tmp\MRE106-123image\pred_cortex'

if __name__ == "__main__":
    image_files = sorted([f for f in os.listdir(images_dir) if f.endswith('.nii.gz') or f.endswith('.nii')])
    label_files = sorted([f for f in os.listdir(labels_dir) if f.endswith('.nii.gz') or f.endswith('.nii')])

    if len(image_files) != len(label_files):
        print("❗ 图像和标签数量不一致")
        exit()

    for image_file, label_file in zip(image_files, label_files):
        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, label_file)

        if not os.path.exists(image_path) or not os.path.exists(label_path):
            print(f"❗ 缺失文件: {image_file} 或 {label_file}")
            continue

        image_data = nib.load(image_path).get_fdata()
        label_data = nib.load(label_path).get_fdata()

        try:
            all_mean, left_mean, right_mean = calculate_middle_means_original(image_data, label_data)
            print(f"🧾 {image_file} → 全肾: {all_mean:.2f}, 左肾: {left_mean}, 右肾: {right_mean}")
        except Exception as e:
            print(f"⚠️ 处理 {image_file} 时出错: {str(e)}")
