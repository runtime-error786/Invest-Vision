import yfinance as yf
from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from phi.model.groq import Groq
import streamlit as st
from utils import load_config


def fetch_stock_data(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = {
            "stock_price": stock.history(period="1d")["Close"].iloc[0],
            "analyst_recommendations": stock.recommendations.tail(5), 
            "stock_fundamentals": stock.info
        }
        return data
    except Exception as e:
        return {"error": str(e)}

def get_stock_summary(stock_data, stock_symbol):  
    agent = Agent(
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
        show_tool_calls=True,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=["Format your response using markdown and use tables to display data where possible."]
    )
    
    stock_price = stock_data["stock_price"]
    analyst_recommendations = stock_data["analyst_recommendations"]
    stock_fundamentals = stock_data["stock_fundamentals"]

    query = f"Share the {stock_symbol} stock price, analyst recommendations, and fundamentals"
    
    summary = agent.run(f"Stock Price: {stock_price}\nAnalyst Recommendations: {analyst_recommendations}\nFundamentals: {stock_fundamentals}")
    
    formatted_summary = f"""
    ## Stock Summary for {stock_symbol}

    ### Stock Price
    - Current Price: **${stock_price}**
    
    ### Analyst Recommendations
    - **Strong Buy**: {analyst_recommendations['strongBuy'].sum()}
    - **Buy**: {analyst_recommendations['buy'].sum()}
    - **Hold**: {analyst_recommendations['hold'].sum()}
    - **Sell**: {analyst_recommendations['sell'].sum()}
    - **Strong Sell**: {analyst_recommendations['strongSell'].sum()}

    ### Fundamentals
    - **Market Cap**: {stock_fundamentals['marketCap']}
    - **PE Ratio**: {stock_fundamentals['trailingPE']}
    - **Beta**: {stock_fundamentals['beta']}
    - **Revenue**: ${stock_fundamentals['totalRevenue']}
    - **Net Income**: ${stock_fundamentals['netIncomeToCommon']}

    ### CEO Information
    - **Name**: {stock_fundamentals['companyOfficers'][0]['name']}
    - **Age**: {stock_fundamentals['companyOfficers'][0]['age']}
    - **Title**: {stock_fundamentals['companyOfficers'][0]['title']}
    """
    return formatted_summary