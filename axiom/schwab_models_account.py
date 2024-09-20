"""
axiom/schwab_models_accounts.py

Generated from OpenAPI Spec
openapi 3.0.1
version 1.0.0
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import AwareDatetime, BaseModel, Field, RootModel
from typing_extensions import Literal

# fmt: off

class AccountNumberHash(BaseModel):
    accountNumber: Optional[str] = None
    hashValue: Optional[str] = None


class Session(Enum):
    NORMAL = 'NORMAL'
    AM = 'AM'
    PM = 'PM'
    SEAMLESS = 'SEAMLESS'


class Duration(Enum):
    DAY = 'DAY'
    GOOD_TILL_CANCEL = 'GOOD_TILL_CANCEL'
    FILL_OR_KILL = 'FILL_OR_KILL'
    IMMEDIATE_OR_CANCEL = 'IMMEDIATE_OR_CANCEL'
    END_OF_WEEK = 'END_OF_WEEK'
    END_OF_MONTH = 'END_OF_MONTH'
    NEXT_END_OF_MONTH = 'NEXT_END_OF_MONTH'
    UNKNOWN = 'UNKNOWN'


class OrderType(Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    TRAILING_STOP = 'TRAILING_STOP'
    CABINET = 'CABINET'
    NON_MARKETABLE = 'NON_MARKETABLE'
    MARKET_ON_CLOSE = 'MARKET_ON_CLOSE'
    EXERCISE = 'EXERCISE'
    TRAILING_STOP_LIMIT = 'TRAILING_STOP_LIMIT'
    NET_DEBIT = 'NET_DEBIT'
    NET_CREDIT = 'NET_CREDIT'
    NET_ZERO = 'NET_ZERO'
    LIMIT_ON_CLOSE = 'LIMIT_ON_CLOSE'
    UNKNOWN = 'UNKNOWN'


class OrderTypeRequest(Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    TRAILING_STOP = 'TRAILING_STOP'
    CABINET = 'CABINET'
    NON_MARKETABLE = 'NON_MARKETABLE'
    MARKET_ON_CLOSE = 'MARKET_ON_CLOSE'
    EXERCISE = 'EXERCISE'
    TRAILING_STOP_LIMIT = 'TRAILING_STOP_LIMIT'
    NET_DEBIT = 'NET_DEBIT'
    NET_CREDIT = 'NET_CREDIT'
    NET_ZERO = 'NET_ZERO'
    LIMIT_ON_CLOSE = 'LIMIT_ON_CLOSE'


class ComplexOrderStrategyType(Enum):
    NONE = 'NONE'
    COVERED = 'COVERED'
    VERTICAL = 'VERTICAL'
    BACK_RATIO = 'BACK_RATIO'
    CALENDAR = 'CALENDAR'
    DIAGONAL = 'DIAGONAL'
    STRADDLE = 'STRADDLE'
    STRANGLE = 'STRANGLE'
    COLLAR_SYNTHETIC = 'COLLAR_SYNTHETIC'
    BUTTERFLY = 'BUTTERFLY'
    CONDOR = 'CONDOR'
    IRON_CONDOR = 'IRON_CONDOR'
    VERTICAL_ROLL = 'VERTICAL_ROLL'
    COLLAR_WITH_STOCK = 'COLLAR_WITH_STOCK'
    DOUBLE_DIAGONAL = 'DOUBLE_DIAGONAL'
    UNBALANCED_BUTTERFLY = 'UNBALANCED_BUTTERFLY'
    UNBALANCED_CONDOR = 'UNBALANCED_CONDOR'
    UNBALANCED_IRON_CONDOR = 'UNBALANCED_IRON_CONDOR'
    UNBALANCED_VERTICAL_ROLL = 'UNBALANCED_VERTICAL_ROLL'
    MUTUAL_FUND_SWAP = 'MUTUAL_FUND_SWAP'
    CUSTOM = 'CUSTOM'


class RequestedDestination(Enum):
    INET = 'INET'
    ECN_ARCA = 'ECN_ARCA'
    CBOE = 'CBOE'
    AMEX = 'AMEX'
    PHLX = 'PHLX'
    ISE = 'ISE'
    BOX = 'BOX'
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    BATS = 'BATS'
    C2 = 'C2'
    AUTO = 'AUTO'


class StopPriceLinkBasis(Enum):
    MANUAL = 'MANUAL'
    BASE = 'BASE'
    TRIGGER = 'TRIGGER'
    LAST = 'LAST'
    BID = 'BID'
    ASK = 'ASK'
    ASK_BID = 'ASK_BID'
    MARK = 'MARK'
    AVERAGE = 'AVERAGE'


class StopPriceLinkType(Enum):
    VALUE = 'VALUE'
    PERCENT = 'PERCENT'
    TICK = 'TICK'


class StopPriceOffset(RootModel[float]):
    root: float


class StopType(Enum):
    STANDARD = 'STANDARD'
    BID = 'BID'
    ASK = 'ASK'
    LAST = 'LAST'
    MARK = 'MARK'


class PriceLinkBasis(Enum):
    MANUAL = 'MANUAL'
    BASE = 'BASE'
    TRIGGER = 'TRIGGER'
    LAST = 'LAST'
    BID = 'BID'
    ASK = 'ASK'
    ASK_BID = 'ASK_BID'
    MARK = 'MARK'
    AVERAGE = 'AVERAGE'


class PriceLinkType(Enum):
    VALUE = 'VALUE'
    PERCENT = 'PERCENT'
    TICK = 'TICK'


class TaxLotMethod(Enum):
    FIFO = 'FIFO'
    LIFO = 'LIFO'
    HIGH_COST = 'HIGH_COST'
    LOW_COST = 'LOW_COST'
    AVERAGE_COST = 'AVERAGE_COST'
    SPECIFIC_LOT = 'SPECIFIC_LOT'
    LOSS_HARVESTER = 'LOSS_HARVESTER'


class SpecialInstruction(Enum):
    ALL_OR_NONE = 'ALL_OR_NONE'
    DO_NOT_REDUCE = 'DO_NOT_REDUCE'
    ALL_OR_NONE_DO_NOT_REDUCE = 'ALL_OR_NONE_DO_NOT_REDUCE'


class OrderStrategyType(Enum):
    SINGLE = 'SINGLE'
    CANCEL = 'CANCEL'
    RECALL = 'RECALL'
    PAIR = 'PAIR'
    FLATTEN = 'FLATTEN'
    TWO_DAY_SWAP = 'TWO_DAY_SWAP'
    BLAST_ALL = 'BLAST_ALL'
    OCO = 'OCO'
    TRIGGER = 'TRIGGER'


class Status(Enum):
    AWAITING_PARENT_ORDER = 'AWAITING_PARENT_ORDER'
    AWAITING_CONDITION = 'AWAITING_CONDITION'
    AWAITING_STOP_CONDITION = 'AWAITING_STOP_CONDITION'
    AWAITING_MANUAL_REVIEW = 'AWAITING_MANUAL_REVIEW'
    ACCEPTED = 'ACCEPTED'
    AWAITING_UR_OUT = 'AWAITING_UR_OUT'
    PENDING_ACTIVATION = 'PENDING_ACTIVATION'
    QUEUED = 'QUEUED'
    WORKING = 'WORKING'
    REJECTED = 'REJECTED'
    PENDING_CANCEL = 'PENDING_CANCEL'
    CANCELED = 'CANCELED'
    PENDING_REPLACE = 'PENDING_REPLACE'
    REPLACED = 'REPLACED'
    FILLED = 'FILLED'
    EXPIRED = 'EXPIRED'
    NEW = 'NEW'
    AWAITING_RELEASE_TIME = 'AWAITING_RELEASE_TIME'
    PENDING_ACKNOWLEDGEMENT = 'PENDING_ACKNOWLEDGEMENT'
    PENDING_RECALL = 'PENDING_RECALL'
    UNKNOWN = 'UNKNOWN'


class AmountIndicator(Enum):
    DOLLARS = 'DOLLARS'
    SHARES = 'SHARES'
    ALL_SHARES = 'ALL_SHARES'
    PERCENTAGE = 'PERCENTAGE'
    UNKNOWN = 'UNKNOWN'


class SettlementInstruction(Enum):
    REGULAR = 'REGULAR'
    CASH = 'CASH'
    NEXT_DAY = 'NEXT_DAY'
    UNKNOWN = 'UNKNOWN'


class AdvancedOrderType(Enum):
    NONE = 'NONE'
    OTO = 'OTO'
    OCO = 'OCO'
    OTOCO = 'OTOCO'
    OT2OCO = 'OT2OCO'
    OT3OCO = 'OT3OCO'
    BLAST_ALL = 'BLAST_ALL'
    OTA = 'OTA'
    PAIR = 'PAIR'


class OrderBalance(BaseModel):
    orderValue: Optional[float] = None
    projectedAvailableFund: Optional[float] = None
    projectedBuyingPower: Optional[float] = None
    projectedCommission: Optional[float] = None


class APIRuleAction(Enum):
    ACCEPT = 'ACCEPT'
    ALERT = 'ALERT'
    REJECT = 'REJECT'
    REVIEW = 'REVIEW'
    UNKNOWN = 'UNKNOWN'


class FeeType(Enum):
    COMMISSION = 'COMMISSION'
    SEC_FEE = 'SEC_FEE'
    STR_FEE = 'STR_FEE'
    R_FEE = 'R_FEE'
    CDSC_FEE = 'CDSC_FEE'
    OPT_REG_FEE = 'OPT_REG_FEE'
    ADDITIONAL_FEE = 'ADDITIONAL_FEE'
    MISCELLANEOUS_FEE = 'MISCELLANEOUS_FEE'
    FTT = 'FTT'
    FUTURES_CLEARING_FEE = 'FUTURES_CLEARING_FEE'
    FUTURES_DESK_OFFICE_FEE = 'FUTURES_DESK_OFFICE_FEE'
    FUTURES_EXCHANGE_FEE = 'FUTURES_EXCHANGE_FEE'
    FUTURES_GLOBEX_FEE = 'FUTURES_GLOBEX_FEE'
    FUTURES_NFA_FEE = 'FUTURES_NFA_FEE'
    FUTURES_PIT_BROKERAGE_FEE = 'FUTURES_PIT_BROKERAGE_FEE'
    FUTURES_TRANSACTION_FEE = 'FUTURES_TRANSACTION_FEE'
    LOW_PROCEEDS_COMMISSION = 'LOW_PROCEEDS_COMMISSION'
    BASE_CHARGE = 'BASE_CHARGE'
    GENERAL_CHARGE = 'GENERAL_CHARGE'
    GST_FEE = 'GST_FEE'
    TAF_FEE = 'TAF_FEE'
    INDEX_OPTION_FEE = 'INDEX_OPTION_FEE'
    TEFRA_TAX = 'TEFRA_TAX'
    STATE_TAX = 'STATE_TAX'
    UNKNOWN = 'UNKNOWN'


class DateParam(BaseModel):
    date: Optional[str] = Field(
        None, description="Valid ISO-8601 format is :<br> <code>yyyy-MM-dd'T'HH:mm:ss.SSSZ</code>"
    )


class ActivityType(Enum):
    EXECUTION = 'EXECUTION'
    ORDER_ACTION = 'ORDER_ACTION'


class ExecutionType(Enum):
    FILL = 'FILL'


class ExecutionLeg(BaseModel):
    legId: Optional[int] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    mismarkedQuantity: Optional[float] = None
    instrumentId: Optional[int] = None
    time: Optional[AwareDatetime] = None


class ServiceError(BaseModel):
    message: Optional[str] = None
    errors: Optional[List[str]] = None


class OrderLegType(Enum):
    EQUITY = 'EQUITY'
    OPTION = 'OPTION'
    INDEX = 'INDEX'
    MUTUAL_FUND = 'MUTUAL_FUND'
    CASH_EQUIVALENT = 'CASH_EQUIVALENT'
    FIXED_INCOME = 'FIXED_INCOME'
    CURRENCY = 'CURRENCY'
    COLLECTIVE_INVESTMENT = 'COLLECTIVE_INVESTMENT'


class PositionEffect(Enum):
    OPENING = 'OPENING'
    CLOSING = 'CLOSING'
    AUTOMATIC = 'AUTOMATIC'


class QuantityType(Enum):
    ALL_SHARES = 'ALL_SHARES'
    DOLLARS = 'DOLLARS'
    SHARES = 'SHARES'


class DivCapGains(Enum):
    REINVEST = 'REINVEST'
    PAYOUT = 'PAYOUT'


class Type(Enum):
    CASH = 'CASH'
    MARGIN = 'MARGIN'


class MarginInitialBalance(BaseModel):
    accruedInterest: Optional[float] = None
    availableFundsNonMarginableTrade: Optional[float] = None
    bondValue: Optional[float] = None
    buyingPower: Optional[float] = None
    cashBalance: Optional[float] = None
    cashAvailableForTrading: Optional[float] = None
    cashReceipts: Optional[float] = None
    dayTradingBuyingPower: Optional[float] = None
    dayTradingBuyingPowerCall: Optional[float] = None
    dayTradingEquityCall: Optional[float] = None
    equity: Optional[float] = None
    equityPercentage: Optional[float] = None
    liquidationValue: Optional[float] = None
    longMarginValue: Optional[float] = None
    longOptionMarketValue: Optional[float] = None
    longStockValue: Optional[float] = None
    maintenanceCall: Optional[float] = None
    maintenanceRequirement: Optional[float] = None
    margin: Optional[float] = None
    marginEquity: Optional[float] = None
    moneyMarketFund: Optional[float] = None
    mutualFundValue: Optional[float] = None
    regTCall: Optional[float] = None
    shortMarginValue: Optional[float] = None
    shortOptionMarketValue: Optional[float] = None
    shortStockValue: Optional[float] = None
    totalCash: Optional[float] = None
    isInCall: Optional[float] = None
    unsettledCash: Optional[float] = None
    pendingDeposits: Optional[float] = None
    marginBalance: Optional[float] = None
    shortBalance: Optional[float] = None
    accountValue: Optional[float] = None


class MarginBalance(BaseModel):
    availableFunds: Optional[float] = None
    availableFundsNonMarginableTrade: Optional[float] = None
    buyingPower: Optional[float] = None
    buyingPowerNonMarginableTrade: Optional[float] = None
    dayTradingBuyingPower: Optional[float] = None
    dayTradingBuyingPowerCall: Optional[float] = None
    equity: Optional[float] = None
    equityPercentage: Optional[float] = None
    longMarginValue: Optional[float] = None
    maintenanceCall: Optional[float] = None
    maintenanceRequirement: Optional[float] = None
    marginBalance: Optional[float] = None
    regTCall: Optional[float] = None
    shortBalance: Optional[float] = None
    shortMarginValue: Optional[float] = None
    sma: Optional[float] = None
    isInCall: Optional[float] = None
    stockBuyingPower: Optional[float] = None
    optionBuyingPower: Optional[float] = None


class CashInitialBalance(BaseModel):
    accruedInterest: Optional[float] = None
    cashAvailableForTrading: Optional[float] = None
    cashAvailableForWithdrawal: Optional[float] = None
    cashBalance: Optional[float] = None
    bondValue: Optional[float] = None
    cashReceipts: Optional[float] = None
    liquidationValue: Optional[float] = None
    longOptionMarketValue: Optional[float] = None
    longStockValue: Optional[float] = None
    moneyMarketFund: Optional[float] = None
    mutualFundValue: Optional[float] = None
    shortOptionMarketValue: Optional[float] = None
    shortStockValue: Optional[float] = None
    isInCall: Optional[float] = None
    unsettledCash: Optional[float] = None
    cashDebitCallValue: Optional[float] = None
    pendingDeposits: Optional[float] = None
    accountValue: Optional[float] = None


class CashBalance(BaseModel):
    cashAvailableForTrading: Optional[float] = None
    cashAvailableForWithdrawal: Optional[float] = None
    cashCall: Optional[float] = None
    longNonMarginableMarketValue: Optional[float] = None
    totalCash: Optional[float] = None
    cashDebitCallValue: Optional[float] = None
    unsettledCash: Optional[float] = None


class AssetType1(Enum):
    EQUITY = 'EQUITY'
    OPTION = 'OPTION'
    INDEX = 'INDEX'
    MUTUAL_FUND = 'MUTUAL_FUND'
    CASH_EQUIVALENT = 'CASH_EQUIVALENT'
    FIXED_INCOME = 'FIXED_INCOME'
    CURRENCY = 'CURRENCY'
    COLLECTIVE_INVESTMENT = 'COLLECTIVE_INVESTMENT'


class TransactionBaseInstrument(BaseModel):
    assetType: AssetType1
    cusip: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    instrumentId: Optional[int] = None
    netChange: Optional[float] = None


class AccountsBaseInstrument(BaseModel):
    assetType: AssetType1
    cusip: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    instrumentId: Optional[int] = None
    netChange: Optional[float] = None


class Type1(Enum):
    SWEEP_VEHICLE = 'SWEEP_VEHICLE'
    SAVINGS = 'SAVINGS'
    MONEY_MARKET_FUND = 'MONEY_MARKET_FUND'
    UNKNOWN = 'UNKNOWN'


class TransactionCashEquivalent(TransactionBaseInstrument):
    type: Optional[Type1] = None
    assetType: Literal['CASH_EQUIVALENT']


class Type2(Enum):
    UNIT_INVESTMENT_TRUST = 'UNIT_INVESTMENT_TRUST'
    EXCHANGE_TRADED_FUND = 'EXCHANGE_TRADED_FUND'
    CLOSED_END_FUND = 'CLOSED_END_FUND'
    INDEX = 'INDEX'
    UNITS = 'UNITS'


class CollectiveInvestment(TransactionBaseInstrument):
    type: Optional[Type2] = None
    assetType: Literal['COLLECTIVE_INVESTMENT']


class Instruction(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    BUY_TO_COVER = 'BUY_TO_COVER'
    SELL_SHORT = 'SELL_SHORT'
    BUY_TO_OPEN = 'BUY_TO_OPEN'
    BUY_TO_CLOSE = 'BUY_TO_CLOSE'
    SELL_TO_OPEN = 'SELL_TO_OPEN'
    SELL_TO_CLOSE = 'SELL_TO_CLOSE'
    EXCHANGE = 'EXCHANGE'
    SELL_SHORT_EXEMPT = 'SELL_SHORT_EXEMPT'


class AssetType(Enum):
    EQUITY = 'EQUITY'
    MUTUAL_FUND = 'MUTUAL_FUND'
    OPTION = 'OPTION'
    FUTURE = 'FUTURE'
    FOREX = 'FOREX'
    INDEX = 'INDEX'
    CASH_EQUIVALENT = 'CASH_EQUIVALENT'
    FIXED_INCOME = 'FIXED_INCOME'
    PRODUCT = 'PRODUCT'
    CURRENCY = 'CURRENCY'
    COLLECTIVE_INVESTMENT = 'COLLECTIVE_INVESTMENT'


class Currency(TransactionBaseInstrument):
    assetType: Literal['CURRENCY']


class Type3(Enum):
    COMMON_STOCK = 'COMMON_STOCK'
    PREFERRED_STOCK = 'PREFERRED_STOCK'
    DEPOSITORY_RECEIPT = 'DEPOSITORY_RECEIPT'
    PREFERRED_DEPOSITORY_RECEIPT = 'PREFERRED_DEPOSITORY_RECEIPT'
    RESTRICTED_STOCK = 'RESTRICTED_STOCK'
    COMPONENT_UNIT = 'COMPONENT_UNIT'
    RIGHT = 'RIGHT'
    WARRANT = 'WARRANT'
    CONVERTIBLE_PREFERRED_STOCK = 'CONVERTIBLE_PREFERRED_STOCK'
    CONVERTIBLE_STOCK = 'CONVERTIBLE_STOCK'
    LIMITED_PARTNERSHIP = 'LIMITED_PARTNERSHIP'
    WHEN_ISSUED = 'WHEN_ISSUED'
    UNKNOWN = 'UNKNOWN'


class TransactionEquity(TransactionBaseInstrument):
    type: Optional[Type3] = None
    assetType: Literal['EQUITY']


class Type4(Enum):
    BOND_UNIT = 'BOND_UNIT'
    CERTIFICATE_OF_DEPOSIT = 'CERTIFICATE_OF_DEPOSIT'
    CONVERTIBLE_BOND = 'CONVERTIBLE_BOND'
    COLLATERALIZED_MORTGAGE_OBLIGATION = 'COLLATERALIZED_MORTGAGE_OBLIGATION'
    CORPORATE_BOND = 'CORPORATE_BOND'
    GOVERNMENT_MORTGAGE = 'GOVERNMENT_MORTGAGE'
    GNMA_BONDS = 'GNMA_BONDS'
    MUNICIPAL_ASSESSMENT_DISTRICT = 'MUNICIPAL_ASSESSMENT_DISTRICT'
    MUNICIPAL_BOND = 'MUNICIPAL_BOND'
    OTHER_GOVERNMENT = 'OTHER_GOVERNMENT'
    SHORT_TERM_PAPER = 'SHORT_TERM_PAPER'
    US_TREASURY_BOND = 'US_TREASURY_BOND'
    US_TREASURY_BILL = 'US_TREASURY_BILL'
    US_TREASURY_NOTE = 'US_TREASURY_NOTE'
    US_TREASURY_ZERO_COUPON = 'US_TREASURY_ZERO_COUPON'
    AGENCY_BOND = 'AGENCY_BOND'
    WHEN_AS_AND_IF_ISSUED_BOND = 'WHEN_AS_AND_IF_ISSUED_BOND'
    ASSET_BACKED_SECURITY = 'ASSET_BACKED_SECURITY'
    UNKNOWN = 'UNKNOWN'


class TransactionFixedIncome(TransactionBaseInstrument):
    type: Optional[Type4] = None
    maturityDate: Optional[AwareDatetime] = None
    factor: Optional[float] = None
    multiplier: Optional[float] = None
    variableRate: Optional[float] = None
    assetType: Literal['FIXED_INCOME']


class Type5(Enum):
    STANDARD = 'STANDARD'
    NBBO = 'NBBO'
    UNKNOWN = 'UNKNOWN'


class Forex(TransactionBaseInstrument):
    type: Optional[Type5] = None
    baseCurrency: Optional[Currency] = None
    counterCurrency: Optional[Currency] = None
    assetType: Literal['FOREX']


class Type6(Enum):
    STANDARD = 'STANDARD'
    UNKNOWN = 'UNKNOWN'


class Type7(Enum):
    BROAD_BASED = 'BROAD_BASED'
    NARROW_BASED = 'NARROW_BASED'
    UNKNOWN = 'UNKNOWN'


class Type8(Enum):
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    OPEN_END_NON_TAXABLE = 'OPEN_END_NON_TAXABLE'
    OPEN_END_TAXABLE = 'OPEN_END_TAXABLE'
    NO_LOAD_NON_TAXABLE = 'NO_LOAD_NON_TAXABLE'
    NO_LOAD_TAXABLE = 'NO_LOAD_TAXABLE'
    UNKNOWN = 'UNKNOWN'


class TransactionMutualFund(TransactionBaseInstrument):
    fundFamilyName: Optional[str] = None
    fundFamilySymbol: Optional[str] = None
    fundGroup: Optional[str] = None
    type: Optional[Type8] = None
    exchangeCutoffTime: Optional[AwareDatetime] = None
    purchaseCutoffTime: Optional[AwareDatetime] = None
    redemptionCutoffTime: Optional[AwareDatetime] = None
    assetType: Literal['MUTUAL_FUND']


class PutCall(Enum):
    PUT = 'PUT'
    CALL = 'CALL'
    UNKNOWN = 'UNKNOWN'


class Type9(Enum):
    VANILLA = 'VANILLA'
    BINARY = 'BINARY'
    BARRIER = 'BARRIER'
    UNKNOWN = 'UNKNOWN'


class Type10(Enum):
    TBD = 'TBD'
    UNKNOWN = 'UNKNOWN'


class Product(TransactionBaseInstrument):
    type: Optional[Type10] = None
    assetType: Literal['PRODUCT']


class Type11(Enum):
    SWEEP_VEHICLE = 'SWEEP_VEHICLE'
    SAVINGS = 'SAVINGS'
    MONEY_MARKET_FUND = 'MONEY_MARKET_FUND'
    UNKNOWN = 'UNKNOWN'


class AccountCashEquivalent(AccountsBaseInstrument):
    type: Optional[Type11] = None
    assetType: Literal['CASH_EQUIVALENT']


class AccountEquity(AccountsBaseInstrument):
    assetType: Literal['EQUITY']


class AccountFixedIncome(AccountsBaseInstrument):
    maturityDate: Optional[AwareDatetime] = None
    factor: Optional[float] = None
    variableRate: Optional[float] = None
    assetType: Literal['FIXED_INCOME']


class AccountMutualFund(AccountsBaseInstrument):
    assetType: Literal['MUTUAL_FUND']


class Type12(Enum):
    VANILLA = 'VANILLA'
    BINARY = 'BINARY'
    BARRIER = 'BARRIER'
    UNKNOWN = 'UNKNOWN'


class ApiCurrencyType(Enum):
    USD = 'USD'
    CAD = 'CAD'
    EUR = 'EUR'
    JPY = 'JPY'


class AccountAPIOptionDeliverable(BaseModel):
    symbol: Optional[str] = None
    deliverableUnits: Optional[float] = None
    apiCurrencyType: Optional[ApiCurrencyType] = None
    assetType: Optional[AssetType] = None


class ApiOrderStatus(Enum):
    AWAITING_PARENT_ORDER = 'AWAITING_PARENT_ORDER'
    AWAITING_CONDITION = 'AWAITING_CONDITION'
    AWAITING_STOP_CONDITION = 'AWAITING_STOP_CONDITION'
    AWAITING_MANUAL_REVIEW = 'AWAITING_MANUAL_REVIEW'
    ACCEPTED = 'ACCEPTED'
    AWAITING_UR_OUT = 'AWAITING_UR_OUT'
    PENDING_ACTIVATION = 'PENDING_ACTIVATION'
    QUEUED = 'QUEUED'
    WORKING = 'WORKING'
    REJECTED = 'REJECTED'
    PENDING_CANCEL = 'PENDING_CANCEL'
    CANCELED = 'CANCELED'
    PENDING_REPLACE = 'PENDING_REPLACE'
    REPLACED = 'REPLACED'
    FILLED = 'FILLED'
    EXPIRED = 'EXPIRED'
    NEW = 'NEW'
    AWAITING_RELEASE_TIME = 'AWAITING_RELEASE_TIME'
    PENDING_ACKNOWLEDGEMENT = 'PENDING_ACKNOWLEDGEMENT'
    PENDING_RECALL = 'PENDING_RECALL'
    UNKNOWN = 'UNKNOWN'


class TransactionType(Enum):
    TRADE = 'TRADE'
    RECEIVE_AND_DELIVER = 'RECEIVE_AND_DELIVER'
    DIVIDEND_OR_INTEREST = 'DIVIDEND_OR_INTEREST'
    ACH_RECEIPT = 'ACH_RECEIPT'
    ACH_DISBURSEMENT = 'ACH_DISBURSEMENT'
    CASH_RECEIPT = 'CASH_RECEIPT'
    CASH_DISBURSEMENT = 'CASH_DISBURSEMENT'
    ELECTRONIC_FUND = 'ELECTRONIC_FUND'
    WIRE_OUT = 'WIRE_OUT'
    WIRE_IN = 'WIRE_IN'
    JOURNAL = 'JOURNAL'
    MEMORANDUM = 'MEMORANDUM'
    MARGIN_CALL = 'MARGIN_CALL'
    MONEY_MARKET = 'MONEY_MARKET'
    SMA_ADJUSTMENT = 'SMA_ADJUSTMENT'


class Status1(Enum):
    VALID = 'VALID'
    INVALID = 'INVALID'
    PENDING = 'PENDING'
    UNKNOWN = 'UNKNOWN'


class SubAccount(Enum):
    CASH = 'CASH'
    MARGIN = 'MARGIN'
    SHORT = 'SHORT'
    DIV = 'DIV'
    INCOME = 'INCOME'
    UNKNOWN = 'UNKNOWN'


class ActivityType1(Enum):
    ACTIVITY_CORRECTION = 'ACTIVITY_CORRECTION'
    EXECUTION = 'EXECUTION'
    ORDER_ACTION = 'ORDER_ACTION'
    TRANSFER = 'TRANSFER'
    UNKNOWN = 'UNKNOWN'


class Type13(Enum):
    ADVISOR_USER = 'ADVISOR_USER'
    BROKER_USER = 'BROKER_USER'
    CLIENT_USER = 'CLIENT_USER'
    SYSTEM_USER = 'SYSTEM_USER'
    UNKNOWN = 'UNKNOWN'


class UserDetails(BaseModel):
    cdDomainId: Optional[str] = None
    login: Optional[str] = None
    type: Optional[Type13] = None
    userId: Optional[int] = None
    systemUserName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    brokerRepCode: Optional[str] = None


class FeeType1(Enum):
    COMMISSION = 'COMMISSION'
    SEC_FEE = 'SEC_FEE'
    STR_FEE = 'STR_FEE'
    R_FEE = 'R_FEE'
    CDSC_FEE = 'CDSC_FEE'
    OPT_REG_FEE = 'OPT_REG_FEE'
    ADDITIONAL_FEE = 'ADDITIONAL_FEE'
    MISCELLANEOUS_FEE = 'MISCELLANEOUS_FEE'
    FUTURES_EXCHANGE_FEE = 'FUTURES_EXCHANGE_FEE'
    LOW_PROCEEDS_COMMISSION = 'LOW_PROCEEDS_COMMISSION'
    BASE_CHARGE = 'BASE_CHARGE'
    GENERAL_CHARGE = 'GENERAL_CHARGE'
    GST_FEE = 'GST_FEE'
    TAF_FEE = 'TAF_FEE'
    INDEX_OPTION_FEE = 'INDEX_OPTION_FEE'
    UNKNOWN = 'UNKNOWN'


class PositionEffect1(Enum):
    OPENING = 'OPENING'
    CLOSING = 'CLOSING'
    AUTOMATIC = 'AUTOMATIC'
    UNKNOWN = 'UNKNOWN'


class UserPreferenceAccount(BaseModel):
    accountNumber: Optional[str] = None
    primaryAccount: Optional[bool] = False
    type: Optional[str] = None
    nickName: Optional[str] = None
    accountColor: Optional[str] = Field(None, description='Green | Blue')
    displayAcctId: Optional[str] = None
    autoPositionEffect: Optional[bool] = False


class StreamerInfo(BaseModel):
    streamerSocketUrl: Optional[str] = None
    schwabClientCustomerId: Optional[str] = None
    schwabClientCorrelId: Optional[str] = None
    schwabClientChannel: Optional[str] = None
    schwabClientFunctionId: Optional[str] = None


class Offer(BaseModel):
    level2Permissions: Optional[bool] = False
    mktDataPermission: Optional[str] = None


class OrderLeg(BaseModel):
    askPrice: Optional[float] = None
    bidPrice: Optional[float] = None
    lastPrice: Optional[float] = None
    markPrice: Optional[float] = None
    projectedCommission: Optional[float] = None
    quantity: Optional[float] = None
    finalSymbol: Optional[str] = None
    legId: Optional[float] = None
    assetType: Optional[AssetType] = None
    instruction: Optional[Instruction] = None


class OrderValidationDetail(BaseModel):
    validationRuleName: Optional[str] = None
    message: Optional[str] = None
    activityMessage: Optional[str] = None
    originalSeverity: Optional[APIRuleAction] = None
    overrideName: Optional[str] = None
    overrideSeverity: Optional[APIRuleAction] = None


class CommissionValue(BaseModel):
    value: Optional[float] = None
    type: Optional[FeeType] = None


class FeeValue(BaseModel):
    value: Optional[float] = None
    type: Optional[FeeType] = None


class OrderActivity(BaseModel):
    activityType: Optional[ActivityType] = None
    executionType: Optional[ExecutionType] = None
    quantity: Optional[float] = None
    orderRemainingQuantity: Optional[float] = None
    executionLegs: Optional[List[ExecutionLeg]] = None


class AccountOption(AccountsBaseInstrument):
    optionDeliverables: Optional[List[AccountAPIOptionDeliverable]] = None
    putCall: Optional[PutCall] = None
    optionMultiplier: Optional[int] = None
    type: Optional[Type12] = None
    underlyingSymbol: Optional[str] = None
    assetType: Literal['OPTION']


class UserPreference(BaseModel):
    accounts: Optional[List[UserPreferenceAccount]] = None
    streamerInfo: Optional[List[StreamerInfo]] = None
    offers: Optional[List[Offer]] = None


class OrderStrategy(BaseModel):
    accountNumber: Optional[str] = None
    advancedOrderType: Optional[AdvancedOrderType] = None
    closeTime: Optional[AwareDatetime] = None
    enteredTime: Optional[AwareDatetime] = None
    orderBalance: Optional[OrderBalance] = None
    orderStrategyType: Optional[OrderStrategyType] = None
    orderVersion: Optional[float] = None
    session: Optional[Session] = None
    status: Optional[ApiOrderStatus] = None
    allOrNone: Optional[bool] = None
    discretionary: Optional[bool] = None
    duration: Optional[Duration] = None
    filledQuantity: Optional[float] = None
    orderType: Optional[OrderType] = None
    orderValue: Optional[float] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    remainingQuantity: Optional[float] = None
    sellNonMarginableFirst: Optional[bool] = None
    settlementInstruction: Optional[SettlementInstruction] = None
    strategy: Optional[ComplexOrderStrategyType] = None
    amountIndicator: Optional[AmountIndicator] = None
    orderLegs: Optional[List[OrderLeg]] = None


class OrderValidationResult(BaseModel):
    alerts: Optional[List[OrderValidationDetail]] = None
    accepts: Optional[List[OrderValidationDetail]] = None
    rejects: Optional[List[OrderValidationDetail]] = None
    reviews: Optional[List[OrderValidationDetail]] = None
    warns: Optional[List[OrderValidationDetail]] = None


class CommissionLeg(BaseModel):
    commissionValues: Optional[List[CommissionValue]] = None


class FeeLeg(BaseModel):
    feeValues: Optional[List[FeeValue]] = None


class AccountsInstrument(
    RootModel[
        Union[
            AccountCashEquivalent,
            AccountEquity,
            AccountFixedIncome,
            AccountMutualFund,
            AccountOption,
        ]
    ]
):
    root: Union[
        AccountCashEquivalent, AccountEquity, AccountFixedIncome, AccountMutualFund, AccountOption
    ] = Field(..., discriminator='assetType')


class Commission(BaseModel):
    commissionLegs: Optional[List[CommissionLeg]] = None


class Fees(BaseModel):
    feeLegs: Optional[List[FeeLeg]] = None


class Position(BaseModel):
    shortQuantity: Optional[float] = None
    averagePrice: Optional[float] = None
    currentDayProfitLoss: Optional[float] = None
    currentDayProfitLossPercentage: Optional[float] = None
    longQuantity: Optional[float] = None
    settledLongQuantity: Optional[float] = None
    settledShortQuantity: Optional[float] = None
    agedQuantity: Optional[float] = None
    instrument: Optional[AccountsInstrument] = None
    marketValue: Optional[float] = None
    maintenanceRequirement: Optional[float] = None
    averageLongPrice: Optional[float] = None
    averageShortPrice: Optional[float] = None
    taxLotAverageLongPrice: Optional[float] = None
    taxLotAverageShortPrice: Optional[float] = None
    longOpenProfitLoss: Optional[float] = None
    shortOpenProfitLoss: Optional[float] = None
    previousSessionLongQuantity: Optional[float] = None
    previousSessionShortQuantity: Optional[float] = None
    currentDayCost: Optional[float] = None


class OrderLegCollection(BaseModel):
    orderLegType: Optional[OrderLegType] = None
    legId: Optional[int] = None
    instrument: Optional[AccountsInstrument] = None
    instruction: Optional[Instruction] = None
    positionEffect: Optional[PositionEffect] = None
    quantity: Optional[float] = None
    quantityType: Optional[QuantityType] = None
    divCapGains: Optional[DivCapGains] = None
    toSymbol: Optional[str] = None


class SecuritiesAccountBase(BaseModel):
    type: Optional[Type] = None
    accountNumber: Optional[str] = None
    roundTrips: Optional[int] = None
    isDayTrader: Optional[bool] = False
    isClosingOnlyRestricted: Optional[bool] = False
    pfcbFlag: Optional[bool] = False
    positions: Optional[List[Position]] = None


class MarginAccount(SecuritiesAccountBase):
    initialBalances: Optional[MarginInitialBalance] = None
    currentBalances: Optional[MarginBalance] = None
    projectedBalances: Optional[MarginBalance] = None
    type: Literal['MARGIN']


class CashAccount(SecuritiesAccountBase):
    initialBalances: Optional[CashInitialBalance] = None
    currentBalances: Optional[CashBalance] = None
    projectedBalances: Optional[CashBalance] = None
    type: Literal['CASH']


class CommissionAndFee(BaseModel):
    commission: Optional[Commission] = None
    fee: Optional[Fees] = None
    trueCommission: Optional[Commission] = None


class Order(BaseModel):
    session: Optional[Session] = None
    duration: Optional[Duration] = None
    orderType: Optional[OrderType] = None
    cancelTime: Optional[AwareDatetime] = None
    complexOrderStrategyType: Optional[ComplexOrderStrategyType] = None
    quantity: Optional[float] = None
    filledQuantity: Optional[float] = None
    remainingQuantity: Optional[float] = None
    requestedDestination: Optional[RequestedDestination] = None
    destinationLinkName: Optional[str] = None
    releaseTime: Optional[AwareDatetime] = None
    stopPrice: Optional[float] = None
    stopPriceLinkBasis: Optional[StopPriceLinkBasis] = None
    stopPriceLinkType: Optional[StopPriceLinkType] = None
    stopPriceOffset: Optional[float] = None
    stopType: Optional[StopType] = None
    priceLinkBasis: Optional[PriceLinkBasis] = None
    priceLinkType: Optional[PriceLinkType] = None
    price: Optional[float] = None
    taxLotMethod: Optional[TaxLotMethod] = None
    orderLegCollection: Optional[List[OrderLegCollection]] = None
    activationPrice: Optional[float] = None
    specialInstruction: Optional[SpecialInstruction] = None
    orderStrategyType: Optional[OrderStrategyType] = None
    orderId: Optional[int] = None
    cancelable: Optional[bool] = False
    editable: Optional[bool] = False
    status: Optional[Status] = None
    enteredTime: Optional[AwareDatetime] = None
    closeTime: Optional[AwareDatetime] = None
    tag: Optional[str] = None
    accountNumber: Optional[int] = None
    orderActivityCollection: Optional[List[OrderActivity]] = None
    replacingOrderCollection: Optional[List[Order]] = None
    childOrderStrategies: Optional[List[Order]] = None
    statusDescription: Optional[str] = None


class OrderRequest(BaseModel):
    session: Optional[Session] = None
    duration: Optional[Duration] = None
    orderType: Optional[OrderTypeRequest] = None
    cancelTime: Optional[AwareDatetime] = None
    complexOrderStrategyType: Optional[ComplexOrderStrategyType] = None
    quantity: Optional[float] = None
    filledQuantity: Optional[float] = None
    remainingQuantity: Optional[float] = None
    destinationLinkName: Optional[str] = None
    releaseTime: Optional[AwareDatetime] = None
    stopPrice: Optional[float] = None
    stopPriceLinkBasis: Optional[StopPriceLinkBasis] = None
    stopPriceLinkType: Optional[StopPriceLinkType] = None
    stopPriceOffset: Optional[float] = None
    stopType: Optional[StopType] = None
    priceLinkBasis: Optional[PriceLinkBasis] = None
    priceLinkType: Optional[PriceLinkType] = None
    price: Optional[float] = None
    taxLotMethod: Optional[TaxLotMethod] = None
    orderLegCollection: Optional[List[OrderLegCollection]] = None
    activationPrice: Optional[float] = None
    specialInstruction: Optional[SpecialInstruction] = None
    orderStrategyType: Optional[OrderStrategyType] = None
    orderId: Optional[int] = None
    cancelable: Optional[bool] = False
    editable: Optional[bool] = False
    status: Optional[Status] = None
    enteredTime: Optional[AwareDatetime] = None
    closeTime: Optional[AwareDatetime] = None
    accountNumber: Optional[int] = None
    orderActivityCollection: Optional[List[OrderActivity]] = None
    replacingOrderCollection: Optional[List[OrderRequest]] = None
    childOrderStrategies: Optional[List[OrderRequest]] = None
    statusDescription: Optional[str] = None


class PreviewOrder(BaseModel):
    orderId: Optional[int] = None
    orderStrategy: Optional[OrderStrategy] = None
    orderValidationResult: Optional[OrderValidationResult] = None
    commissionAndFee: Optional[CommissionAndFee] = None


class SecuritiesAccount(RootModel[Union[MarginAccount, CashAccount]]):
    root: Union[MarginAccount, CashAccount] = Field(..., discriminator='type')


class Account(BaseModel):
    securitiesAccount: Optional[SecuritiesAccount] = None


class TransactionInstrument(
    RootModel[
        Union[
            TransactionCashEquivalent,
            CollectiveInvestment,
            Currency,
            TransactionEquity,
            TransactionFixedIncome,
            Forex,
            # Future,
            # Index,
            TransactionMutualFund,
            # TransactionOption,
            Product,
        ]
    ]
):
    root: Union[
        TransactionCashEquivalent,
        CollectiveInvestment,
        Currency,
        TransactionEquity,
        TransactionFixedIncome,
        Forex,
        Future,
        Index,
        TransactionMutualFund,
        TransactionOption,
        Product,
    ] = Field(..., discriminator='assetType')


class TransactionOption(TransactionBaseInstrument):
    expirationDate: Optional[AwareDatetime] = None
    optionDeliverables: Optional[List[TransactionAPIOptionDeliverable]] = None
    optionPremiumMultiplier: Optional[int] = None
    putCall: Optional[PutCall] = None
    strikePrice: Optional[float] = None
    type: Optional[Type9] = None
    underlyingSymbol: Optional[str] = None
    underlyingCusip: Optional[str] = None
    deliverable: Optional[TransactionInstrument] = None
    assetType: Literal['OPTION']


class TransactionAPIOptionDeliverable(BaseModel):
    rootSymbol: Optional[str] = None
    strikePercent: Optional[int] = None
    deliverableNumber: Optional[int] = None
    deliverableUnits: Optional[float] = None
    deliverable: Optional[TransactionInstrument] = None
    assetType: Optional[AssetType] = None


class Transaction(BaseModel):
    activityId: Optional[int] = None
    time: Optional[AwareDatetime] = None
    user: Optional[UserDetails] = None
    description: Optional[str] = None
    accountNumber: Optional[str] = None
    type: Optional[TransactionType] = None
    status: Optional[Status1] = None
    subAccount: Optional[SubAccount] = None
    tradeDate: Optional[AwareDatetime] = None
    settlementDate: Optional[AwareDatetime] = None
    positionId: Optional[int] = None
    orderId: Optional[int] = None
    netAmount: Optional[float] = None
    activityType: Optional[ActivityType1] = None
    transferItems: Optional[List[TransferItem]] = None


class TransferItem(BaseModel):
    instrument: Optional[TransactionInstrument] = None
    amount: Optional[float] = None
    cost: Optional[float] = None
    price: Optional[float] = None
    feeType: Optional[FeeType1] = None
    positionEffect: Optional[PositionEffect1] = None


class Future(BaseModel):
    activeContract: Optional[bool] = False
    type: Optional[Type6] = None
    expirationDate: Optional[AwareDatetime] = None
    lastTradingDate: Optional[AwareDatetime] = None
    firstNoticeDate: Optional[AwareDatetime] = None
    multiplier: Optional[float] = None
    assetType: Literal['FUTURE']


class Index(BaseModel):
    activeContract: Optional[bool] = False
    type: Optional[Type7] = None
    assetType: Literal['INDEX']


Order.model_rebuild()
OrderRequest.model_rebuild()
TransactionInstrument.model_rebuild()
TransactionOption.model_rebuild()
Transaction.model_rebuild()
Future.model_rebuild()
Index.model_rebuild()

# fmt: on
