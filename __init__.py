from flask import Flask, render_template, redirect, request
from linode_api4 import LinodeLoginClient, OAuthScopes
from keys import LINODE_API_KEY, LINODE_CLIENT_ID
from setup_vpn import create_vpn

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("homepage.html")


@app.route("/setup")
def setup():
    return render_template("setup.html")


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

    return render_template("confirm.html", provider="Linode", token=token)


"""
Create VPN with Digital Ocean API
"""


@app.route("/create-vpn", methods=['POST'])
def create_vpn_on_server():
    # use linode api to create a vpn
    token = request.form["token"]
    create_vpn("Linode", token)
    return render_template("success.html")


if __name__ == "__main__":
    app.run()
