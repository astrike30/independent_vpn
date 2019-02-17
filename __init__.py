from flask import Flask, render_template, redirect, request, send_from_directory
from linode_api4 import LinodeLoginClient, OAuthScopes
from keys import LINODE_API_KEY, LINODE_CLIENT_ID
from setup_vpn import create_vpn
from constants import LINODE_REGIONS

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("homepage.html")


@app.route("/setup")
def setup():
    return render_template("setup.html")


@app.route("/FAQ")
def help():
    return render_template("help.html")


"""
Create VPN with Linode API
"""


@app.route("/linode-oauth-begin")
def linode_oauth():
    login_client = LinodeLoginClient(LINODE_CLIENT_ID, LINODE_API_KEY)

    redirect_to = login_client.generate_login_url(scopes=[OAuthScopes.Linodes.create, OAuthScopes.Linodes.modify, OAuthScopes.Linodes.view])

    return redirect(redirect_to)


@app.route("/linode_oauth_redirect", methods=['GET'])
def linode_oauth_redirect():
    login_client = LinodeLoginClient(LINODE_CLIENT_ID, LINODE_API_KEY)

    code = request.args["code"]
    token = login_client.finish_oauth(code)[0]

    print(token)

    regions = [key for key, value in LINODE_REGIONS.items()]

    return render_template("confirm.html", provider="Linode", token=token, regions=regions)


"""
Create VPN with Digital Ocean API
"""
"""
"""


@app.route("/create-vpn", methods=['POST'])
def create_vpn_on_server():
    # use linode api to create a vpn
    token = request.form["token"]
    region = request.form["region"]
    create_vpn("Linode", region, token)
    return render_template("success.html", token=token)


"""
Download VPN file
"""


@app.route('/download', methods=['POST'])
def download():
    token = request.form["file"]
    login_client = LinodeLoginClient(LINODE_CLIENT_ID, LINODE_API_KEY)
    login_client.expire_token(token)
    return send_from_directory(directory="configs", filename=token + ".ovpn", attachment_filename="yourkeyfile.ovpn", as_attachment=True)


"""
"""

if __name__ == "__main__":
    app.run()
