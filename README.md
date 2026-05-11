# Claude Skills

## Install

In a terminal, run:

```bash
claude plugin marketplace add zyte-ai/claude-skills
claude plugin install zyte-web-data@zyte-ai
```

If you have an open session in some other terminal, run:

```bash
/reload-plugins
```

## Update

We recommend that you enable automatic updates: 

1.  Enter `/plugin` on a Claude Code session
2.  Select **Marketplaces** → **zyte** → **Enable auto-update**.

To update manually, update the marketplace:

```bash
claude plugin marketplace update zyte-ai/claude-skills
```

And then, in a Claude Code session, run:

```bash
/reload-plugins
```

See also: https://code.claude.com/docs/en/discover-plugins.md

## Usage

The web scraping skills are designed to support any web scraping prompt, and be
picked up automatically.

For example:

> Scrape https://books.toscrape.com/

## Evaluation

We automatically evaluate skills and track both wall time and cost; we measure
and aim to improve these metrics over time.

## Feedback

If you find any issue, such as prompts that did not work as expected, or
cause excessive wall time or cost, please open a GitHub issue.

Try to provide as much information as possible for us to be able to reproduce
your issue, even if you prefer to annonimize target websites or other data.
