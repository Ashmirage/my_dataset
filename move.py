import os
import shutil
import random

def split_and_rename_dataset_v2():
    # ================= 配置区域 =================
    # 1. 源文件路径
    src_img_dir = r"C:\Users\36137\Mycode\yolo\my_test\dataset\images"
    src_lbl_dir = r"C:\Users\36137\Mycode\yolo\my_test\dataset\labels"

    # 2. 目标根路径
    target_root_images = r"C:\Users\36137\Mycode\yolo\my_test\datasets\images"
    target_root_labels = r"C:\Users\36137\Mycode\yolo\my_test\datasets\labels"

    # 3. 详细的目标子路径
    train_img_dst = os.path.join(target_root_images, "train")
    val_img_dst   = os.path.join(target_root_images, "val")
    train_lbl_dst = os.path.join(target_root_labels, "train")
    val_lbl_dst   = os.path.join(target_root_labels, "val")

    # 4. 划分比例
    TRAIN_RATIO = 0.8
    # ===========================================

    # --- 1. 创建目标目录 ---
    for d in [train_img_dst, val_img_dst, train_lbl_dst, val_lbl_dst]:
        os.makedirs(d, exist_ok=True)

    # --- 2. 获取源文件 ---
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tif')
    
    if not os.path.exists(src_img_dir):
        print(f"[错误] 源目录不存在: {src_img_dir}")
        return

    all_images = [f for f in os.listdir(src_img_dir) if f.lower().endswith(valid_exts)]
    
    if not all_images:
        print("[错误] 源目录中没找到图片！")
        return

    # --- 3. 随机打乱 ---
    random.shuffle(all_images)
    
    # --- 4. 划分 ---
    split_idx = int(len(all_images) * TRAIN_RATIO)
    train_files = all_images[:split_idx]
    val_files = all_images[split_idx:]
    
    print(f"总数: {len(all_images)} -> 训练集: {len(train_files)}, 验证集: {len(val_files)}")
    print("-" * 50)

    # --- 5. 定义处理函数 ---
    def process_files(file_list, img_dst_dir, lbl_dst_dir, prefix_code):
        """
        file_list: 图片文件名列表
        img_dst_dir: 图片目标文件夹
        lbl_dst_dir: 标签目标文件夹
        prefix_code: '001' 或 '002'
        """
        count = 0
        missing_labels = 0
        
        for idx, filename in enumerate(file_list):
            # 1. 构造新名字: 前缀_五位序号 (例如: 001_00005.jpg)
            # idx+1 表示从1开始计数
            ext = os.path.splitext(filename)[1] # 获取原后缀 (.jpg)
            new_name_base = f"{prefix_code}_{str(idx + 1).zfill(5)}"
            
            new_img_name = new_name_base + ext
            new_lbl_name = new_name_base + ".txt"
            
            # 2. 源路径
            src_img_path = os.path.join(src_img_dir, filename)
            # 推断标签源文件名 (假设标签和图片同名，只是后缀不同)
            original_lbl_name = os.path.splitext(filename)[0] + ".txt"
            src_lbl_path = os.path.join(src_lbl_dir, original_lbl_name)
            
            # 3. 目标路径
            dst_img_path = os.path.join(img_dst_dir, new_img_name)
            dst_lbl_path = os.path.join(lbl_dst_dir, new_lbl_name)
            
            try:
                # 移动图片
                shutil.move(src_img_path, dst_img_path)
                
                # 移动标签 (如果有)
                if os.path.exists(src_lbl_path):
                    shutil.move(src_lbl_path, dst_lbl_path)
                else:
                    # 如果没有标签，只提示一下
                    # print(f"[警告] 缺标签: {filename}") 
                    missing_labels += 1
                
                count += 1
            except Exception as e:
                print(f"[错误] 处理 {filename} 失败: {e}")
        
        return count, missing_labels

    # --- 6. 执行处理 ---
    print("正在处理训练集 (001_xxxxx)...")
    t_cnt, t_miss = process_files(train_files, train_img_dst, train_lbl_dst, "001")
    
    print("正在处理验证集 (002_xxxxx)...")
    v_cnt, v_miss = process_files(val_files, val_img_dst, val_lbl_dst, "002")

    print("-" * 50)
    print("处理完成！")
    print(f"训练集移动: {t_cnt} (无标签: {t_miss})")
    print(f"验证集移动: {v_cnt} (无标签: {v_miss})")

if __name__ == "__main__":
    split_and_rename_dataset_v2()