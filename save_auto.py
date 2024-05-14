import os
import shutil
import time
from datetime import datetime

# 源文件路径
source_dir = 'C:\\ProgramData\\PopCap Games\\PlantsVsZombies\\pvzHE\\yourdata'

# 备份目录路径
backup_dir = 'C:\\Users\\Pan\\Desktop\\temp\\save_auto\\data'

# 自动保存的时间间隔（秒）
interval = 5 # 每隔5秒保存一次

# 保留的备份数量
max_backups = 3

def create_backup():
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # 获取当前时间并格式化为字符串
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # 创建新的备份子目录
    current_backup_dir = os.path.join(backup_dir, f'backup_{timestamp}')
    os.makedirs(current_backup_dir)

    # 复制源目录中的所有文件到备份子目录
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        backup_file = os.path.join(current_backup_dir, filename)

        if os.path.isfile(source_file):  # 只复制文件，忽略子目录
            shutil.copy2(source_file, backup_file)
            print(f'文件 {filename} 已备份到 {current_backup_dir}')

    # 检查并删除旧的备份
    manage_backups()

def manage_backups():
    # 获取备份目录中的所有备份子目录，按创建时间排序
    backups = [os.path.join(backup_dir, d) for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
    backups.sort(key=os.path.getctime)

    # 如果备份数量超过 max_backups，则删除最旧的备份
    while len(backups) > max_backups:
        oldest_backup = backups.pop(0)
        shutil.rmtree(oldest_backup)
        print(f'已删除旧的备份目录 {oldest_backup}')

def should_create_backup():
    # 获取源目录中的文件个数
    source_files_count = len([f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))])

    # 获取最新的备份目录中的文件个数
    backups = [os.path.join(backup_dir, d) for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
    backups.sort(key=os.path.getctime)

    if backups:
        latest_backup_dir = backups[-1]
        latest_backup_files_count = len([f for f in os.listdir(latest_backup_dir) if os.path.isfile(os.path.join(latest_backup_dir, f))])
    else:
        latest_backup_files_count = 0

    print(f'源目录文件数: {source_files_count}, 最新备份目录文件数: {latest_backup_files_count}')
    return source_files_count >= latest_backup_files_count

try:
    while True:
        if should_create_backup():
            create_backup()
        else:
            print('源目录文件数少于最新备份目录文件数，跳过此次备份')
        time.sleep(interval)
except KeyboardInterrupt:
    print('自动备份已停止')