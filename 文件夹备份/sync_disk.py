import os, shutil, psutil, time, threading


# version 0.1
# 支持同一台计算机上，不同磁盘不同文件夹之间的同步
# 支持动态插拔移动硬盘与U盘
# 填好配置，启动程序，后台静默处理
# only win
#
# todo: mac
# todo: 多台电脑相互备份

def src_file_dst(path, src, dst):
    return os.path.join(dst, path.lstrip(src).lstrip('/').lstrip('\\'))


def sync(src_dir, dst_dir):
    print(f"{time.strftime('%Y-%m-%d %X')} begin sync {src_dir} to {dst_dir}")
    err = []
    # copy src to dst
    for root, dirs, files in os.walk(src_dir):
        for dir in dirs:
            src_path = os.path.join(root, dir)
            dst_path = src_file_dst(src_path, src_dir, dst_dir)
            try:
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)
            except:
                err.append(f'E: copy {src_path} to {dst_path}')
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = src_file_dst(src_path, src_dir, dst_dir)
            if not os.path.exists(dst_path) or os.path.getmtime(src_path) != os.path.getmtime(dst_path):  # 修改时间不同
                try:
                    shutil.copyfile(src_path, dst_path)
                    os.utime(dst_path, (os.path.getatime(src_path), os.path.getmtime(src_path)))  # 修改修改时间
                except:
                    err.append(f'E: copy {src_path} to {dst_path}')
    # delete dst not in src
    for root, dirs, files in os.walk(dst_dir):
        for dir in dirs:
            dst_path = os.path.join(root, dir)
            src_path = src_file_dst(dst_path, dst_dir, src_dir)
            if not os.path.exists(src_path):
                try:
                    os.rmdir(dst_path)
                except:
                    err.append(f'E: remove {dst_path}')
        for file in files:
            dst_path = os.path.join(root, file)
            src_path = src_file_dst(dst_path, dst_dir, src_dir)
            if not os.path.exists(src_path):
                try:
                    os.remove(dst_path)
                except:
                    err.append(f'E: remove {dst_path}')
    err_str = f', with {len(err)} errors \n' + "\n".join(err) if len(err) > 0 else ""
    print(f"{time.strftime('%Y-%m-%d %X')} sync over. {src_dir} to {dst_dir} {err_str}")


def scan_disk(src, dst):
    '''
    扫描磁盘，确认待备份磁盘是否插入电脑
    :param src:
    :param dst:
    :return:
    '''
    disks = [x.device for x in psutil.disk_partitions()]
    re_src, re_dst = None, None
    srcs = [os.path.join(d, src) for d in disks]
    srcs.extend([src])
    for src in srcs:
        if os.path.exists(src):
            re_src = src
            break
    dsts = [os.path.join(d, dst) for d in disks]
    dsts.extend([dst])
    for dst in dsts:
        if os.path.exists(dst):
            re_dst = dst
            break
    return re_src, re_dst


def sync_wait_time(src, dst, tim=60):
    print(f'{src} to {dst} start')
    while True:
        src, dst = scan_disk(src, dst)
        if src is not None and dst is not None:
            sync(src, dst)
            time.sleep(tim)
        else:
            time.sleep(5)  # 失败重试


def main():
    print('server start')
    for cfg in __cfg:
        # sync_wait_time(*cfg)
        threading.Thread(target=sync_wait_time, args=cfg).start()


# 待备份文件夹，仓库文件夹，备份间隔时间
# 可以忽略盘符，以支持移动硬盘和U盘
# 得先确保俩文件夹存在
__cfg = [
    ['folder1', 'folder2', 2],
]

if __name__ == '__main__':
    main()
