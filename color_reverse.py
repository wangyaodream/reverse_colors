import cv2
import numpy as np
import sys
import os


def convert_to_black_white(image_path, output_path=None, background_threshold=200):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return False

    # 转换为HSV颜色空间，更容易处理颜色
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 获取亮度通道
    v_channel = hsv[:,:,2]
    
    # 创建掩码：背景（高亮度）为黑色，其他（文字和代码）为白色
    mask = np.ones_like(v_channel) * 255
    mask[v_channel > background_threshold] = 0
    
    # 创建输出图像（全黑背景）
    output = np.zeros_like(img)
    
    # 在非背景区域（掩码为255的地方）设置为白色
    output[mask == 255] = 255

    # 如果没有指定输出路径，则在原文件名基础上添加后缀
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_bw{ext}"

    # 保存结果
    cv2.imwrite(output_path, output)
    print(f"已保存黑白图片到: {output_path}")
    return True

def reverse_colors(image_path, output_path=None):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return False

    # 反转颜色
    inverted = cv2.bitwise_not(img)

    # 如果没有指定输出路径，则在原文件名基础上添加后缀
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_reversed{ext}"

    # 保存结果
    cv2.imwrite(output_path, inverted)
    print(f"已保存反转后的图片到: {output_path}")
    return True

def process_directory(input_dir, output_dir, mode="reverse", threshold=127):
    """批量处理目录中的所有PNG文件"""
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"输入目录不存在: {input_dir}")
        return False
    
    # 获取目录中的所有PNG文件
    png_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    
    if not png_files:
        print(f"在目录 {input_dir} 中没有找到PNG文件")
        return False
    
    print(f"找到 {len(png_files)} 个PNG文件，开始处理...")
    
    success_count = 0
    for filename in png_files:
        input_path = os.path.join(input_dir, filename)
        
        # 生成输出文件名（在原文件名基础上加-reversed后缀）
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}-reversed{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"正在处理: {filename}")
        
        # 根据模式处理文件
        if mode == "reverse":
            success = reverse_colors(input_path, output_path)
        elif mode == "bw":
            success = convert_to_black_white(input_path, output_path, threshold)
        else:
            print(f"未知的模式: {mode}")
            continue
            
        if success:
            success_count += 1
    
    print(f"处理完成！成功处理了 {success_count}/{len(png_files)} 个文件")
    return True


def main():
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  批量处理: python color_reverse.py <模式> <输入目录> <输出目录> [阈值]")
        print("  单张处理: python color_reverse.py <模式> <输入文件路径> [输出文件路径] [阈值]")
        print("模式选项:")
        print("  reverse - 反转颜色")
        print("  bw     - 转换为黑白")
        print("示例:")
        print("  python color_reverse.py reverse ./images ./output")
        print("  python color_reverse.py bw ./images/test.png ./output/test-bw.png 150")
        return

    mode = sys.argv[1]
    input_path = sys.argv[2]
    
    if mode not in ["reverse", "bw"]:
        print(f"未知的模式: {mode}")
        print("可用模式: reverse, bw")
        return

    # 判断是文件还是目录
    if os.path.isfile(input_path):
        # 单张图片处理模式
        if not input_path.lower().endswith('.png'):
            print("错误: 只支持PNG文件")
            return
            
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        threshold = int(sys.argv[4]) if len(sys.argv) > 4 and mode == "bw" else 127
        
        print(f"单张图片处理模式: {input_path}")
        
        if mode == "reverse":
            success = reverse_colors(input_path, output_path)
        elif mode == "bw":
            success = convert_to_black_white(input_path, output_path, threshold)
            
        if success:
            print("处理完成！")
        else:
            print("处理失败！")
            
    elif os.path.isdir(input_path):
        # 批量处理模式
        if len(sys.argv) < 4:
            print("批量处理需要指定输出目录")
            print("使用方法: python color_reverse.py <模式> <输入目录> <输出目录> [阈值]")
            return
            
        output_dir = sys.argv[3]
        threshold = int(sys.argv[4]) if len(sys.argv) > 4 and mode == "bw" else 127
        
        print(f"批量处理模式: {input_path} -> {output_dir}")
        process_directory(input_path, output_dir, mode, threshold)
    else:
        print(f"错误: 输入路径不存在或不是有效的文件/目录: {input_path}")


if __name__ == "__main__":
    main()