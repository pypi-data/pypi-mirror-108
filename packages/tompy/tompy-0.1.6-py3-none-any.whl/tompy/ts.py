import datetime
import random
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import optimize as sco
from sklearn import metrics

###############################################################################
# datetime
###############################################################################


def div(dividend: float, divisor: float) -> float:
    if divisor == 0.0:
        return 0.0
    else:
        return dividend / divisor


###############################################################################
# datetime
###############################################################################


def date(year: int, month: int, day: int) -> datetime.date:
    return datetime.date(year, month, day)


def date_today() -> datetime.date:
    """
    Return the current local date.
    """
    return datetime.date.today()


def date_add(d: datetime.date, days: int) -> datetime.date:
    """
    days range: -999999999 <= days <= 999999999
    """
    return d + datetime.timedelta(days=days)


def date_weekday(d: datetime.date) -> int:
    """
    Return the day of the week as an integer, Monday is 0 and Sunday is 6.
    """
    return d.weekday()


def date_is_weekend(d: datetime.date) -> bool:
    return date_weekday(d) > 4


def date_str(d: datetime.date) -> str:
    """
    Return a string representing the date in ISO 8601 format, YYYY-MM-DD.
    """
    return d.isoformat()


def date_from_str(datestr: str, fmt: str = "%Y-%m-%d") -> datetime.date:
    return datetime.datetime.strptime(datestr, fmt).date()


def datetime_now() -> datetime.datetime:
    """
    Return the current local datetime.
    """
    return datetime.datetime.now()


###############################################################################
# pandas
###############################################################################


def read_csv(
    fpath: str, index_col: Optional[int] = 0, parse_dates: bool = True
) -> pd.DataFrame:
    return pd.read_csv(fpath, index_col=index_col, parse_dates=parse_dates)


def write_csv(df: pd.DataFrame, fpath: str) -> None:
    df.to_csv(fpath)


def df_drop_weekends(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.index.dayofweek < 5]


def risk(
    df: pd.DataFrame,
    o: str,
    h: str,
    l: str,
    c: str,
    window: int = 20,
    ann_factor: int = 252,
) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["O"] = df[o]
    df1["H"] = df[h]
    df1["L"] = df[l]
    df1["C"] = df[c]
    df1["C1"] = df1["C"].shift()
    df1["TR_HL"] = np.abs(df1["H"] - df1["L"])
    df1["TR_HC"] = np.abs(df1["H"] - df1["C1"])
    df1["TR_LC"] = np.abs(df1["L"] - df1["C1"])
    df1["TR"] = df1[["TR_HL", "TR_HC", "TR_LC"]].max(axis=1, skipna=False)
    df1["ATR"] = df1["TR"].rolling(window).mean()
    df1["PATR"] = df1["ATR"] / df1["C"]
    df1["SR_OC"] = df1["O"] / df1["C1"] - 1.0
    df1["SR_CO"] = df1["C"] / df1["O"] - 1.0
    df1["SR_CC"] = df1["C"].pct_change()
    df1["LR_OC"] = np.log(1.0 + df1["SR_OC"])
    df1["LR_CO"] = np.log(1.0 + df1["SR_CO"])
    df1["LR_CC"] = np.log(1.0 + df1["SR_CC"])
    df1["HVOL"] = df1["LR_CC"].rolling(window).std() * np.sqrt(ann_factor)
    return df1


def ma(df: pd.DataFrame, c: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["C"] = df[c]
    for t in terms:
        st = str(t)
        df1[st] = df1["C"].rolling(t).mean()
    return df1


def ema(df: pd.DataFrame, c: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["C"] = df[c]
    for t in terms:
        st = str(t)
        df1[st] = df1["C"].ewm(span=t, adjust=False).mean()
    return df1


def high(df: pd.DataFrame, h: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["H"] = df[h]
    for t in terms:
        st = str(t)
        df1[st] = df1["H"].rolling(t).max()
    return df1


def low(df: pd.DataFrame, l: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["L"] = df[l]
    for t in terms:
        st = str(t)
        df1[st] = df1["L"].rolling(t).min()
    return df1


###############################################################################
# numpy
###############################################################################


def random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def sr2lr(sr: Any) -> Any:
    return np.log(1.0 + sr)


def lr2sr(lr: Any) -> Any:
    return np.exp(lr) - 1.0


def lr_cum(lr: np.ndarray) -> np.ndarray:
    return np.cumsum(lr)


def lr_mean(lr: np.ndarray, ann_factor: int = 252) -> float:
    return float(np.mean(lr) * ann_factor)


def lr_vol(lr: np.ndarray, ann_factor: int = 252) -> float:
    return float(np.std(lr, ddof=1) * np.sqrt(ann_factor))


def lr_sharpe(lr: np.ndarray, ann_factor: int = 252) -> float:
    m = lr_mean(lr, ann_factor=ann_factor)
    v = lr_vol(lr, ann_factor=ann_factor)
    return div(m, v)


def lr_mdd(lr: np.ndarray) -> float:
    cum = lr_cum(np.concatenate(([0.0], lr)))
    peak = np.maximum.accumulate(cum)
    dd = cum - peak
    mdd = np.min(dd)
    return float(mdd)


def analysis(
    lr: np.ndarray,
    column_name: str,
    ann_factor: int = 252,
) -> pd.DataFrame:
    """
    ndarray(n,)
    """
    n = lr.shape[0]
    c = lr_cum(lr)[-1]
    m = lr_mean(lr, ann_factor=ann_factor)
    if n > 1:
        v = lr_vol(lr, ann_factor=ann_factor)
        sharpe = div(m, v)
    else:
        v = np.nan
        sharpe = np.nan
    mdd = lr_mdd(lr)
    mar = div(m, np.abs(mdd))
    index = [
        "cum",
        "ann_mean",
        "ann_vol",
        "ann_sharpe",
        "mdd",
        "mar",
    ]
    data = [
        c,
        m,
        v,
        sharpe,
        mdd,
        mar,
    ]
    df = pd.DataFrame(data=data, index=index)
    df.columns = [column_name]
    return df


def analysis_terms(lr: np.ndarray) -> pd.DataFrame:
    """
    ndarray(n,)
    """
    ann_factor = 252
    D = 1
    W = 5
    M = 21
    Y = M * 12
    n = lr.shape[0]
    kvs = {
        "1D": 1 * D,
        "1W": 1 * W,
        "1M": 1 * M,
        "3M": 3 * M,
        "6M": 6 * M,
        "1Y": 1 * Y,
        "3Y": 3 * Y,
        "5Y": 5 * Y,
        "10Y": 10 * Y,
        "ITD": n,
    }

    dfo = pd.DataFrame()
    for key, term in kvs.items():
        if term <= n:
            dfi = analysis(lr[-term:], key, ann_factor=ann_factor)
            dfo = pd.concat([dfo, dfi], axis=1)
        else:
            dfo[key] = np.nan
    return dfo


def confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Tuple[int, int, int, int]:
    """
    ndarray(n,), ndarray(n,)
    return tn, fp, fn, tp
    """
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp


def print_confusion_matrix(tn: int, fp: int, fn: int, tp: int) -> None:
    print("confusion matrix")
    print("tp fn")
    print("fp tn")
    print(tp, fn, tp + fn)
    print(fp, tn, fp + tn)
    print(tp + fp, fn + tn, tp + fn + fp + tn)
    print("accuracy  ", div(tp + tn, tp + fn + fp + tn))
    print("tp/(tp+fp)", div(tp, tp + fp))
    print("tn/(fn+tn)", div(tn, fn + tn))
    print("tp/(tp+fn)", div(tp, tp + fn))
    print("tn/(fp+tn)", div(tn, fp + tn))


def sco_minimize(*args: Any, **kwargs: Any) -> np.ndarray:
    res = sco.minimize(*args, **kwargs)
    if res.success:
        assert isinstance(res.x, np.ndarray)
        return res.x
    assert False


def crp(sr: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    ndarray(m, n), ndarray(n,) -> ndarray(m,)
    """
    ret = np.dot(sr, w)
    assert isinstance(ret, np.ndarray)
    return ret


def max_kelly(
    sr: np.ndarray,
    bounds: List[Tuple[float, float]],
    constraints: List[Dict[str, Any]],
) -> np.ndarray:
    """
    ndarray(m, n), bounds, constraints -> ndarray(n,)
    """
    nx0 = sr.shape[1]
    ix0 = np.zeros(nx0) + (1.0 / nx0)

    def fun(ix1: np.ndarray) -> float:
        return float(-np.mean(sr2lr(crp(sr, ix1))))

    return sco_minimize(fun, x0=ix0, bounds=bounds, constraints=constraints)
