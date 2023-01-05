import streamlit as st
from util.pages.opensea import opensea_page
from util.pages.x2y2 import x2y2_page
from util.pages.blur import blur_page
from util.pages.looksrare import looksrare_page
from util.pages.sudoswap import sudoswap_page
from util.pages.nftx import nftx_page
from util.pages.rarible import rarible_page
from util.pages.about import about_page

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        st.set_page_config(page_title="NFT Marketplace", layout="wide")

        st.sidebar.markdown("## NFT Marketplace on Ethereum")
        app = st.sidebar.selectbox(
            "Select Marketplace", self.apps, format_func=lambda app: app["title"]
        )
        app["function"]()

app = MultiApp()

app.add_app("Opensea", opensea_page)
app.add_app("X2Y2", x2y2_page)
app.add_app("Blur", blur_page)
app.add_app("Looksrare", looksrare_page)
app.add_app("Sudoswap", sudoswap_page)
app.add_app("NFTX", nftx_page)
app.add_app("Rarible", rarible_page)
app.add_app("About", about_page)

app.run()