from typing import Any, Dict

import pandas as pd
import numpy as np


def smallest_viable_type(srs: pd.Series, cat_thresh=0.95, sample_size=None):
    """Determine smallest viable type for Pandas Series."""

    def type_cast_successful(srs, type_) -> bool:
        return np.allclose(srs.astype(type_), srs)

    if sample_size and srs.size > sample_size:
        srs = srs.sample(n=sample_size)  # type: ignore

    original_dtype = srs.dtype
    if np.issubdtype(original_dtype, np.number):
        val_range = srs.min(), srs.max()
        is_signed = val_range[0] < 0
        is_nullable = srs.isna().sum() > 0
        is_decimal = not np.isclose(np.sum(np.mod(srs.values, 1)), 0)

        if not is_decimal:
            if is_nullable:
                if is_signed:
                    int_types = [
                        pd.Int8Dtype,
                        pd.Int16Dtype,
                        pd.Int32Dtype,
                        pd.Int64Dtype,
                    ]
                    for type_ in int_types:
                        if type_cast_successful(srs, type_):
                            return type_
                # Unsigned
                else:
                    uint_types = [
                        pd.UInt8Dtype,
                        pd.UInt16Dtype,
                        pd.UInt32Dtype,
                        pd.UInt64Dtype,
                    ]
                    for type_ in uint_types:
                        if type_cast_successful(srs, type_):
                            return type_
            # Not nullable
            else:
                if is_signed:
                    int_types = [np.int8, np.int16, np.int32, np.int64]
                    for type_ in int_types:
                        if type_cast_successful(srs, type_):
                            return type_
                # Unsigned
                else:
                    # Identify 1 / 0 flags and cast to `np.bool`
                    if (
                        np.isclose(val_range[0], 0)
                        and (np.isclose(val_range[1], 0) or np.isclose(val_range[1], 1))
                        and np.size(srs.unique()) <= 2
                    ):
                        return np.bool

                    uint_types = [np.uint8, np.uint16, np.uint32, np.uint64]
                    for type_ in uint_types:
                        if type_cast_successful(srs, type_):
                            return type_
        # Float type
        float_types = [np.float16, np.float32, np.float64, np.float128]
        for type_ in float_types:
            if type_cast_successful(srs, type_):
                return type_

    # Non-numeric
    else:
        unique_count = np.size(srs.unique())
        srs_length = srs.size
        unique_pct = unique_count / srs_length
        if unique_pct < cat_thresh:
            return pd.CategoricalDtype()
        return np.object

    # Keep original type if nothing else works
    return original_dtype


def minimum_viable_schema(
    df: pd.DataFrame, cat_thresh=0.8, sample_size=10_000
) -> Dict[str, Any]:
    """Determine minimum viable schema for Pandas DataFrame."""
    df = df.copy()
    if sample_size:
        # Use head and tail in case DataFrame is sorted
        df = _sample_head_tail(df)
    schema = {
        str(col): smallest_viable_type(srs, cat_thresh=cat_thresh)
        for col, srs in df.iteritems()
    }
    return schema


def _sample_head_tail(df: pd.DataFrame, sample_size: int = 10_000):
    """Sample from head and tail of DataFrame."""
    half_sample = sample_size // 2
    return df[:half_sample].append(df[-half_sample:])
