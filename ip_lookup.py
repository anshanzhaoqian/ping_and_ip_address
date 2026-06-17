import socket
import ip2region.util as util
import ip2region.searcher as xdb
import platform
import subprocess
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)
    
    
def ping_host(host):
    # Determine the operating system
    current_os = platform.system().lower()
    
    # Configure the count parameter based on the OS
    # Windows uses '-n', while Linux/macOS uses '-c'
    if current_os == "windows":
        command = ["ping", "-n", "5", host]
    else:
        command = ["ping", "-c", "5", host]
    
    # Run the command and stream the output directly to the console
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"\nFailed to reach {host}")
    except FileNotFoundError:
        print("\nPing command not found on this system.")


def main():
    # 提示用户输入网址
    url = input("请输入网址: ").strip()
    
    # 使用 socket.getaddrinfo 获取 IP 地址
    try:
        addr_info = socket.getaddrinfo(url, None)
        ip = addr_info[0][4][0]
        print(f"解析到的 IP 地址: {ip}")
    except socket.gaierror as e:
        print(f"无法解析网址: {e}")
        return
    
    # 判断 IP 类型并设置对应的 db_path 和 version
    if ":" in ip:
        # IPv6
        real_path = resource_path("ip2region_v6.xdb")
        db_path = real_path
        version = util.IPv6
        print("检测到 IPv6 地址")
    else:
        # IPv4
        real_path = resource_path("ip2region_v4.xdb")
        db_path = real_path
        version = util.IPv4
        print("检测到 IPv4 地址")
    
    try:
        util.verify_from_file(db_path)
    except Exception as e:
        print(f"binding is not applicable for xdb file '{db_path}':{str(e)}")
        return
    
    try:
        searcher = xdb.new_with_file_only(version, db_path)
    except Exception as e:
        print(f"failed to new_with_file_only:{str(e)}")
        return
    
    # 使用 py-ip2region 的 searcher 查询 region 信息
    try:
        region_info = searcher.search(ip)
        print(f"IP 归属地信息: {region_info}")
    except Exception as e:
        print(f"查询 IP 归属地失败: {e}")
        
    ping_host(url)

if __name__ == "__main__":
    main()
