"""Прозора модель unit economics для одного клієнта підписного сервісу.

Часовий горизонт: місяці; внесок від активного клієнта у кожному місяці;
у нульовому місяці витрачається CAC.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Inputs:
    cac: float
    monthly_revenue: float
    gross_margin_percent: float
    monthly_churn_percent: float


@dataclass(frozen=True)
class Results:
    monthly_contribution: float
    ltv: float
    ltv_cac: float
    expected_months: float
    payback_month: int | None
    value_60m: float
    net_60m: float
    months: tuple[int, ...]
    cumulative_contribution: tuple[float, ...]
    cumulative_after_cac: tuple[float, ...]


def calculate(inputs: Inputs, horizon: int = 60) -> Results:
    if inputs.cac <= 0 or inputs.monthly_revenue < 0:
        raise ValueError('CAC має бути > 0, а виручка — не від’ємною.')
    if not 0 <= inputs.gross_margin_percent <= 100:
        raise ValueError('Маржа має бути від 0 до 100%.')
    if not 0 < inputs.monthly_churn_percent <= 100:
        raise ValueError('Churn має бути понад 0% і не більше 100%.')
    if horizon < 1:
        raise ValueError('Горизонт має становити щонайменше один місяць.')

    churn = inputs.monthly_churn_percent / 100.0
    contribution = inputs.monthly_revenue * inputs.gross_margin_percent / 100.0
    ltv = contribution / churn
    months = tuple(range(horizon + 1))
    # Кумулятивний очікуваний валовий прибуток за t місяців
    earned = tuple(contribution * (1 - (1 - churn) ** t) / churn for t in months)
    after_cac = tuple(value - inputs.cac for value in earned)

    # Шукаємо перший місяць окупності з урахуванням втрати клієнтів.
    if contribution == 0 or ltv <= inputs.cac:
        payback_month = None
    else:
        if churn == 1:
            payback_month = 1
        else:
            threshold = 1 - inputs.cac / ltv
            payback_month = max(1, math.ceil(math.log(threshold) / math.log(1 - churn) - 1e-12))

    return Results(
        monthly_contribution=contribution,
        ltv=ltv,
        ltv_cac=ltv / inputs.cac,
        expected_months=1.0 / churn,
        payback_month=payback_month,
        value_60m=earned[-1],
        net_60m=after_cac[-1],
        months=months,
        cumulative_contribution=earned,
        cumulative_after_cac=after_cac,
    )
