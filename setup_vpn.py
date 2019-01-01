import pysftp
from linode import LinodeClient


def create_linode_vpn(token, region="us-west", ltype="g6-nanode-1", image="linode/ubuntu18.10"):
    client = LinodeClient(token)
    linode, password = client.linode.create_instance(ltype, region, image=image)
    print(password)
    print(linode.status)
    setup(linode.ipv4[0], "root", password, linode)


def setup(ip, username, password, node):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    connected = False
    while not connected:
        try:
            print(node.status)
            sftp = pysftp.Connection(ip, username=username, password=password, cnopts=cnopts)
            connected = True
        except Exception as e:
            print(e)

    sftp.put('install.sh')
    sftp.execute("bash install.sh")
    sftp.execute("mkdir profiles")
    sftp.execute("mv /root/yourkeyfile.ovpn /root/profiles/yourkeyfile.ovpn")
    sftp.get_d('/root/profiles', '/Users/Adam/Desktop')
    sftp.close()


if __name__ == "__main__":
    setup("88.80.188.89", "root", "n04cce55")
    # sftp = pysftp.Connection("88.80.188.89", username="root", password="n04cce55")
    # sftp.put("openvpn-install.sh")
