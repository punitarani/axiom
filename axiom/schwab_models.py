"""
axiom/schwab_models.py

Generated from OpenAPI Spec
openapi 3.0.3
version 1.0.0
"""

# fmt: off

from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field, RootModel, conint, constr


class AssetType(Enum):
    BOND = 'BOND'
    EQUITY = 'EQUITY'
    ETF = 'ETF'
    EXTENDED = 'EXTENDED'
    FOREX = 'FOREX'
    FUTURE = 'FUTURE'
    FUTURE_OPTION = 'FUTURE_OPTION'
    FUNDAMENTAL = 'FUNDAMENTAL'
    INDEX = 'INDEX'
    INDICATOR = 'INDICATOR'
    MUTUAL_FUND = 'MUTUAL_FUND'
    OPTION = 'OPTION'
    UNKNOWN = 'UNKNOWN'


class Type(Enum):
    BOND = 'BOND'
    EQUITY = 'EQUITY'
    ETF = 'ETF'
    EXTENDED = 'EXTENDED'
    FOREX = 'FOREX'
    FUTURE = 'FUTURE'
    FUTURE_OPTION = 'FUTURE_OPTION'
    FUNDAMENTAL = 'FUNDAMENTAL'
    INDEX = 'INDEX'
    INDICATOR = 'INDICATOR'
    MUTUAL_FUND = 'MUTUAL_FUND'
    OPTION = 'OPTION'
    UNKNOWN = 'UNKNOWN'


class Bond(BaseModel):
    cusip: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    exchange: Optional[str] = None
    assetType: Optional[AssetType] = None
    bondFactor: Optional[str] = None
    bondMultiplier: Optional[str] = None
    bondPrice: Optional[float] = None
    type: Optional[Type] = None


class FundamentalInst(BaseModel):
    symbol: Optional[str] = None
    high52: Optional[float] = None
    low52: Optional[float] = None
    dividendAmount: Optional[float] = None
    dividendYield: Optional[float] = None
    dividendDate: Optional[str] = None
    peRatio: Optional[float] = None
    pegRatio: Optional[float] = None
    pbRatio: Optional[float] = None
    prRatio: Optional[float] = None
    pcfRatio: Optional[float] = None
    grossMarginTTM: Optional[float] = None
    grossMarginMRQ: Optional[float] = None
    netProfitMarginTTM: Optional[float] = None
    netProfitMarginMRQ: Optional[float] = None
    operatingMarginTTM: Optional[float] = None
    operatingMarginMRQ: Optional[float] = None
    returnOnEquity: Optional[float] = None
    returnOnAssets: Optional[float] = None
    returnOnInvestment: Optional[float] = None
    quickRatio: Optional[float] = None
    currentRatio: Optional[float] = None
    interestCoverage: Optional[float] = None
    totalDebtToCapital: Optional[float] = None
    ltDebtToEquity: Optional[float] = None
    totalDebtToEquity: Optional[float] = None
    epsTTM: Optional[float] = None
    epsChangePercentTTM: Optional[float] = None
    epsChangeYear: Optional[float] = None
    epsChange: Optional[float] = None
    revChangeYear: Optional[float] = None
    revChangeTTM: Optional[float] = None
    revChangeIn: Optional[float] = None
    sharesOutstanding: Optional[float] = None
    marketCapFloat: Optional[float] = None
    marketCap: Optional[float] = None
    bookValuePerShare: Optional[float] = None
    shortIntToFloat: Optional[float] = None
    shortIntDayToCover: Optional[float] = None
    divGrowthRate3Year: Optional[float] = None
    dividendPayAmount: Optional[float] = None
    dividendPayDate: Optional[str] = None
    beta: Optional[float] = None
    vol1DayAvg: Optional[float] = None
    vol10DayAvg: Optional[float] = None
    vol3MonthAvg: Optional[float] = None
    avg10DaysVolume: Optional[int] = None
    avg1DayVolume: Optional[int] = None
    avg3MonthVolume: Optional[int] = None
    declarationDate: Optional[str] = None
    dividendFreq: Optional[int] = None
    eps: Optional[float] = None
    corpactionDate: Optional[str] = None
    dtnVolume: Optional[int] = None
    nextDividendPayDate: Optional[str] = None
    nextDividendDate: Optional[str] = None
    fundLeverageFactor: Optional[float] = None
    fundStrategy: Optional[str] = None


class Instrument(BaseModel):
    cusip: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    exchange: Optional[str] = None
    assetType: Optional[AssetType] = None
    type: Optional[Type] = None


class InstrumentResponse(BaseModel):
    cusip: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    exchange: Optional[str] = None
    assetType: Optional[AssetType] = None
    bondFactor: Optional[str] = None
    bondMultiplier: Optional[str] = None
    bondPrice: Optional[float] = None
    fundamental: Optional[FundamentalInst] = None
    instrumentInfo: Optional[Instrument] = None
    bondInstrumentInfo: Optional[Bond] = None
    type: Optional[Type] = None


class MarketType(Enum):
    BOND = 'BOND'
    EQUITY = 'EQUITY'
    ETF = 'ETF'
    EXTENDED = 'EXTENDED'
    FOREX = 'FOREX'
    FUTURE = 'FUTURE'
    FUTURE_OPTION = 'FUTURE_OPTION'
    FUNDAMENTAL = 'FUNDAMENTAL'
    INDEX = 'INDEX'
    INDICATOR = 'INDICATOR'
    MUTUAL_FUND = 'MUTUAL_FUND'
    OPTION = 'OPTION'
    UNKNOWN = 'UNKNOWN'


class Interval(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None


class Direction(Enum):
    up = 'up'
    down = 'down'


class Screener(BaseModel):
    change: Optional[float] = Field(
        None, description='percent or value changed, by default its percent changed'
    )
    description: Optional[str] = Field(None, description='Name of security')
    direction: Optional[Direction] = None
    last: Optional[float] = Field(None, description='what was last quoted price')
    symbol: Optional[str] = Field(None, description='schwab security symbol')
    totalVolume: Optional[int] = None


class Candle(BaseModel):
    close: Optional[float] = None
    datetime: Optional[int] = None
    datetimeISO8601: Optional[str] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    volume: Optional[int] = None


class CandleList(BaseModel):
    candles: Optional[List[Candle]] = None
    empty: Optional[bool] = None
    previousClose: Optional[float] = None
    previousCloseDate: Optional[int] = None
    previousCloseDateISO8601: Optional[str] = None
    symbol: Optional[str] = None


class QuoteError(BaseModel):
    invalidCusips: Optional[List[str]] = Field(
        None, description='list of invalid cusips from request'
    )
    invalidSSIDs: Optional[List[int]] = Field(
        None, description='list of invalid SSIDs from request'
    )
    invalidSymbols: Optional[List[str]] = Field(
        None, description='list of invalid symbols from request'
    )


class ExtendedMarket(BaseModel):
    askPrice: Optional[float] = Field(
        None, description='Extended market ask price', examples=[124.85]
    )
    askSize: Optional[int] = Field(None, description='Extended market ask size', examples=[51771])
    bidPrice: Optional[float] = Field(
        None, description='Extended market bid price', examples=[124.85]
    )
    bidSize: Optional[int] = Field(None, description='Extended market bid size', examples=[51771])
    lastPrice: Optional[float] = Field(
        None, description='Extended market last price', examples=[124.85]
    )
    lastSize: Optional[int] = Field(None, description='Regular market last size', examples=[51771])
    mark: Optional[float] = Field(None, description='mark price', examples=[1.1246])
    quoteTime: Optional[int] = Field(
        None,
        description='Extended market quote time in milliseconds since Epoch',
        examples=[1621368000400],
    )
    totalVolume: Optional[float] = Field(None, description='Total volume', examples=[12345])
    tradeTime: Optional[int] = Field(
        None,
        description='Extended market trade time in milliseconds since Epoch',
        examples=[1621368000400],
    )


class QuoteEquity(BaseModel):
    field_52WeekHigh: Optional[float] = Field(
        None,
        alias='52WeekHigh',
        description='Higest price traded in the past 12 months, or 52 weeks',
        examples=[145.09],
    )
    field_52WeekLow: Optional[float] = Field(
        None,
        alias='52WeekLow',
        description='Lowest price traded in the past 12 months, or 52 weeks',
        examples=[77.581],
    )
    askMICId: Optional[str] = Field(None, description='ask MIC code', examples=['XNYS'])
    askPrice: Optional[float] = Field(None, description='Current Best Ask Price', examples=[124.63])
    askSize: Optional[int] = Field(None, description='Number of shares for ask', examples=[700])
    askTime: Optional[int] = Field(
        None, description='Last ask time in milliseconds since Epoch', examples=[1621376892336]
    )
    bidMICId: Optional[str] = Field(None, description='bid MIC code', examples=['XNYS'])
    bidPrice: Optional[float] = Field(None, description='Current Best Bid Price', examples=[124.6])
    bidSize: Optional[int] = Field(None, description='Number of shares for bid', examples=[300])
    bidTime: Optional[int] = Field(
        None, description='Last bid time in milliseconds since Epoch', examples=[1621376892336]
    )
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    highPrice: Optional[float] = Field(
        None, description="Day's high trade price", examples=[126.99]
    )
    lastMICId: Optional[str] = Field(None, description='Last MIC Code', examples=['XNYS'])
    lastPrice: Optional[float] = Field(None, examples=[122.3])
    lastSize: Optional[int] = Field(
        None, description='Number of shares traded with last trade', examples=[100]
    )
    lowPrice: Optional[float] = Field(None, description="Day's low trade price")
    mark: Optional[float] = Field(None, description='Mark price', examples=[52.93])
    markChange: Optional[float] = Field(None, description='Mark Price change', examples=[-0.01])
    markPercentChange: Optional[float] = Field(
        None, description='Mark Price percent change', examples=[-0.0189]
    )
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[52.8])
    quoteTime: Optional[int] = Field(
        None, description='Last quote time in milliseconds since Epoch', examples=[1621376892336]
    )
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )
    volatility: Optional[float] = Field(
        None, description='Option Risk/Volatility Measurement', examples=[0.0094]
    )


class QuoteForex(BaseModel):
    field_52WeekHigh: Optional[float] = Field(
        None,
        alias='52WeekHigh',
        description='Higest price traded in the past 12 months, or 52 weeks',
        examples=[145.09],
    )
    field_52WeekLow: Optional[float] = Field(
        None,
        alias='52WeekLow',
        description='Lowest price traded in the past 12 months, or 52 weeks',
        examples=[77.581],
    )
    askPrice: Optional[float] = Field(None, description='Current Best Ask Price', examples=[124.63])
    askSize: Optional[int] = Field(None, description='Number of shares for ask', examples=[700])
    bidPrice: Optional[float] = Field(None, description='Current Best Bid Price', examples=[124.6])
    bidSize: Optional[int] = Field(None, description='Number of shares for bid', examples=[300])
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    highPrice: Optional[float] = Field(
        None, description="Day's high trade price", examples=[126.99]
    )
    lastPrice: Optional[float] = Field(None, examples=[122.3])
    lastSize: Optional[int] = Field(
        None, description='Number of shares traded with last trade', examples=[100]
    )
    lowPrice: Optional[float] = Field(None, description="Day's low trade price", examples=[52.74])
    mark: Optional[float] = Field(None, description='Mark price', examples=[52.93])
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[52.8])
    quoteTime: Optional[int] = Field(
        None, description='Last quote time in milliseconds since Epoch', examples=[1621376892336]
    )
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    tick: Optional[float] = Field(None, description='Tick Price', examples=[0])
    tickAmount: Optional[float] = Field(None, description='Tick Amount', examples=[0])
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )


class QuoteFuture(BaseModel):
    askMICId: Optional[str] = Field(None, description='ask MIC code', examples=['XNYS'])
    askPrice: Optional[float] = Field(
        None, description='Current Best Ask Price', examples=[4083.25]
    )
    askSize: Optional[int] = Field(None, description='Number of shares for ask', examples=[36])
    askTime: Optional[int] = Field(
        None, description='Last ask time in milliseconds since Epoch', examples=[1621376892336]
    )
    bidMICId: Optional[str] = Field(None, description='bid MIC code', examples=['XNYS'])
    bidPrice: Optional[float] = Field(None, description='Current Best Bid Price', examples=[4083])
    bidSize: Optional[int] = Field(None, description='Number of shares for bid', examples=[18])
    bidTime: Optional[int] = Field(
        None, description='Last bid time in milliseconds since Epoch', examples=[1621376892336]
    )
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[4123]
    )
    futurePercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    highPrice: Optional[float] = Field(None, description="Day's high trade price", examples=[4123])
    lastMICId: Optional[str] = Field(None, description='Last MIC Code', examples=['XNYS'])
    lastPrice: Optional[float] = Field(None, examples=[4083])
    lastSize: Optional[int] = Field(
        None, description='Number of shares traded with last trade', examples=[7]
    )
    lowPrice: Optional[float] = Field(None, description="Day's low trade price", examples=[4075.5])
    mark: Optional[float] = Field(None, description='Mark price', examples=[4083])
    netChange: Optional[float] = Field(None, description='Current Last-Prev Close', examples=[-40])
    openInterest: Optional[int] = Field(None, description='Open interest', examples=[2517139])
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[4114])
    quoteTime: Optional[int] = Field(
        None, description='Last quote time in milliseconds since Epoch', examples=[1621427004585]
    )
    quotedInSession: Optional[bool] = Field(
        None, description='quoted during trading session', examples=[False]
    )
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    settleTime: Optional[int] = Field(
        None, description='settlement time in milliseconds since Epoch', examples=[1621376892336]
    )
    tick: Optional[float] = Field(None, description='Tick Price', examples=[0.25])
    tickAmount: Optional[float] = Field(None, description='Tick Amount', examples=[12.5])
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )


class QuoteFutureOption(BaseModel):
    askMICId: Optional[str] = Field(None, description='ask MIC code', examples=['XNYS'])
    askPrice: Optional[float] = Field(None, description='Current Best Ask Price', examples=[124.63])
    askSize: Optional[int] = Field(None, description='Number of shares for ask', examples=[700])
    bidMICId: Optional[str] = Field(None, description='bid MIC code', examples=['XNYS'])
    bidPrice: Optional[float] = Field(None, description='Current Best Bid Price', examples=[124.6])
    bidSize: Optional[int] = Field(None, description='Number of shares for bid', examples=[300])
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    highPrice: Optional[float] = Field(
        None, description="Day's high trade price", examples=[126.99]
    )
    lastMICId: Optional[str] = Field(None, description='Last MIC Code', examples=['XNYS'])
    lastPrice: Optional[float] = Field(None, examples=[122.3])
    lastSize: Optional[int] = Field(
        None, description='Number of shares traded with last trade', examples=[100]
    )
    lowPrice: Optional[float] = Field(None, description="Day's low trade price", examples=[52.74])
    mark: Optional[float] = Field(None, description='Mark price', examples=[52.93])
    markChange: Optional[float] = Field(None, description='Mark Price change', examples=[-0.04])
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    openInterest: Optional[int] = Field(None, description='Open Interest', examples=[317])
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[52.8])
    quoteTime: Optional[int] = Field(
        None, description='Last quote time in milliseconds since Epoch', examples=[1621376892336]
    )
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    settlemetPrice: Optional[float] = Field(
        None, description='Price at market open', examples=[52.8]
    )
    tick: Optional[float] = Field(None, description='Tick Price', examples=[0])
    tickAmount: Optional[float] = Field(None, description='Tick Amount', examples=[0])
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )


class QuoteIndex(BaseModel):
    field_52WeekHigh: Optional[float] = Field(
        None,
        alias='52WeekHigh',
        description='Higest price traded in the past 12 months, or 52 weeks',
        examples=[145.09],
    )
    field_52WeekLow: Optional[float] = Field(
        None,
        alias='52WeekLow',
        description='Lowest price traded in the past 12 months, or 52 weeks',
        examples=[77.581],
    )
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    highPrice: Optional[float] = Field(
        None, description="Day's high trade price", examples=[126.99]
    )
    lastPrice: Optional[float] = Field(None, examples=[122.3])
    lowPrice: Optional[float] = Field(None, description="Day's low trade price", examples=[52.74])
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[52.8])
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )


class QuoteMutualFund(BaseModel):
    field_52WeekHigh: Optional[float] = Field(
        None,
        alias='52WeekHigh',
        description='Higest price traded in the past 12 months, or 52 weeks',
        examples=[145.09],
    )
    field_52WeekLow: Optional[float] = Field(
        None,
        alias='52WeekLow',
        description='Lowest price traded in the past 12 months, or 52 weeks',
        examples=[77.581],
    )
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    nAV: Optional[float] = Field(None, description='Net Asset Value', examples=[126.99])
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )


class QuoteOption(BaseModel):
    field_52WeekHigh: Optional[float] = Field(
        None,
        alias='52WeekHigh',
        description='Higest price traded in the past 12 months, or 52 weeks',
        examples=[145.09],
    )
    field_52WeekLow: Optional[float] = Field(
        None,
        alias='52WeekLow',
        description='Lowest price traded in the past 12 months, or 52 weeks',
        examples=[77.581],
    )
    askPrice: Optional[float] = Field(None, description='Current Best Ask Price', examples=[124.63])
    askSize: Optional[int] = Field(None, description='Number of shares for ask', examples=[700])
    bidPrice: Optional[float] = Field(None, description='Current Best Bid Price', examples=[124.6])
    bidSize: Optional[int] = Field(None, description='Number of shares for bid', examples=[300])
    closePrice: Optional[float] = Field(
        None, description="Previous day's closing price", examples=[126.27]
    )
    delta: Optional[float] = Field(None, description='Delta Value', examples=[-0.0407])
    gamma: Optional[float] = Field(None, description='Gamma Value', examples=[0.0001])
    highPrice: Optional[float] = Field(
        None, description="Day's high trade price", examples=[126.99]
    )
    indAskPrice: Optional[float] = Field(
        None,
        description='Indicative Ask Price applicable only for Indicative Option Symbols',
        examples=[126.99],
    )
    indBidPrice: Optional[float] = Field(
        None,
        description='Indicative Bid Price applicable only for Indicative Option Symbols',
        examples=[126.99],
    )
    indQuoteTime: Optional[int] = Field(
        None,
        description='Indicative Quote Time in milliseconds since Epoch applicable only for Indicative Option Symbols',
        examples=[126.99],
    )
    impliedYield: Optional[float] = Field(None, description='Implied Yield', examples=[-0.0067])
    lastPrice: Optional[float] = Field(None, examples=[122.3])
    lastSize: Optional[int] = Field(
        None, description='Number of shares traded with last trade', examples=[100]
    )
    lowPrice: Optional[float] = Field(None, description="Day's low trade price", examples=[52.74])
    mark: Optional[float] = Field(None, description='Mark price', examples=[52.93])
    markChange: Optional[float] = Field(None, description='Mark Price change', examples=[-0.01])
    markPercentChange: Optional[float] = Field(
        None, description='Mark Price percent change', examples=[-0.0189]
    )
    moneyIntrinsicValue: Optional[float] = Field(
        None, description='Money Intrinsic Value', examples=[-947.96]
    )
    netChange: Optional[float] = Field(
        None, description='Current Last-Prev Close', examples=[-0.04]
    )
    netPercentChange: Optional[float] = Field(
        None, description='Net Percentage Change', examples=[-0.0756]
    )
    openInterest: Optional[float] = Field(None, description='Open Interest', examples=[317])
    openPrice: Optional[float] = Field(None, description='Price at market open', examples=[52.8])
    quoteTime: Optional[int] = Field(
        None, description='Last quote time in milliseconds since Epoch', examples=[1621376892336]
    )
    rho: Optional[float] = Field(None, description='Rho Value', examples=[-0.3732])
    securityStatus: Optional[str] = Field(
        None, description='Status of security', examples=['Normal']
    )
    theoreticalOptionValue: Optional[float] = Field(
        None, description='Theoretical option Value', examples=[12.275]
    )
    theta: Optional[float] = Field(None, description='Theta Value', examples=[-0.315])
    timeValue: Optional[float] = Field(None, description='Time Value', examples=[12.22])
    totalVolume: Optional[int] = Field(
        None,
        description='Aggregated shares traded throughout the day, including pre/post market hours.',
        examples=[20171188],
    )
    tradeTime: Optional[int] = Field(
        None, description='Last trade time in milliseconds since Epoch', examples=[1621376731304]
    )
    underlyingPrice: Optional[float] = Field(
        None, description='Underlying Price', examples=[3247.96]
    )
    vega: Optional[float] = Field(None, description='Vega Value', examples=[1.4455])
    volatility: Optional[float] = Field(
        None, description='Option Risk/Volatility Measurement', examples=[0.0094]
    )


class Realtime(Enum):
    boolean_True = True
    boolean_False = False


class Indicative(Enum):
    boolean_True = True
    boolean_False = False


class QuoteRequest(BaseModel):
    cusips: Optional[List[str]] = Field(
        None,
        description='List of cusip, max of 500 of symbols+cusip+ssids',
        examples=[[808524680, 594918104]],
    )
    fields: Optional[str] = Field(
        None,
        description='comma separated list of nodes in each quote<br/> possible values are quote,fundamental,reference,extended,regular. Dont send this attribute for full response.',
        examples=['quote,reference'],
    )
    ssids: Optional[List[conint(ge=1, le=9999999999)]] = Field(
        None,
        description='List of Schwab securityid[SSID], max of 500 of symbols+cusip+ssids',
        examples=[[1516105793, 34621523]],
    )
    symbols: Optional[List[str]] = Field(
        None,
        description='List of symbols, max of 500 of symbols+cusip+ssids',
        examples=[
            [
                'MRAD',
                'EATOF',
                'EBIZ',
                'AAPL',
                'BAC',
                'AAAHX',
                'AAAIX',
                '$DJI',
                '$SPX',
                'MVEN',
                'SOBS',
                'TOITF',
                'CNSWF',
                'AMZN  230317C01360000',
                'DJX   231215C00290000',
                '/ESH23',
                './ADUF23C0.55',
                'AUD/CAD',
            ]
        ],
    )
    realtime: Optional[Realtime] = Field(
        None, description='Get realtime quotes and skip entitlement check', examples=[True]
    )
    indicative: Optional[Indicative] = Field(
        None,
        description='Include indicative symbol quotes for all ETF symbols in request. If ETF symbol ABC is in request and indicative=true API will return quotes for ABC and its corresponding indicative quote for $ABC.IV',
        examples=[True],
    )


class ReferenceEquity(BaseModel):
    cusip: Optional[str] = Field(None, description='CUSIP of Instrument', examples=['A23456789'])
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['Apple Inc. - Common Stock']
    )
    exchange: Optional[str] = Field(None, description='Exchange Code', examples=['q'])
    exchangeName: Optional[str] = Field(None, description='Exchange Name')
    fsiDesc: Optional[constr(max_length=50)] = Field(None, description='FSI Desc')
    htbQuantity: Optional[int] = Field(None, description='Hard to borrow quantity.', examples=[100])
    htbRate: Optional[float] = Field(None, description='Hard to borrow rate.', examples=[4.5])
    isHardToBorrow: Optional[bool] = Field(
        None, description='is Hard to borrow security.', examples=[False]
    )
    isShortable: Optional[bool] = Field(
        None, description='is shortable security.', examples=[False]
    )
    otcMarketTier: Optional[constr(max_length=10)] = Field(None, description='OTC Market Tier')


class ReferenceForex(BaseModel):
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['Euro/USDollar Spot']
    )
    exchange: Optional[str] = Field(None, description='Exchange Code', examples=['q'])
    exchangeName: Optional[str] = Field(None, description='Exchange Name')
    isTradable: Optional[bool] = Field(None, description='is FOREX tradable', examples=[True])
    marketMaker: Optional[str] = Field(None, description='Market marker')
    product: Optional[str] = Field(None, description='Product name', examples=[None])
    tradingHours: Optional[str] = Field(None, description='Trading hours')


class ReferenceFuture(BaseModel):
    description: Optional[str] = Field(
        None,
        description='Description of Instrument',
        examples=['E-mini S&P 500 Index Futures,Jun-2021,ETH'],
    )
    exchange: Optional[str] = Field(None, description='Exchange Code', examples=['q'])
    exchangeName: Optional[str] = Field(None, description='Exchange Name')
    futureActiveSymbol: Optional[str] = Field(
        None, description='Active symbol', examples=['/ESM21']
    )
    futureExpirationDate: Optional[float] = Field(
        None,
        description='Future expiration date in milliseconds since epoch',
        examples=[1623988800000],
    )
    futureIsActive: Optional[bool] = Field(None, description='Future is active', examples=[True])
    futureMultiplier: Optional[float] = Field(None, description='Future multiplier', examples=[50])
    futurePriceFormat: Optional[str] = Field(None, description='Price format', examples=['D,D'])
    futureSettlementPrice: Optional[float] = Field(
        None, description='Future Settlement Price', examples=[4123]
    )
    futureTradingHours: Optional[str] = Field(
        None,
        description='Trading Hours',
        examples=['GLBX(de=1640;0=-1700151515301600;1=r-17001515r15301600d-15551640;7=d-16401555)'],
    )
    product: Optional[str] = Field(None, description='Futures product symbol', examples=['/ES'])


class ReferenceIndex(BaseModel):
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['DOW JONES 30 INDUSTRIALS']
    )
    exchange: Optional[str] = Field(None, description='Exchange Code', examples=['q'])
    exchangeName: Optional[str] = Field(None, description='Exchange Name')


class ReferenceMutualFund(BaseModel):
    cusip: Optional[str] = Field(None, description='CUSIP of Instrument', examples=['A23456789'])
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['Apple Inc. - Common Stock']
    )
    exchange: Optional[str] = Field('m', description='Exchange Code')
    exchangeName: Optional[str] = Field('MUTUAL_FUND', description='Exchange Name')


class RegularMarket(BaseModel):
    regularMarketLastPrice: Optional[float] = Field(
        None, description='Regular market last price', examples=[124.85]
    )
    regularMarketLastSize: Optional[int] = Field(
        None, description='Regular market last size', examples=[51771]
    )
    regularMarketNetChange: Optional[float] = Field(
        None, description='Regular market net change', examples=[-1.42]
    )
    regularMarketPercentChange: Optional[float] = Field(
        None, description='Regular market percent change', examples=[-1.1246]
    )
    regularMarketTradeTime: Optional[int] = Field(
        None,
        description='Regular market trade time in milliseconds since Epoch',
        examples=[1621368000400],
    )


class AssetMainType(Enum):
    BOND = 'BOND'
    EQUITY = 'EQUITY'
    FOREX = 'FOREX'
    FUTURE = 'FUTURE'
    FUTURE_OPTION = 'FUTURE_OPTION'
    INDEX = 'INDEX'
    MUTUAL_FUND = 'MUTUAL_FUND'
    OPTION = 'OPTION'


class EquityAssetSubType(Enum):
    COE = 'COE'
    PRF = 'PRF'
    ADR = 'ADR'
    GDR = 'GDR'
    CEF = 'CEF'
    ETF = 'ETF'
    ETN = 'ETN'
    UIT = 'UIT'
    WAR = 'WAR'
    RGT = 'RGT'


class MutualFundAssetSubType(Enum):
    OEF = 'OEF'
    CEF = 'CEF'
    MMF = 'MMF'


class ContractType(Enum):
    P = 'P'
    C = 'C'


class SettlementType(Enum):
    A = 'A'  # AM settlement
    P = 'P'  # PM settlement

    @classmethod
    def _missing_(cls, value):
        # Default to PM settlement if input is invalid
        return cls.P


class ExpirationType(Enum):
    M = 'M'
    Q = 'Q'
    S = 'S'
    W = 'W'


class FundStrategy(Enum):
    A = 'A'
    L = 'L'
    P = 'P'
    Q = 'Q'
    S = 'S'


class ExerciseType(Enum):
    A = 'A'
    E = 'E'


class DivFreq(Enum):
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3
    integer_4 = 4
    integer_6 = 6
    integer_11 = 11
    integer_12 = 12
    integer_None = None


class QuoteType(Enum):
    NBBO = 'NBBO'
    NFL = 'NFL'


class Status(Enum):
    field_400 = '400'
    field_401 = '401'
    field_404 = '404'
    field_500 = '500'


class ErrorSource(BaseModel):
    pointer: Optional[List[str]] = Field(
        None,
        description='list of attributes which lead to this error message.',
        examples=[
            ['/data/attributes/symbols', '/data/attributes/cusips', '/data/attributes/ssids']
        ],
    )
    parameter: Optional[str] = Field(
        None, description='parameter name which lead to this error message.', examples=['fields']
    )
    header: Optional[str] = Field(
        None,
        description='header name which lead to this error message.',
        examples=['Schwab-Client-CorrelId'],
    )


class Strategy(Enum):
    SINGLE = 'SINGLE'
    ANALYTICAL = 'ANALYTICAL'
    COVERED = 'COVERED'
    VERTICAL = 'VERTICAL'
    CALENDAR = 'CALENDAR'
    STRANGLE = 'STRANGLE'
    STRADDLE = 'STRADDLE'
    BUTTERFLY = 'BUTTERFLY'
    CONDOR = 'CONDOR'
    DIAGONAL = 'DIAGONAL'
    COLLAR = 'COLLAR'
    ROLL = 'ROLL'


class ExchangeName(Enum):
    IND = 'IND'
    ASE = 'ASE'
    NYS = 'NYS'
    NAS = 'NAS'
    NAP = 'NAP'
    PAC = 'PAC'
    OPR = 'OPR'
    BATS = 'BATS'
    NYSE = 'NYSE'
    NYSE_ARCA = 'NYSE Arca'
    NASDAQ = 'NASDAQ'


class Underlying(BaseModel):
    ask: Optional[float] = None
    askSize: Optional[int] = None
    bid: Optional[float] = None
    bidSize: Optional[int] = None
    change: Optional[float] = None
    close: Optional[float] = None
    delayed: Optional[bool] = None
    description: Optional[str] = None
    exchangeName: Optional[ExchangeName] = None
    fiftyTwoWeekHigh: Optional[float] = None
    fiftyTwoWeekLow: Optional[float] = None
    highPrice: Optional[float] = None
    last: Optional[float] = None
    lowPrice: Optional[float] = None
    mark: Optional[float] = None
    markChange: Optional[float] = None
    markPercentChange: Optional[float] = None
    openPrice: Optional[float] = None
    percentChange: Optional[float] = None
    quoteTime: Optional[int] = None
    symbol: Optional[str] = None
    totalVolume: Optional[int] = None
    tradeTime: Optional[int] = None


class OptionDeliverables(BaseModel):
    symbol: Optional[str] = None
    assetType: Optional[str] = None
    deliverableUnits: Optional[float] = None
    currencyType: Optional[str] = None


class PutCall(Enum):
    PUT = 'PUT'
    CALL = 'CALL'


class OptionContract(BaseModel):
    putCall: Optional[PutCall] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    exchangeName: Optional[str] = None
    bidPrice: Optional[float] = None
    askPrice: Optional[float] = None
    lastPrice: Optional[float] = None
    markPrice: Optional[float] = None
    bidSize: Optional[int] = None
    askSize: Optional[int] = None
    lastSize: Optional[int] = None
    highPrice: Optional[float] = None
    lowPrice: Optional[float] = None
    openPrice: Optional[float] = None
    closePrice: Optional[float] = None
    totalVolume: Optional[int] = None
    tradeDate: Optional[float] = None
    quoteTimeInLong: Optional[int] = None
    tradeTimeInLong: Optional[int] = None
    netChange: Optional[float] = None
    volatility: Optional[float] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    rho: Optional[float] = None
    timeValue: Optional[float] = None
    openInterest: Optional[float] = None
    isInTheMoney: Optional[bool] = None
    theoreticalOptionValue: Optional[float] = None
    theoreticalVolatility: Optional[float] = None
    isMini: Optional[bool] = None
    isNonStandard: Optional[bool] = None
    optionDeliverablesList: Optional[List[OptionDeliverables]] = None
    strikePrice: Optional[float] = None
    expirationDate: Optional[str] = None
    daysToExpiration: Optional[float] = None
    expirationType: Optional[ExpirationType] = None
    lastTradingDay: Optional[float] = None
    multiplier: Optional[float] = None
    settlementType: Optional[SettlementType] = None
    deliverableNote: Optional[str] = None
    isIndexOption: Optional[bool] = None
    percentChange: Optional[float] = None
    markChange: Optional[float] = None
    markPercentChange: Optional[float] = None
    isPennyPilot: Optional[bool] = None
    intrinsicValue: Optional[float] = None
    optionRoot: Optional[str] = None


class Expiration(BaseModel):
    daysToExpiration: Optional[int] = None
    expiration: Optional[str] = None
    expirationType: Optional[ExpirationType] = None
    standard: Optional[bool] = None
    settlementType: Optional[SettlementType] = None
    optionRoots: Optional[str] = None


class Hours(BaseModel):
    date: Optional[str] = None
    marketType: Optional[MarketType] = None
    exchange: Optional[str] = None
    category: Optional[str] = None
    product: Optional[str] = None
    productName: Optional[str] = None
    isOpen: Optional[bool] = None
    sessionHours: Optional[Dict[str, List[Interval]]] = None


class ForexResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quote: Optional[QuoteForex] = None
    reference: Optional[ReferenceForex] = None


class Fundamental(BaseModel):
    avg10DaysVolume: Optional[float] = Field(None, description='Average 10 day volume')
    avg1YearVolume: Optional[float] = Field(None, description='Average 1 day volume')
    declarationDate: Optional[AwareDatetime] = Field(
        None,
        description='Declaration date in yyyy-mm-ddThh:mm:ssZ',
        examples=['2021-04-28T00:00:00Z'],
    )
    divAmount: Optional[float] = Field(None, description='Dividend Amount', examples=[0.88])
    divExDate: Optional[str] = Field(
        None, description='Dividend date in yyyy-mm-ddThh:mm:ssZ', examples=['2021-05-07T00:00:00Z']
    )
    divFreq: Optional[DivFreq] = None
    divPayAmount: Optional[float] = Field(None, description='Dividend Pay Amount', examples=[0.22])
    divPayDate: Optional[AwareDatetime] = Field(
        None,
        description='Dividend pay date in yyyy-mm-ddThh:mm:ssZ',
        examples=['2021-05-13T00:00:00Z'],
    )
    divYield: Optional[float] = Field(None, description='Dividend yield', examples=[0.7])
    eps: Optional[float] = Field(None, description='Earnings per Share', examples=[4.45645])
    fundLeverageFactor: Optional[float] = Field(
        None, description='Fund Leverage Factor + > 0 <-', examples=[-1]
    )
    fundStrategy: Optional[FundStrategy] = None
    nextDivExDate: Optional[AwareDatetime] = Field(
        None, description='Next Dividend date', examples=['2021-02-12T00:00:00Z']
    )
    nextDivPayDate: Optional[AwareDatetime] = Field(
        None, description='Next Dividend pay date', examples=['2021-02-12T00:00:00Z']
    )
    peRatio: Optional[float] = Field(None, description='P/E Ratio', examples=[28.599])


class FutureResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quote: Optional[QuoteFuture] = None
    reference: Optional[ReferenceFuture] = None


class IndexResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quote: Optional[QuoteIndex] = None
    reference: Optional[ReferenceIndex] = None


class MutualFundResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    assetSubType: Optional[MutualFundAssetSubType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    fundamental: Optional[Fundamental] = None
    quote: Optional[QuoteMutualFund] = None
    reference: Optional[ReferenceMutualFund] = None


class ReferenceFutureOption(BaseModel):
    contractType: Optional[ContractType] = None
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['AMZN Aug 20 2021 2300 Put']
    )
    exchange: Optional[str] = Field(None, description='Exchange Code', examples=['q'])
    exchangeName: Optional[str] = Field(None, description='Exchange Name')
    multiplier: Optional[float] = Field(None, description='Option multiplier', examples=[100])
    expirationDate: Optional[int] = Field(None, description='date of expiration in long')
    expirationStyle: Optional[str] = Field(None, description='Style of expiration')
    strikePrice: Optional[float] = Field(None, description='Strike Price', examples=[2300])
    underlying: Optional[str] = Field(
        None, description='A company, index or fund name', examples=['AMZN Aug 20 2021 2300 Put']
    )


class ReferenceOption(BaseModel):
    contractType: Optional[ContractType] = None
    cusip: Optional[str] = Field(
        None, description='CUSIP of Instrument', examples=['0AMZN.TK12300000']
    )
    daysToExpiration: Optional[int] = Field(None, description='Days to Expiration', examples=[94])
    deliverables: Optional[str] = Field(
        None,
        description='Unit of trade',
        examples=['$6024.37 cash in lieu of shares, 212 shares of AZN'],
    )
    description: Optional[str] = Field(
        None, description='Description of Instrument', examples=['AMZN Aug 20 2021 2300 Put']
    )
    exchange: Optional[str] = Field('o', description='Exchange Code')
    exchangeName: Optional[str] = Field(None, description='Exchange Name')
    exerciseType: Optional[ExerciseType] = None
    expirationDay: Optional[conint(ge=1, le=31)] = Field(
        None, description='Expiration Day', examples=[20]
    )
    expirationMonth: Optional[conint(ge=1, le=12)] = Field(
        None, description='Expiration Month', examples=[8]
    )
    expirationType: Optional[ExpirationType] = None
    expirationYear: Optional[int] = Field(None, description='Expiration Year', examples=[2021])
    isPennyPilot: Optional[bool] = Field(
        None, description='Is this contract part of the Penny Pilot program', examples=[True]
    )
    lastTradingDay: Optional[int] = Field(
        None, description='milliseconds since epoch', examples=[1629504000000]
    )
    multiplier: Optional[float] = Field(None, description='Option multiplier', examples=[100])
    settlementType: Optional[SettlementType] = None
    strikePrice: Optional[float] = Field(None, description='Strike Price', examples=[2300])
    underlying: Optional[str] = Field(
        None, description='A company, index or fund name', examples=['AMZN Aug 20 2021 2300 Put']
    )


class Error(BaseModel):
    id: Optional[UUID] = Field(
        None, description='Unique error id.', examples=['9821320c-8500-4edf-bd46-a9299c13d2e0']
    )
    status: Optional[Status] = Field(None, description='The HTTP status code .', examples=['400'])
    title: Optional[str] = Field(
        None, description='Short error description.', examples=['Missing header']
    )
    detail: Optional[str] = Field(
        None,
        description='Detailed error description.',
        examples=['Search combination should not exceed 500.'],
    )
    source: Optional[ErrorSource] = None


class OptionContractMap(RootModel):
    root: Optional[Dict[str, List[OptionContract]]] = None

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class ExpirationChain(BaseModel):
    status: Optional[str] = None
    expirationList: Optional[List[Expiration]] = None


class EquityResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    assetSubType: Optional[EquityAssetSubType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quoteType: Optional[QuoteType] = None
    extended: Optional[ExtendedMarket] = None
    fundamental: Optional[Fundamental] = None
    quote: Optional[QuoteEquity] = None
    reference: Optional[ReferenceEquity] = None
    regular: Optional[RegularMarket] = None


class FutureOptionResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quote: Optional[QuoteFutureOption] = None
    reference: Optional[ReferenceFutureOption] = None


class OptionResponse(BaseModel):
    assetMainType: Optional[AssetMainType] = None
    ssid: Optional[int] = Field(None, description='SSID of instrument', examples=[1234567890])
    symbol: Optional[str] = Field(None, description='Symbol of instrument', examples=['AAPL'])
    realtime: Optional[bool] = Field(None, description='is quote realtime', examples=[True])
    quote: Optional[QuoteOption] = None
    reference: Optional[ReferenceOption] = None


class QuoteResponseObject(RootModel):
    root: Union[
        EquityResponse,
        OptionResponse,
        ForexResponse,
        FutureResponse,
        FutureOptionResponse,
        IndexResponse,
        MutualFundResponse,
        QuoteError,
    ]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class ErrorResponse(BaseModel):
    errors: Optional[List[Error]] = None


class OptionChain(BaseModel):
    symbol: Optional[str] = None
    status: Optional[str] = None
    underlying: Optional[Underlying] = None
    strategy: Optional[Strategy] = None
    interval: Optional[float] = None
    isDelayed: Optional[bool] = None
    isIndex: Optional[bool] = None
    daysToExpiration: Optional[float] = None
    interestRate: Optional[float] = None
    underlyingPrice: Optional[float] = None
    volatility: Optional[float] = None
    callExpDateMap: Optional[Dict[str, OptionContractMap]] = None
    putExpDateMap: Optional[Dict[str, OptionContractMap]] = None


class QuoteResponse(RootModel):
    root: Optional[Dict[str, QuoteResponseObject]] = None

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class PriceLevel(BaseModel):
    price: Optional[float] = None
    aggregate_size: Optional[int] = None
    market_maker_count: Optional[int] = None
    market_makers: Optional[List[dict]] = None


class BookContent(BaseModel):
    symbol: Optional[str] = None
    market_snapshot_time: Optional[int] = None
    bid_side_levels: Optional[List[PriceLevel]] = None
    ask_side_levels: Optional[List[PriceLevel]] = None


class ChartContent(BaseModel):
    key: Optional[str] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None
    sequence: Optional[int] = None
    chart_time: Optional[int] = None
    chart_day: Optional[int] = None


class ScreenerItem(BaseModel):
    description: Optional[str] = None
    last_price: Optional[float] = None
    market_share: Optional[float] = None
    net_change: Optional[float] = None
    net_percent_change: Optional[float] = None
    symbol: Optional[str] = None
    total_volume: Optional[int] = None
    trades: Optional[int] = None
    volume: Optional[int] = None


class ScreenerContent(BaseModel):
    symbol: Optional[str] = None
    timestamp: Optional[int] = None
    sort_field: Optional[str] = None
    frequency: Optional[int] = None
    items: Optional[List[ScreenerItem]] = None


class AccountActivityContent(BaseModel):
    seq: Optional[int] = None
    key: Optional[str] = None
    account: Optional[str] = None
    message_type: Optional[str] = None
    message_data: Optional[Union[dict, str]] = None


# Specific Models
class LevelOneEquityContent(BaseModel):
    ASK_ID: Optional[str] = None
    ASK_MIC_ID: Optional[str] = None
    ASK_PRICE: Optional[float] = None
    ASK_SIZE: Optional[int] = None
    ASK_TIME_MILLIS: Optional[int] = None
    BID_ID: Optional[str] = None
    BID_MIC_ID: Optional[str] = None
    BID_PRICE: Optional[float] = None
    BID_SIZE: Optional[int] = None
    BID_TIME_MILLIS: Optional[int] = None
    LAST_ID: Optional[str] = None
    LAST_MIC_ID: Optional[str] = None
    LAST_SIZE: Optional[int] = None
    MARK: Optional[float] = None
    MARK_CHANGE: Optional[float] = None
    MARK_CHANGE_PERCENT: Optional[float] = None
    QUOTE_TIME_MILLIS: Optional[int] = None
    REGULAR_MARKET_LAST_SIZE: Optional[int] = None
    REGULAR_MARKET_TRADE_MILLIS: Optional[int] = None
    TOTAL_VOLUME: Optional[int] = None
    TRADE_TIME_MILLIS: Optional[int] = None
    key: Optional[str] = None


class LevelOneEquity(BaseModel):
    command: Optional[str] = None
    content: Optional[List[LevelOneEquityContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class LevelOneOptionsContent(BaseModel):
    symbol: Optional[str] = None
    description: Optional[str] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    total_volume: Optional[int] = None
    open_interest: Optional[int] = None
    volatility: Optional[float] = None
    money_intrinsic_value: Optional[float] = None
    expiration_year: Optional[int] = None
    multiplier: Optional[float] = None
    digits: Optional[int] = None
    open_price: Optional[float] = None
    bid_size: Optional[int] = None
    ask_size: Optional[int] = None
    last_size: Optional[int] = None
    net_change: Optional[float] = None
    strike_price: Optional[float] = None
    contract_type: Optional[str] = None
    underlying: Optional[str] = None
    expiration_month: Optional[int] = None
    deliverables: Optional[str] = None
    time_value: Optional[float] = None
    expiration_day: Optional[int] = None
    days_to_expiration: Optional[int] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    rho: Optional[float] = None
    security_status: Optional[str] = None
    theoretical_option_value: Optional[float] = None
    underlying_price: Optional[float] = None
    uv_expiration_type: Optional[str] = None
    mark_price: Optional[float] = None
    quote_time_in_long: Optional[int] = None
    trade_time_in_long: Optional[int] = None
    exchange: Optional[str] = None
    exchange_name: Optional[str] = None
    last_trading_day: Optional[int] = None
    settlement_type: Optional[str] = None
    net_percent_change: Optional[float] = None
    mark_price_net_change: Optional[float] = None
    mark_price_percent_change: Optional[float] = None
    implied_yield: Optional[float] = None
    is_penny_pilot: Optional[bool] = None
    option_root: Optional[str] = None
    week_high: Optional[float] = None
    week_low: Optional[float] = None
    indicative_ask_price: Optional[float] = None
    indicative_bid_price: Optional[float] = None
    indicative_quote_time: Optional[int] = None
    exercise_type: Optional[str] = None


class LevelOneOptions(BaseModel):
    command: Optional[str] = None
    content: Optional[List[LevelOneOptionsContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class LevelOneFuturesContent(BaseModel):
    symbol: Optional[str] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    bid_size: Optional[int] = None
    ask_size: Optional[int] = None
    bid_id: Optional[str] = None
    ask_id: Optional[str] = None
    total_volume: Optional[int] = None
    last_size: Optional[int] = None
    quote_time: Optional[int] = None
    trade_time: Optional[int] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    exchange_id: Optional[str] = None
    description: Optional[str] = None
    last_id: Optional[str] = None
    open_price: Optional[float] = None
    net_change: Optional[float] = None
    future_percent_change: Optional[float] = None
    exchange_name: Optional[str] = None
    security_status: Optional[str] = None
    open_interest: Optional[int] = None
    mark: Optional[float] = None
    tick: Optional[float] = None
    tick_amount: Optional[float] = None
    product: Optional[str] = None
    future_price_format: Optional[str] = None
    future_trading_hours: Optional[str] = None
    future_is_tradable: Optional[bool] = None
    future_multiplier: Optional[float] = None
    future_is_active: Optional[bool] = None
    future_settlement_price: Optional[float] = None
    future_active_symbol: Optional[str] = None
    future_expiration_date: Optional[int] = None
    expiration_style: Optional[str] = None
    ask_time: Optional[int] = None
    bid_time: Optional[int] = None
    quoted_in_session: Optional[bool] = None
    settlement_date: Optional[int] = None


class LevelOneFutures(BaseModel):
    command: Optional[str] = None
    content: Optional[List[LevelOneFuturesContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class LevelOneFuturesOptionsContent(BaseModel):
    symbol: Optional[str] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    bid_size: Optional[int] = None
    ask_size: Optional[int] = None
    bid_id: Optional[str] = None
    ask_id: Optional[str] = None
    total_volume: Optional[int] = None
    last_size: Optional[int] = None
    quote_time: Optional[int] = None
    trade_time: Optional[int] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    exchange_id: Optional[str] = None
    description: Optional[str] = None
    last_id: Optional[str] = None
    open_price: Optional[float] = None
    open_interest: Optional[float] = None
    mark: Optional[float] = None
    tick: Optional[float] = None
    tick_amount: Optional[float] = None
    future_multiplier: Optional[float] = None
    future_settlement_price: Optional[float] = None
    underlying_symbol: Optional[str] = None
    strike_price: Optional[float] = None
    future_expiration_date: Optional[int] = None
    expiration_style: Optional[str] = None
    contract_type: Optional[str] = None
    security_status: Optional[str] = None
    exchange: Optional[str] = None
    exchange_name: Optional[str] = None
    last_trading_day: Optional[int] = None
    settlement_type: Optional[str] = None
    net_percent_change: Optional[float] = None
    mark_price_net_change: Optional[float] = None
    mark_price_percent_change: Optional[float] = None
    implied_yield: Optional[float] = None
    is_penny_pilot: Optional[bool] = None
    option_root: Optional[str] = None
    week_high: Optional[float] = None
    week_low: Optional[float] = None
    indicative_ask_price: Optional[float] = None
    indicative_bid_price: Optional[float] = None
    indicative_quote_time: Optional[int] = None
    exercise_type: Optional[str] = None


class LevelOneFuturesOptions(BaseModel):
    command: Optional[str] = None
    content: Optional[List[LevelOneFuturesOptionsContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class LevelOneForexContent(BaseModel):
    symbol: Optional[str] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    bid_size: Optional[int] = None
    ask_size: Optional[int] = None
    total_volume: Optional[int] = None
    last_size: Optional[int] = None
    quote_time: Optional[int] = None
    trade_time: Optional[int] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    exchange: Optional[str] = None
    description: Optional[str] = None
    open_price: Optional[float] = None
    net_change: Optional[float] = None
    percent_change: Optional[float] = None
    exchange_name: Optional[str] = None
    digits: Optional[int] = None
    security_status: Optional[str] = None
    tick: Optional[float] = None
    tick_amount: Optional[float] = None
    product: Optional[str] = None
    trading_hours: Optional[str] = None
    is_tradable: Optional[bool] = None
    market_maker: Optional[str] = None
    week_high: Optional[float] = None
    week_low: Optional[float] = None
    mark: Optional[float] = None


class LevelOneForex(BaseModel):
    command: Optional[str] = None
    content: Optional[List[LevelOneForexContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class NYSEBook(BaseModel):
    command: Optional[str] = None
    content: Optional[List[BookContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class NASDAQBook(BaseModel):
    command: Optional[str] = None
    content: Optional[List[BookContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class OptionsBook(BaseModel):
    command: Optional[str] = None
    content: Optional[List[BookContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class ChartEquity(BaseModel):
    command: Optional[str] = None
    content: Optional[List[ChartContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class ChartFutures(BaseModel):
    command: Optional[str] = None
    content: Optional[List[ChartContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class ScreenerEquity(BaseModel):
    command: Optional[str] = None
    content: Optional[List[ScreenerContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class ScreenerOption(BaseModel):
    command: Optional[str] = None
    content: Optional[List[ScreenerContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None


class AccountActivity(BaseModel):
    command: Optional[str] = None
    content: Optional[List[AccountActivityContent]] = None
    service: Optional[str] = None
    timestamp: Optional[int] = None
