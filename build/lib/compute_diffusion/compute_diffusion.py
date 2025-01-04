#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修订版脚本：
1. JSON 配置和命令行合并逻辑保持不变；
2. 修正：
   - Avg slope = 使用整个数据的斜率；
   - Max/Min = 每段斜率的最大值和最小值；
   - D = (整体斜率) / (2 * dimension * time_unit)；
   - Error = ((Max slope - Min slope) / 2) / (2 * dimension * time_unit)。
3. 输出调整为：
   - 每段打印 "Segment i slope="；
   - 最后统一打印 "Avg=", "Max=", "Min=", "D=", "Error="。
"""

import argparse
import json
import os
import numpy as np

DEFAULT_JSON_FILE = "diffusion.json"
DEFAULT_CONFIG = {
    "filename": "msd_data.txt",
    "skip_row": 1,
    "time_index": 0,
    "msd_col": 1,    # index start from 0
    "time_unit": 1,  # default unit: ps, if fs you should set 0.001 
    "group_size": 4,
    "dimension": 1
}

def parse_command_line():
    parser = argparse.ArgumentParser(description="Compute slopes and D from data file.")
    parser.add_argument("--filename",    "-f",  type=str, help="MSD file path")
    parser.add_argument("--skip_row",          type=int, help="skip rows from head")
    parser.add_argument("--time_index",        type=int, help="Time column index (0-based)")
    parser.add_argument("--msd_col",           type=int, help="MSD column (0-based)")
    parser.add_argument("--time_unit",         type=int, help="Time unit：defult is ps,so set 1 when unit is ps, and set 0.001 when use fs")
    parser.add_argument("--group_size",        type=int, help="batch number")
    parser.add_argument("--dimension",         type=int, help="System dimension")
    args = parser.parse_args()
    cmd_config = {k: v for k, v in vars(args).items() if v is not None}
    return cmd_config

def load_or_init_config(cmd_config):
    if not cmd_config and not os.path.exists(DEFAULT_JSON_FILE):
        print("[INFO] 无 JSON 和命令行参数，生成默认配置文件并退出...")
        with open(DEFAULT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        exit(0)

    if os.path.exists(DEFAULT_JSON_FILE) and not cmd_config:
        print(f"[INFO] 加载现有配置文件 {DEFAULT_JSON_FILE}...")
        with open(DEFAULT_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    if not os.path.exists(DEFAULT_JSON_FILE) and cmd_config:
        config = DEFAULT_CONFIG.copy()
        config.update(cmd_config)
        print("[INFO] 无 JSON 文件，根据命令行生成...")
        with open(DEFAULT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return config

    if os.path.exists(DEFAULT_JSON_FILE) and cmd_config:
        print(f"[INFO] JSON 文件和命令行参数合并，命令行优先...")
        with open(DEFAULT_JSON_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        config.update(cmd_config)
        with open(DEFAULT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return config

def compute_slope(time_array, msd_array):
    """对 (time, msd) 做最小二乘拟合，返回斜率"""
    n = len(time_array)
    if n < 2:
        return 0.0
    sum_x = np.sum(time_array)
    sum_y = np.sum(msd_array)
    sum_xy = np.sum(time_array * msd_array)
    sum_x2 = np.sum(time_array ** 2)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x2 - sum_x ** 2
    if abs(denominator) < 1e-20:
        return 0.0
    return numerator / denominator

def main():
    cmd_config = parse_command_line()
    config = load_or_init_config(cmd_config)

    # 使用最终配置
    filename = config["filename"]
    skip_row = config["skip_row"]
    time_idx = config["time_index"]
    msd_idx = config["msd_col"]
    time_unit = config["time_unit"]
    group_size = config["group_size"]
    dimension = config["dimension"]

    print("\n[INFO] 最终配置：")
    print(json.dumps(config, indent=4))

    # 读取数据
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] 文件 {filename} 不存在！")
        return

    # 跳过指定行
    lines = lines[skip_row:]
    time_list, msd_list = [], []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        cols = line.split()
        time_list.append(float(cols[time_idx]))
        msd_list.append(float(cols[msd_idx]))

    time_array = np.array(time_list) * time_unit  # 转换时间单位为 ps
    msd_array = np.array(msd_list)

    n_data = len(time_array)
    if n_data == 0:
        print("[ERROR] 数据为空，请检查输入文件！")
        return

    block_size = n_data // group_size
    print(f"\n[INFO] 数据点数: {n_data}, 每段大小: {block_size}")

    # 累积式分段
    slopes = []
    for i in range(1, group_size + 1):
        end_idx = i * block_size if i < group_size else n_data
        sub_time = time_array[:end_idx]
        sub_msd = msd_array[:end_idx]

        slope = compute_slope(sub_time, sub_msd)
        slopes.append(slope)
        print(f"Segment {i} :  1 ~ {end_idx}  slope= {slope:.6f}")

    # 计算整体斜率（使用全体数据）
    avg_slope = compute_slope(time_array, msd_array)

    # Max 和 Min
    max_slope = np.max(slopes)
    min_slope = np.min(slopes)

    # 计算扩散系数 D
    D = avg_slope / (2 * dimension * time_unit)  # 转为 10^-4 cm^2/s

    # 计算误差
    D_error = (max_slope - min_slope) / (2 * 2 * dimension * time_unit)

    # 打印最终结果
    print(f"\n[RESULT] Avg= {avg_slope:.12f}")
    print(f"[RESULT] Max= {max_slope:.12f}")
    print(f"[RESULT] Min= {min_slope:.12f}")
    print(f"[RESULT] D= {D:.6f} (10^-4 cm^2/s)")
    print(f"[RESULT] Error= {D_error:.6f} (10^-4 cm^2/s)")

if __name__ == "__main__":
    main()

