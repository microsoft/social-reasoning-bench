# SAGE Protocol

Run protocols in a Magentic-Marketplace server.

Current protocols:

- [messenger](sage_protocol/messenger/README.md)
- [calendar](sage_protocol/calendar/README.md)
- [marketplace](sage_protocol/marketplace/README.md)

## Quick Start

To launch all protocols in a single server (recommended):

```
uv run -m sage_protocol
```

Or run an individual protocol:

```
uv run -m sage_protocol.messenger
uv run -m sage_protocol.marketplace
uv run -m sage_protocol.calendar
```

## Server

To talk to other tinyPAs, we need a remote server. We are currently hosting one on GCR.

Make sure you are connected to VPN to use, then install the sage apps. During onboarding be sure to specify your server URL:

http://gcr-sandbox-017.redmond.corp.microsoft.com:5000
