import pysftp
from linode_api4 import LinodeClient
from constants import LINODE_REGIONS
import os


def create_vpn(provider, region, token):
    if provider == "Linode":
        create_linode_vpn(token, region=LINODE_REGIONS[region])


def create_linode_vpn(token, region="eu-west", ltype="g6-nanode-1", image="linode/ubuntu18.10"):
    client = LinodeClient(token)
    linode, password = client.linode.instance_create(ltype, region, image=image)
    print(password)
    print(linode.status)
    setup(linode.ipv4[0], "root", password, linode, token)


def setup(ip, username, password, node, token="token"):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    connected = False
    while not connected:
        try:
            # print(node.status)
            sftp = pysftp.Connection(ip, username=username, password=password, cnopts=cnopts)
            connected = True
        except Exception as e:
            print(e)

    sftp.put('install.sh')
    sftp.execute("bash install.sh")
    sftp.execute("mkdir profiles")
    sftp.execute("mv /root/yourkeyfile.ovpn /root/profiles/{}.ovpn".format(token))
    if not os.path.exists(os.getcwd() + '/configs'):
        os.makedirs(os.getcwd() + '/configs')

    sftp.get_d('/root/profiles', 'configs')
    sftp.execute('rm install.sh')
    sftp.close()


if __name__ == "__main__":
    setup("45.33.15.88", "root", "n04cce55", None)
    # sftp = pysftp.Connection("88.80.188.89", username="root", password="n04cce55")
    # sftp.put("openvpn-install.sh")
