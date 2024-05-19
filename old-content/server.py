from fastapi import FastAPI, Body
from pydantic import BaseModel
from schemas.api_class import (stock,article,balancing)
from fastapi import FastAPI, Request, Form, status, Body, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from newsfeed.get_articles import (get_art, get_stock, get_art_sentiment)
from dynamic_portfolio_rebalancing.diverse_portfolio_generation import api_call as get_balancing

app = FastAPI()


@app.post("/get_stock")
async def stock_details(body: stock):
    output = await get_stock(body.symbol, body.interval, body.range)
    return output


@app.post("/get_article")
async def articles(body: article):
    output = await get_art(body.symbol)
    return output

@app.post("/get_sentiment")
async def articles(body: article):
    output = await get_art_sentiment(body.symbol)
    return output


@app.post("/balancing")
async def balancing(body: balancing):
    output = await get_balancing(total_investment_amount=body.amount)
    return output