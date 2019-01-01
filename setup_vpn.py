import pysftp


def setup(ip, username, password):
    sftp = pysftp.Connection(ip, username=username, password=password)
    sftp.put('install.sh')
    print(sftp.execute("bash install.sh"))
    sftp.execute("mkdir profiles")
    sftp.execute("mv /root/yourkeyfile.ovpn /root/profiles/yourkeyfile.ovpn")
    sftp.get_d('/root/profiles', '/Users/Adam/Desktop')


if __name__ == "__main__":
    setup("88.80.188.89", "root", "n04cce55")
    # sftp = pysftp.Connection("88.80.188.89", username="root", password="n04cce55")
    # sftp.put("openvpn-install.sh")
