#!/usr/bin/env python3
"""Subscriber CRM for a disclosed AI-creator brand.

Tracks subscribers, tiers, lifetime value, and VIP status, and surfaces who
needs attention first — VIPs and high-LTV subs are prioritized, matching the
"top subscribers are the priority" rule structurally rather than by vibes.

Non-explicit by design. Message drafting (see `draft_reply`) produces only
neutral, non-sexual copy: greetings, tier info, upsell, retention. Anything
sexual is left to a human operator.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import IntEnum


class Tier(IntEnum):
    FREE = 0
    T1 = 1      # $9.99  standard gallery
    T2 = 2      # $24.99 gallery + priority DM
    VIP = 3     # $99+   first access, custom requests, top of queue


TIER_PRICE = {Tier.FREE: 0.0, Tier.T1: 9.99, Tier.T2: 24.99, Tier.VIP: 99.0}


@dataclass
class Subscriber:
    handle: str
    platform: str
    tier: Tier = Tier.FREE
    lifetime_value: float = 0.0
    last_contact: str = ""          # ISO date
    joined: str = field(default_factory=lambda: date.today().isoformat())
    notes: str = ""

    @property
    def is_vip(self) -> bool:
        return self.tier == Tier.VIP

    def days_since_contact(self, today: date | None = None) -> int:
        if not self.last_contact:
            return 10_000
        today = today or date.today()
        return (today - date.fromisoformat(self.last_contact)).days


def priority_score(s: Subscriber, today: date | None = None) -> float:
    """Higher = attend to sooner. VIP and LTV weighted up; staleness adds urgency."""
    base = int(s.tier) * 100 + s.lifetime_value
    staleness = min(s.days_since_contact(today), 90)
    return base + staleness


def queue(subs: list[Subscriber], today: date | None = None) -> list[Subscriber]:
    """Ordered work queue — who to reply to first."""
    return sorted(subs, key=lambda s: priority_score(s, today), reverse=True)


# --- Non-explicit message drafting -----------------------------------------

def draft_reply(s: Subscriber, intent: str) -> str:
    """Neutral, non-sexual draft copy only."""
    name = s.handle.lstrip("@")
    if intent == "welcome":
        return (f"Hey {name}! Thanks for subscribing 💛 Just so it's clear, I'm "
                f"an AI-generated character — hope you enjoy the content!")
    if intent == "upsell":
        nxt = Tier(min(int(s.tier) + 1, int(Tier.VIP)))
        return (f"Hey {name}, wanted to let you know Tier {int(nxt)} unlocks "
                f"more — first access to new sets and priority replies. Let me "
                f"know if you'd like details.")
    if intent == "retention":
        return (f"Hey {name}, haven't seen you in a bit — new sets just dropped. "
                f"Come say hi whenever!")
    if intent == "vip_checkin":
        return (f"Hey {name} 💛 You're one of my top supporters — you're first in "
                f"line for the next drop. Anything you'd like to see next?")
    raise ValueError(f"unknown intent: {intent!r}")


# --- Persistence ------------------------------------------------------------

def load(path: str) -> list[Subscriber]:
    with open(path) as f:
        raw = json.load(f)
    return [Subscriber(**{**r, "tier": Tier(r.get("tier", 0))}) for r in raw]


def save(path: str, subs: list[Subscriber]) -> None:
    with open(path, "w") as f:
        json.dump([{**asdict(s), "tier": int(s.tier)} for s in subs], f, indent=2)


# --- Demo / CLI -------------------------------------------------------------

def _demo() -> None:
    today = date.today()
    subs = [
        Subscriber("@bigfan", "fansly", Tier.VIP, 480.0,
                   last_contact=today.isoformat()),
        Subscriber("@newbie", "fansly", Tier.T1, 9.99, last_contact=""),
        Subscriber("@lurker", "reddit", Tier.FREE, 0.0),
        Subscriber("@steady", "fansly", Tier.T2, 149.94,
                   last_contact="2000-01-01"),
    ]
    print("Work queue (top = attend first):\n")
    for s in queue(subs, today):
        flag = "VIP" if s.is_vip else f"T{int(s.tier)}"
        print(f"  [{flag:>3}] {s.handle:<10} LTV ${s.lifetime_value:>7,.2f} "
              f"score {priority_score(s, today):>7.1f}")
    print("\nSample VIP check-in draft:")
    print("  " + draft_reply(subs[0], "vip_checkin"))


def main() -> None:
    p = argparse.ArgumentParser(description="AI-creator subscriber CRM")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    args = p.parse_args()
    if args.cmd == "demo":
        _demo()


if __name__ == "__main__":
    main()
