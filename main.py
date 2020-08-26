import os
import re
import signal
import psutil
import configparser


def get_ports(port_str):
    """
    从配置文件获得目标端口，返回端口列表
    :param port_str: 端口str
    :return: 端口list
    """
    if "," not in port_str:
        return [int(port_str)]
    ports = port_str.split(",")
    return [p for p in ports if p != ""]


def confirm():
    """
    确认是否kill掉目标进程
    :return:
    """
    print(process.name())
    print("是否kill掉？[y]/n:")
    input_item = input()
    return input_item == "" or input_item.lower() == "y"


def creat_conf():
    s = """[main]
# 需要找出占用的端口格式：7000,8000,9000
target_ports = 7000
# 是否不询问直接kill掉进程True/False
quiet = False"""
    with open("cleanPort.ini", "wb") as f:
        f.write(s.encode("utf8"))


if __name__ == '__main__':
    # 没有配置文件，自动创建一个
    if not os.path.exists("cleanPort.ini"):
        creat_conf()
        print("没有找到配置文件，已经自动创建在程序目录下：cleanPort.ini")
        print("请配置后重新运行本程序,回车键退出")
        input()
        exit(0)

    # 读取配置文件
    config = configparser.ConfigParser()
    conf = config.read('cleanPort.ini', encoding="utf8")
    is_quiet = config["main"]["quiet"] == "True"
    ports = get_ports(config["main"]["target_ports"])

    for port in ports:
        pid_regex = re.compile(r"(\d*)\n$")
        result = os.popen('netstat -ano | findstr "%s"' % port)
        print("找到以下进程占用%s端口：" % port)
        for r in result:
            pid = pid_regex.findall(r)
            if not pid:
                continue
            pid = int(pid[0])
            process = psutil.Process(pid)
            print(process.name())
            if is_quiet or confirm():
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except PermissionError:
                    pass

    print("\n执行完毕,回车退出")
    input()