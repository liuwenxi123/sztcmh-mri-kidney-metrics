# sztcmh-mri-kidney-metrics

深圳市中医院肾脏 MRI 指标测量工具，面向 NIfTI (`.nii` / `.nii.gz`) 影像、标签和 vMRE/sADC 工作流。

## Versions

- `v0-code-0`
  - 原始历史工程完整导入
- `v1`
  - 保行为重构，建立 `src/` 包结构、服务层、领域层和测试
- `v2`
  - 清理旧根目录文件，保留现代项目结构，并强化真实数据目录下的批量配对逻辑

## Repository Layout

```text
sztcmh-mri-kidney-metrics/
  main.py
  pyproject.toml
  README.md
  docs/
  data/
  scripts/
  src/
  tests/
```

## Main Structure

- `src/sztcmh_mri_kidney_metrics/app`
  - 应用入口和主窗口
- `src/sztcmh_mri_kidney_metrics/ui`
  - PyQt 界面层
- `src/sztcmh_mri_kidney_metrics/domain`
  - 纯算法逻辑
- `src/sztcmh_mri_kidney_metrics/services`
  - 文件提取、批量配对、导出、转换等服务
- `src/sztcmh_mri_kidney_metrics/models`
  - 指标结果数据模型
- `tests/unit`
  - 单元测试
- `data/samples/legacy-test-set`
  - 从旧工程迁移出来的历史样例数据

## Run

```bash
python main.py
```

## Tests

```bash
python -m unittest discover -s tests/unit -v
```

## Real Data Validation

本仓库已在真实目录 `D:/508Lab/深圳中医院/DWI` 上做过验证：

- 新的批量 workflow 可以忽略目录中的杂项文件
- 图像与标签现在按病例键配对，而不是只按数量和排序硬配对
- `stiff200-800` 与 `label/kidney`、`label/kidney2` 都可以得到有效批量结果
