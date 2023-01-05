import streamlit as st
import requests
import json
import util.constants.urls as urls

def about_page():
    api_data_last_updated_time = requests.get(url=urls.url_last_updated, headers={})
    json_last_updated_time = json.loads(api_data_last_updated_time.text)
    last_updated_time = json_last_updated_time[0]["DATE"]

    st.markdown("## About ")
    st.markdown("---")

    # need a photo
    # https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/wp-content/uploads/2022/05/best-nft-marketplaces.jpeg
    # https://miro.medium.com/max/626/0*MpnnuY9T9jQ6fnA-.jpg
    st.markdown("![ ](https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/wp-content/uploads/2022/05/best-nft-marketplaces.jpeg \"NFT Marketplace\")")

    st.markdown("#### About ")
    st.markdown("This dashboard is made with love by [@TheaChenyj](https://twitter.com/Thea_Chenyj), in a response "
                "to [MetricsDAO Analytics 📊 Bounty](https://metricsdao.notion.site/Bounty-Programs-d4bac7f1908f412f8bf4ed349198e5fe). "
                "This dashboard covers the most popular mainstream NFT marketplaces on Ethereum, including Opensea, X2Y2, Blur, Looksrare and so on. I hope you can get some practical insights from it.")

    st.markdown("#### Methodology")
    st.markdown("Data is from Flipside's dataset ez_nft_sales. I created some relevant querys and drew it by existing APIs.")
    st.write("Data Last Updated: "+ last_updated_time)