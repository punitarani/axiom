from enum import Enum


class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    OPTION = "OPTION"


class AssetType(str, Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    CEF = "CEF"
    ADR = "ADR"
    INDEX = "INDEX"


class AssetSubType(str, Enum):
    COE = "COE"
    PRF = "PRF"
    ADR = "ADR"
    GDR = "GDR"
    CEF = "CEF"
    ETF = "ETF"
    ETN = "ETN"
    UIT = "UIT"
    WAR = "WAR"
    RGT = "RGT"


class SecurityStatus(str, Enum):
    NORMAL = "Normal"
    HALTED = "Halted"
    CLOSED = "Closed"
    SUSPENDED = "Suspended"


class OrderSide(str, Enum):
    BID = "BID"
    ASK = "ASK"


class Timeframe(str, Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    FOUR_HOUR = "4h"
    ONE_DAY = "1d"


class ContractType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class ExpirationType(str, Enum):
    MONTHLY = "MONTHLY"
    WEEKLY = "WEEKLY"
    QUARTERLY = "QUARTERLY"
    STANDARD = "STANDARD"


class ExerciseType(str, Enum):
    AMERICAN = "AMERICAN"
    EUROPEAN = "EUROPEAN"


class SettlementType(str, Enum):
    PHYSICAL = "PHYSICAL"
    CASH = "CASH"


class TransactionType(str, Enum):
    TRADE = "TRADE"
    RECEIVE_AND_DELIVER = "RECEIVE_AND_DELIVER"
    DIVIDEND_OR_INTEREST = "DIVIDEND_OR_INTEREST"
    ACH_RECEIPT = "ACH_RECEIPT"
    ACH_DISBURSEMENT = "ACH_DISBURSEMENT"
    CASH_RECEIPT = "CASH_RECEIPT"
    CASH_DISBURSEMENT = "CASH_DISBURSEMENT"
    ELECTRONIC_FUND = "ELECTRONIC_FUND"
    WIRE_OUT = "WIRE_OUT"
    WIRE_IN = "WIRE_IN"
    JOURNAL = "JOURNAL"
    MEMORANDUM = "MEMORANDUM"
    MARGIN_CALL = "MARGIN_CALL"
    MONEY_MARKET = "MONEY_MARKET"
    SMA_ADJUSTMENT = "SMA_ADJUSTMENT"
