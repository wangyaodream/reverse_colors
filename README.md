# 图片颜色反转工具

一个简单易用的Python图片处理工具，支持图片颜色反转和黑白转换功能。

## 功能特性

- **颜色反转**：将图片的颜色进行反转处理
- **黑白转换**：将彩色图片转换为黑白图片，可自定义阈值
- **批量处理**：支持批量处理指定目录中的所有PNG文件
- **单张处理**：支持对特定图片进行单独处理和参数调整
- **灵活输出**：可自定义输出文件名和路径

## 依赖要求

```bash
pip install opencv-python numpy
```

## 使用方法

### 批量处理模式

处理整个目录中的所有PNG文件：

```bash
# 批量反转颜色
python color_reverse.py reverse ./images ./output

# 批量黑白转换（默认阈值127）
python color_reverse.py bw ./images ./output

# 批量黑白转换（自定义阈值200）
python color_reverse.py bw ./images ./output 200
```

### 单张图片处理模式

针对特定图片进行处理：

```bash
# 反转颜色（自动生成输出文件名）
python color_reverse.py reverse ./images/test.png

# 反转颜色（指定输出文件名）
python color_reverse.py reverse ./images/test.png ./output/test-custom.png

# 黑白转换（自定义阈值150）
python color_reverse.py bw ./images/test.png ./output/test-bw.png 150
```

## 参数说明

- `<模式>`：处理模式
  - `reverse`：颜色反转
  - `bw`：黑白转换
- `<输入路径>`：输入文件或目录路径
- `<输出路径>`：输出文件或目录路径（可选）
- `[阈值]`：黑白转换的阈值参数（可选，默认127）

## 输出文件命名规则

- **批量处理**：原文件名 + `-reversed` + 扩展名
  - 例：`image.png` → `image-reversed.png`
- **单张处理**：如果不指定输出路径，则为原文件名 + `_reversed` 或 `_bw` + 扩展名

## 项目结构

```
color_reverse/
├── color_reverse.py    # 主程序文件
├── images/            # 输入图片目录
├── output/            # 输出图片目录
└── README.md          # 说明文档
```

## 示例

假设你有一个包含多张PNG图片的`images`目录：

1. **批量处理所有图片**：
   ```bash
   python color_reverse.py reverse ./images ./output
   ```

2. **测试单张图片效果**：
   ```bash
   python color_reverse.py bw ./images/test.png ./output/test-bw.png 150
   ```

3. **找到最佳参数后批量处理**：
   ```bash
   python color_reverse.py bw ./images ./output 150
   ```

## 注意事项

- 目前只支持PNG格式的图片文件
- 输出目录不存在时会自动创建
- 建议先用单张模式测试参数效果，再进行批量处理
- 黑白转换的阈值范围通常在0-255之间，数值越高背景越容易被识别为黑色

## 许可证

MIT License