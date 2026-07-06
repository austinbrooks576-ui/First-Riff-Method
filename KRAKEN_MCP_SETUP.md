# Kraken MCP Connection Setup

This repo ships a project-level MCP configuration (`.mcp.json`) that connects
Claude Code to the Kraken exchange for the trade bot. Because cloud sessions
run in ephemeral containers, the connection is defined here in the repo so it
re-establishes automatically every time a session starts — no manual setup
per session.

## What it configures

The `kraken` MCP server runs [`mcp-kraken`](https://pypi.org/project/mcp-kraken/)
(installed on demand via `uvx` from PyPI) over stdio. It exposes ~54 tools for
the Kraken Spot REST API, including:

- **Market data (no credentials needed):** ticker, OHLC, order book, recent
  trades, asset pairs, system status
- **Account (credentials required):** balances, trade balance, ledgers,
  open/closed orders, trade history
- **Trading (credentials required):** add/edit/amend/cancel orders, batch
  orders
- **Funding (credentials required):** deposit/withdrawal methods, addresses,
  and status

## Providing credentials

Private endpoints need a Kraken API key. **Never commit keys to this repo.**
Set them as environment variables:

- `KRAKEN_API_KEY` — your Kraken API public key
- `KRAKEN_API_SECRET` — your Kraken API private key (base64)

For Claude Code on the web, add both variables to the session environment:
**claude.ai/code → your environment → Environment variables**. Locally,
export them in your shell before starting Claude Code.

Create keys at kraken.com → **Settings → API**. For the trade bot, grant only
**Query Funds**, **Query Orders/Trades**, and **Create & Modify Orders**.
Leave **Withdraw Funds** disabled — the bot never needs it, and it limits
damage if a key leaks.

Without credentials, the server still starts and the public market-data tools
work; private tools return an auth error until the variables are set.

## Verifying the connection

In a Claude Code session, run `/mcp` to confirm the `kraken` server is
connected, or ask Claude to call `get_system_status` (public) and
`get_account_balance` (private) as a smoke test.

## Alternative: official Kraken CLI (local machines)

Kraken also ships an official CLI with a built-in MCP server
([krakenfx/kraken-cli](https://github.com/krakenfx/kraken-cli)):

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/krakenfx/kraken-cli/releases/latest/download/kraken-cli-installer.sh | sh
claude mcp add kraken -- kraken mcp -s market,account,paper
```

It supports futures, staking, WebSocket streaming, and paper trading. It is
not used in `.mcp.json` because cloud sessions for this repo cannot download
GitHub release binaries from other repositories; on a local machine it is a
good option.

## Security note

`mcp-kraken` is a community package (not affiliated with Kraken). It signs
requests locally and sends credentials only to `api.kraken.com`, but as with
any third-party dependency handling exchange keys: pin versions if you need
reproducibility, review updates, and keep withdrawal permission off the key.
