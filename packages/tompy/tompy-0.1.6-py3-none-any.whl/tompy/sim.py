from typing import Callable, Tuple

import numpy as np
import pandas as pd


def ysim(
    df: pd.DataFrame,
    f_y_pred: Callable[[pd.DataFrame, int], Tuple[float, float]],
    f_y_true: Callable[[pd.DataFrame, int], Tuple[float, float]],
) -> pd.DataFrame:
    """
    f_y_pred(df, i) -> y_pred, y_pos
    f_y_true(df, i) -> y_true, y_lr
    output columns = ["y_pred", "y_pos", "y_true", "y_lr", "y_sr", "y_psr", "y_plr"]
    """
    df = df.dropna()
    columns = ["y_pred", "y_pos", "y_true", "y_lr", "y_sr", "y_psr", "y_plr"]
    dfo = pd.DataFrame(index=df.index, columns=columns)
    ny = df.shape[0]
    for i in range(1, ny):
        y_pred, y_pos = f_y_pred(df, i - 1)
        y_true, y_lr = f_y_true(df, i)
        y_sr = np.exp(y_lr) - 1.0
        y_psr = y_sr * y_pos
        y_plr = np.log(1.0 + y_psr)
        dfo.iloc[i] = pd.Series(
            data=[y_pred, y_pos, y_true, y_lr, y_sr, y_psr, y_plr],
            index=columns,
        )
    return dfo.dropna()


def ytest(
    df: pd.DataFrame,
    f_y_pred: Callable[[pd.DataFrame, int], Tuple[float, float]],
) -> pd.DataFrame:
    """
    f_y_pred(df, i) -> y_pred, y_pos
    output columns = ["y_pred", "y_pos"]
    """
    df = df.dropna()
    columns = ["y_pred", "y_pos"]
    dfo = pd.DataFrame(index=df.index, columns=columns)
    ny = df.shape[0]
    i = ny - 1
    y_pred, y_pos = f_y_pred(df, i)
    dfo.iloc[i] = pd.Series(data=[y_pred, y_pos], index=columns)
    return dfo.dropna()
