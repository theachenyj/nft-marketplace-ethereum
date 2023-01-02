import streamlit as st
import requests
import pandas as pd
import json
import altair as alt
import util.constants.urls as urls
from millify import millify

def x2y2_page():
    st.markdown("## X2Y2")
    st.markdown(
        "Launched on January 28, 2022, users can use X2Y2 to buy and sell NFTs, for bulk listing, batch purchasing, receiving real-time notifications "
        "and viewing rarities of NFTs. Developers can use X2Y2's Open APIs and Javascript SDK to build web3 applications "
        "like analytics tools and trading bots. "
        "X2Y2 does not offer private token sale and shares the market fees such that 100% of market fees collected are rewarded to X2Y2 stakers."
    )
    st.markdown("---")

    # Get Total calculation
    api_data_total = requests.get(url=urls.url_metric_total, headers={})
    json_data_total = json.loads(api_data_total.text)
    for item in json_data_total:
        if(item['PLATFORM_NAME'] == 'x2y2'):
            total_sales_count = millify(item['SALES_COUNT'])
            total_sales_volume = millify(item['SALES_VOLUME'])
            total_buyers = millify(item['BUYERS'])
            total_sellers = millify(item['SELLERS'])

    # Get 24 hours calculation
    api_data_current = requests.get(url=urls.url_metric_24h, headers={})
    json_data_current = json.loads(api_data_current.text)
    for item in json_data_current:
        if(item['PLATFORM_NAME'] == 'x2y2'):
            current_sales_count = millify(item['SALES_COUNT'])
            current_sales_volume = millify(item['SALES_VOLUME'])
            current_buyers = millify(item['BUYERS'])
            current_sellers = millify(item['SELLERS'])

    total_col1, total_col2, total_col3, total_col4 = st.columns(4)
    total_col1.metric(label="Total Sales Count", value=total_sales_count)
    total_col2.metric(label="Total Sales Volume in USD", value=total_sales_volume)
    total_col3.metric(label="Total Unique Buyers", value=total_buyers)
    total_col4.metric(label="Total Unique Sellers", value=total_sellers)

    crr_col1, crr_col2, crr_col3, crr_col4 = st.columns(4)
    crr_col1.metric(label="24H Sales Count", value=current_sales_count)
    crr_col2.metric(label="24H Sales Volume in USD", value=current_sales_volume)
    crr_col3.metric(label="24H Unique Buyers", value=current_buyers)
    crr_col4.metric(label="24H Unique Sellers", value=current_sellers)

    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Top 10 NFT Collections
        # Top 10 NFT Collections Based on  Count
    st.markdown(" ")

    api_data_top_collection = requests.get(url=urls.url_top_collections, headers={})
    json_top_collection = json.loads(api_data_top_collection.text)

    save_dict_top_collection_count = {"NFT Collection": [], "Sales Count": []}
    for item in json_top_collection:
        if (item["PLATFORM_NAME"] == 'x2y2' and item['COUNT_RANKINGS'] <= 10):
            save_dict_top_collection_count["NFT Collection"].append(item["NFT_COLLECTION"])
            save_dict_top_collection_count["Sales Count"].append(item["SALES_COUNT"])

    save_dict_top_collection_volume = {"NFT Collection": [], "Sales Volume": []}
    for item in json_top_collection:
        if (item['PLATFORM_NAME'] == 'x2y2' and item['VOLUME_RANKINGS'] <= 10):
            save_dict_top_collection_volume["NFT Collection"].append(item["NFT_COLLECTION"])
            save_dict_top_collection_volume["Sales Volume"].append(item["SALES_VOLUME"])

    top_collections_count, top_collections_volume = st.columns(2)

    with top_collections_count:
        df_collection_count = pd.DataFrame(data=save_dict_top_collection_count,
                                           columns=['NFT Collection', 'Sales Count'])
        chart_collection_count = alt.Chart(df_collection_count).mark_bar(color='#4E31C2').encode(
            x=alt.X('Sales Count:Q', axis=alt.Axis(title=None)),
            y=alt.Y('NFT Collection:N', sort='-x'),
            tooltip=[
                alt.Tooltip('NFT Collection:N'),
                alt.Tooltip('Sales Count:Q', format=',')
            ]
        ).properties(title='Top 10 NFT Collections Based on Sales Count')

        st.altair_chart(chart_collection_count, use_container_width=True)
        st.markdown(" ")

    with top_collections_volume:
        df_collection_volume = pd.DataFrame(data=save_dict_top_collection_volume,
                                            columns=['NFT Collection', 'Sales Volume'])
        chart_collection_volume = alt.Chart(df_collection_volume).mark_bar(color='#4E31C2').encode(
            x=alt.X('Sales Volume:Q', axis=alt.Axis(title=None)),
            y=alt.Y('NFT Collection:N', sort='-x'),
            tooltip=[
                alt.Tooltip('NFT Collection:N'),
                alt.Tooltip('Sales Volume:Q', format='$,.2f')
            ]
        ).properties(title='Top 10 NFT Collections Based on Sales Volume in USD Value')

        st.altair_chart(chart_collection_volume, use_container_width=True)
        st.markdown(" ")

    # Trading Activity Trends
    # The Percentage(%) Increase/Decrease of Sales Count
    # The Percentage(%) Increase/Decrease of Sales Volume
    st.markdown(" ")

    api_data_sales_change = requests.get(url=urls.url_sales_change, headers={})
    json_sales_change = json.loads(api_data_sales_change.text)

    save_dict_sales_change_count = {"Month": [], "Change": []}
    for item in json_sales_change:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_sales_change_count["Month"].append(item["BLOCK_MONTH"])
            save_dict_sales_change_count["Change"].append(item["SALES_COUNT_MOM"])
    df_sales_change_count = pd.DataFrame(data=save_dict_sales_change_count, columns=['Month', 'Change'])

    save_dict_sales_change_volume = {"Month": [], "Change": []}
    for item in json_sales_change:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_sales_change_volume["Month"].append(item["BLOCK_MONTH"])
            save_dict_sales_change_volume["Change"].append(item["SALES_VOLUME_MOM"])
    df_sales_change_volume = pd.DataFrame(data=save_dict_sales_change_volume, columns=['Month', 'Change'])

    change_sales_count, change_sales_volume = st.columns(2)
    with change_sales_count:
        change_sales_count_chart = alt.Chart(df_sales_change_count).mark_bar(size=20).encode(
            alt.X('Month:T', axis=alt.Axis(title=None)),
            alt.Y('Change:Q', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum.Change > 0,
                alt.value("green"),  # The positive color
                alt.value("red")  # The negative color
            ),
            tooltip=[
                alt.Tooltip('Month:T'),
                alt.Tooltip('Change:Q', format='.2%')
            ]
        ).properties(title='The Percentage(%) Increase/Decrease of Sales Count')
        st.altair_chart(change_sales_count_chart, use_container_width=True)
        st.markdown(" ")

    with change_sales_volume:
        change_sales_volume_chart = alt.Chart(df_sales_change_volume).mark_bar(size=20).encode(
            alt.X('Month:T', axis=alt.Axis(title=None)),
            alt.Y('Change:Q', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum.Change > 0,
                alt.value("green"),  # The positive color
                alt.value("red")  # The negative color
            ),
            tooltip=[
                alt.Tooltip('Month:T'),
                alt.Tooltip('Change:Q', format='.2%')
            ]
        ).properties(title='The Percentage(%) Increase/Decrease of Sales Volume')
        st.altair_chart(change_sales_volume_chart, use_container_width=True)
        st.markdown(" ")

    # Daily Sales Count v.s. Ether Price
    # Daily Sales Volume v.s. Ether Price
    st.markdown(" ")
    api_data_daily_trends = requests.get(url=urls.url_daily_trends, headers={})
    json_daily_trends = json.loads(api_data_daily_trends.text)

    save_dict_daily_sales_count = {"Date": [], "Sales Count": [], "Ether Price": []}
    for item in json_daily_trends:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_daily_sales_count["Date"].append(item["BLOCK_DATE"])
            save_dict_daily_sales_count["Sales Count"].append(item["SALES_COUNT"])
            save_dict_daily_sales_count["Ether Price"].append(item["AVG_PRICE"])
    df_daily_sales_count = pd.DataFrame(data=save_dict_daily_sales_count,
                                        columns=['Date', 'Sales Count', 'Ether Price'])

    save_dict_daily_sales_volume = {"Date": [], "Sales Volume": [], "Ether Price": []}
    for item in json_daily_trends:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_daily_sales_volume["Date"].append(item["BLOCK_DATE"])
            save_dict_daily_sales_volume["Sales Volume"].append(item["SALES_VOLUME"])
            save_dict_daily_sales_volume["Ether Price"].append(item["AVG_PRICE"])
    df_daily_sales_volume = pd.DataFrame(data=save_dict_daily_sales_volume,
                                         columns=['Date', 'Sales Volume', 'Ether Price'])

    daily_sales_count = st.container()
    with daily_sales_count:
        daily_sales_count_base = alt.Chart(df_daily_sales_count).encode(
            x=alt.X('Date:T', axis=alt.Axis(title=None)))
        daily_sales_count_area = daily_sales_count_base.mark_area(color='#4E31C2').encode(
            y='Sales Count:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Sales Count:Q', format=',')
            ]
        )
        daily_sales_count_line = daily_sales_count_base.mark_line(color='grey').encode(
            y='Ether Price:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Ether Price:Q', format='$,.2f')
            ]
        )
        daily_sales_count_layer = alt.layer(
            daily_sales_count_area,
            daily_sales_count_line
        ).resolve_scale(y='independent').properties(title='Daily Sales Count v.s. Ether Price')

        st.altair_chart(daily_sales_count_layer, use_container_width=True)
        st.markdown(" ")

    daily_sales_volume = st.container()
    with daily_sales_volume:
        daily_sales_volume_base = alt.Chart(df_daily_sales_volume).encode(
            x=alt.X('Date:T', axis=alt.Axis(title=None)))
        daily_sales_volume_area = daily_sales_volume_base.mark_area(color='#4E31C2').encode(
            y='Sales Volume:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Sales Volume:Q', format='$,.2f')
            ]
        )
        daily_sales_volume_line = daily_sales_volume_base.mark_line(color='grey').encode(
            y='Ether Price:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Ether Price:Q', format='$,.2f')
            ]
        )

        daily_sales_volume_layer = alt.layer(
            daily_sales_volume_area,
            daily_sales_volume_line
        ).resolve_scale(y='independent').properties(title='Daily Sales Volume v.s. Ether Price')
        st.altair_chart(daily_sales_volume_layer, use_container_width=True)
        st.markdown(" ")

    # Trader part

    st.markdown(" ")

    save_dict_buyers_change = {"Month": [], "Change": []}
    for item in json_sales_change:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_buyers_change["Month"].append(item["BLOCK_MONTH"])
            save_dict_buyers_change["Change"].append(item["BUYERS_MOM"])
    df_buyers_change = pd.DataFrame(data=save_dict_buyers_change, columns=['Month', 'Change'])

    save_dict_sellers_change = {"Month": [], "Change": []}
    for item in json_sales_change:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_sellers_change["Month"].append(item["BLOCK_MONTH"])
            save_dict_sellers_change["Change"].append(item["SELLERS_MOM"])
    df_sellers_change = pd.DataFrame(data=save_dict_sellers_change, columns=['Month', 'Change'])

    change_buyers, change_sellers = st.columns(2)

    # The Percentage(%) Increase/Decrease of Unique Buyers
    with change_buyers:
        change_buyers_chart = alt.Chart(df_buyers_change).mark_bar(size=20).encode(
            alt.X('Month:T', axis=alt.Axis(title=None)),
            alt.Y('Change:Q', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum.Change > 0,
                alt.value("green"),  # The positive color
                alt.value("red")  # The negative color
            ),
            tooltip=[
                alt.Tooltip('Month:T'),
                alt.Tooltip('Change:Q', format='.2%')
            ]
        ).properties(title='The Percentage(%) Increase/Decrease of Unique Buyers')
        st.altair_chart(change_buyers_chart, use_container_width=True)
        st.markdown(" ")

    # The Percentage(%) Increase/Decrease of Unique Sellers
    with change_sellers:
        change_sellers_chart = alt.Chart(df_sellers_change).mark_bar(size=20).encode(
            alt.X('Month:T', axis=alt.Axis(title=None)),
            alt.Y('Change:Q', axis=alt.Axis(format='%')),
            color=alt.condition(
                alt.datum.Change > 0,
                alt.value("green"),  # The positive color
                alt.value("red")  # The negative color
            ),
            tooltip=[
                alt.Tooltip('Month:T'),
                alt.Tooltip('Change:Q', format='.2%')
            ]
        ).properties(title='The Percentage(%) Increase/Decrease of Unique Sellers')
        st.altair_chart(change_sellers_chart, use_container_width=True)
        st.markdown(" ")

    # Daily Unique traders v.s. Ether Price
    save_dict_daily_traders = {"Date": [], "Traders": [], "Ether Price": []}
    for item in json_daily_trends:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_daily_traders["Date"].append(item["BLOCK_DATE"])
            save_dict_daily_traders["Traders"].append(item["TRADERS"])
            save_dict_daily_traders["Ether Price"].append(item["AVG_PRICE"])
    df_daily_traders = pd.DataFrame(data=save_dict_daily_traders, columns=['Date', 'Traders', 'Ether Price'])

    daily_traders = st.container()
    with daily_traders:
        daily_traders_base = alt.Chart(df_daily_traders).encode(x=alt.X('Date:T', axis=alt.Axis(title=None)))
        daily_traders_area = daily_traders_base.mark_area(color='#4E31C2').encode(
            y='Traders:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Traders:Q', format=',')
            ]
        )
        daily_traders_line = daily_traders_base.mark_line(color='grey').encode(
            y='Ether Price:Q',
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Ether Price:Q', format='$,.2f')
            ]
        )

        daily_traders_layer = alt.layer(
            daily_traders_area,
            daily_traders_line
        ).resolve_scale(y='independent').properties(title='Daily Traders v.s. Ether Price')

        st.altair_chart(daily_traders_layer, use_container_width=True)
        st.markdown(" ")

    # Buyer/Seller
    st.markdown(" ")
    api_data_daily_buyer_seller = requests.get(url=urls.url_daily_buyer_seller, headers={})
    json_daily_buyer_seller = json.loads(api_data_daily_buyer_seller.text)
    save_dict_daily_buyer_seller = {"Date": [], "Trader Type": [], "Traders": []}
    for item in json_daily_buyer_seller:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_daily_buyer_seller["Date"].append(item["BLOCK_DATE"])
            save_dict_daily_buyer_seller["Trader Type"].append(item["TRADER_TYPE"])
            save_dict_daily_buyer_seller["Traders"].append(item["WALLETS"])
    df_daily_buyer_seller = pd.DataFrame(data=save_dict_daily_buyer_seller,
                                         columns=['Date', 'Trader Type', 'Traders'])

    daily_buyer_seller = st.container()
    with daily_buyer_seller:
        daily_buyer_seller_color = {'Buyer': '#4E31C2', 'Seller': '#7FE0FE'}
        daily_buyer_seller_chart = alt.Chart(df_daily_buyer_seller).mark_area().encode(
            x=alt.X("Date:T", axis=alt.Axis(title=None)),
            y=alt.Y("Traders:Q"),
            # color="Trader Type:N",
            color=alt.Color('Trader Type', scale=alt.Scale(
                domain=['Buyer', 'Seller'],
                range=['#4E31C2', '#7FE0FE']
            )),
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Trader Type:N'),
                alt.Tooltip('Traders:Q', format=',')
            ]
        ).properties(title='Daily Buyer&Seller')

        st.altair_chart(daily_buyer_seller_chart, use_container_width=True)
        st.markdown(" ")

    # Buyer/Seller Ratio
    st.markdown(" ")
    api_data_daily_buyer_seller_ratio = requests.get(url=urls.url_daily_buyer_seller_ratio, headers={})
    json_daily_buyer_seller_ratio = json.loads(api_data_daily_buyer_seller_ratio.text)
    save_dict_daily_buyer_seller_ratio = {"Date": [], "Ratio": []}
    for item in json_daily_buyer_seller_ratio:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_daily_buyer_seller_ratio["Date"].append(item["BLOCK_DATE"])
            save_dict_daily_buyer_seller_ratio["Ratio"].append(item["BUYER_SELLER_RATIO"])
    df_daily_buyer_seller_ratio = pd.DataFrame(data=save_dict_daily_buyer_seller_ratio, columns=['Date', 'Ratio'])

    daily_buyer_seller_ratio = st.container()
    with daily_buyer_seller_ratio:
        daily_buyer_seller_ratio_chart = alt.Chart(df_daily_buyer_seller_ratio).mark_line(color='#4E31C2').encode(
            x=alt.X("Date:T", axis=alt.Axis(title=None)),
            y=alt.Y("Ratio:Q", axis=alt.Axis(format='%')),
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('Ratio:Q', format='.2%')
            ]
        ).properties(title='Daily Buyer/Seller Ratio')
        st.altair_chart(daily_buyer_seller_ratio_chart, use_container_width=True)
        st.markdown(" ")

    # Traders Grouping Based on Sales Count
    # User Grouping Baseed on Sales Volume
    st.markdown(" ")
    api_data_trader_group_sales_count = requests.get(url=urls.url_user_grouping_sales_count, headers={})
    json_trader_group_sales_count = json.loads(api_data_trader_group_sales_count.text)
    save_dict_trader_group_sales_count = {"Sales Count": [], "% of Total Traders": [], "Rankings": []}
    for item in json_trader_group_sales_count:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_trader_group_sales_count["Sales Count"].append(item["SALES_COUNT_TIER"])
            save_dict_trader_group_sales_count["% of Total Traders"].append(item["PCT"])
            save_dict_trader_group_sales_count["Rankings"].append(item["RANKINGS"])
    df_trader_group_sales_count = pd.DataFrame(data=save_dict_trader_group_sales_count,
                                               columns=['Sales Count', '% of Total Traders', 'Rankings'])

    api_data_trader_group_sales_volume = requests.get(url=urls.url_user_grouping_sales_volume, headers={})
    json_trader_group_sales_volume = json.loads(api_data_trader_group_sales_volume.text)
    save_dict_trader_group_sales_volume = {"Sales Volume": [], "% of Total Traders": [], "Rankings": []}
    for item in json_trader_group_sales_volume:
        if (item["PLATFORM_NAME"] == 'x2y2'):
            save_dict_trader_group_sales_volume["Sales Volume"].append(item["SALES_VOLUME_TIER"])
            save_dict_trader_group_sales_volume["% of Total Traders"].append(item["PCT"])
            save_dict_trader_group_sales_volume["Rankings"].append(item["RANKINGS"])
    df_trader_group_sales_volume = pd.DataFrame(data=save_dict_trader_group_sales_volume,
                                                columns=['Sales Volume', '% of Total Traders', 'Rankings'])

    trader_group_sales_count, trader_group_sales_volume = st.columns(2)
    with trader_group_sales_count:
        trader_group_sales_count_chart = alt.Chart(df_trader_group_sales_count).mark_bar(color='#4E31C2').encode(
            x=alt.X("Sales Count:N", sort=alt.SortField(field='Rankings', order='ascending'),
                    axis=alt.Axis(title=None)),
            y=alt.Y("% of Total Traders:Q", axis=alt.Axis(format='%')),
            tooltip=[
                alt.Tooltip('Sales Count:N'),
                alt.Tooltip('% of Total Traders:Q', format='.2%')
            ]
        ).properties(title='User Grouping Baseed on Sales Count')
        st.altair_chart(trader_group_sales_count_chart, use_container_width=True)
        st.markdown(" ")

    # Traders Grouping Based on Sales Volume
    with trader_group_sales_volume:
        trader_group_sales_volume_chart = alt.Chart(df_trader_group_sales_volume).mark_bar(color='#4E31C2').encode(
            x=alt.X("Sales Volume:N", sort=alt.SortField(field='Rankings', order='ascending'),
                    axis=alt.Axis(title=None)),
            y=alt.Y("% of Total Traders:Q", axis=alt.Axis(format='%')),
            tooltip=[
                alt.Tooltip('Sales Volume:N'),
                alt.Tooltip('% of Total Traders:Q', format='.2%')
            ]
        ).properties(title='User Grouping Baseed on Sales Volume')
        st.altair_chart(trader_group_sales_volume_chart, use_container_width=True)
        st.markdown(" ")

    # % of Ethereum NFT traders on Marketplaces
    st.markdown(" ")
    api_data_trader_share = requests.get(url=urls.url_trader_share, headers={})
    json_trader_share = json.loads(api_data_trader_share.text)
    save_dict_trader_share = {"Date": [], "% of Total Traders on Ethereum": []}
    for item in json_trader_share:
        if (item["BLOCK_DATE"] >= '2022-02-04'):
            save_dict_trader_share["Date"].append(item["BLOCK_DATE"])
            save_dict_trader_share["% of Total Traders on Ethereum"].append(item["X2Y2_SHARE"])
    df_trader_share = pd.DataFrame(data=save_dict_trader_share,
                                   columns=['Date', '% of Total Traders on Ethereum'])
    trader_share = st.container()
    with trader_share:
        trader_share_chart = alt.Chart(df_trader_share).mark_area(color='#4E31C2').encode(
            x=alt.X("Date:T", axis=alt.Axis(title=None)),
            y=alt.Y("% of Total Traders on Ethereum:Q", axis=alt.Axis(format='%')),
            tooltip=[
                alt.Tooltip('Date:T'),
                alt.Tooltip('% of Total Traders on Ethereum:Q', format='.2%')
            ]
        ).properties(title='% of Total NFT traders on Ethereum')
        st.altair_chart(trader_share_chart, use_container_width=True)
        st.markdown(" ")