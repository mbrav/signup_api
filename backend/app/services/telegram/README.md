## Aiogram + FastAPI integration with webhooks

### Ngrok usage:

Register new auth token:

```bash
ngrok authtoken y0uR-Tok3en
```

Start new proxy where 8000 is the port of FastAPI:

```bash
ngrok http -region=eu 8000
```

Add "Forwarding" https address to `WEBHOOK_HOST` variable in settings
