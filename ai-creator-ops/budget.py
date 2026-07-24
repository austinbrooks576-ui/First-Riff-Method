#!/usr/bin/env python3
"""Revenue split for a disclosed AI-creator brand.

Computes net revenue after platform + processor fees, then splits it into
production reinvestment (the 30% flow), operator draw, a chargeback reserve
(adult processors hold funds — this matters), and growth.

No banking details live here. Payouts are configured in each platform's own
dashboard against the operator's verified identity.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

# Split of NET revenue (after platform + processor fees). Must sum to 1.0.
SPLIT = {
    "production": 0.30,  # image-gen credits, editing, new character assets
    "owner_draw": 0.45,  # operator income
    "reserve":    0.15,  # chargeback / payout-hold buffer
    "growth":     0.10,  # promo where platforms allow it
}


@dataclass
class Breakdown:
    gross: float
    platform_fee: float
    processor_fee: float
    net: float
    buckets: dict[str, float]


def compute(gross: float, platform_fee_pct: float = 20.0,
            processor_fee_pct: float = 3.0) -> Breakdown:
    if gross < 0:
        raise ValueError("gross must be non-negative")
    assert abs(sum(SPLIT.values()) - 1.0) < 1e-9, "SPLIT must sum to 1.0"

    platform_fee = gross * platform_fee_pct / 100.0
    processor_fee = gross * processor_fee_pct / 100.0
    net = gross - platform_fee - processor_fee
    buckets = {name: net * pct for name, pct in SPLIT.items()}
    return Breakdown(gross, platform_fee, processor_fee, net, buckets)


def render(b: Breakdown) -> str:
    lines = [
        f"Gross revenue        ${b.gross:>12,.2f}",
        f"  Platform fee      -${b.platform_fee:>12,.2f}",
        f"  Processor fee     -${b.processor_fee:>12,.2f}",
        f"Net revenue          ${b.net:>12,.2f}",
        "",
        "Allocation:",
    ]
    for name, amount in b.buckets.items():
        lines.append(f"  {name:<12} {SPLIT[name]*100:>4.0f}%  ${amount:>12,.2f}")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="AI-creator revenue split")
    p.add_argument("--gross", type=float, required=True, help="gross revenue")
    p.add_argument("--platform-fee-pct", type=float, default=20.0)
    p.add_argument("--processor-fee-pct", type=float, default=3.0)
    args = p.parse_args()
    print(render(compute(args.gross, args.platform_fee_pct,
                         args.processor_fee_pct)))


if __name__ == "__main__":
    main()
