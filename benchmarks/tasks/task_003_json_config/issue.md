# JSON config file fails to load

Hey, I just tried switching one of our service configs from YAML to JSON (we're standardizing on JSON across the team) and got this error:

```
ValueError: JSON config loading is not implemented yet: config/app.json
```

I was under the impression JSON was already supported — the function signature for `load_config()` lists `.json` as a supported extension. I double-checked and my file is valid JSON:

```json
{
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "logging": {
    "level": "info"
  }
}
```

Loading the same settings from a `.yaml` file works fine, so it's specifically something with how JSON files are handled.

Would be great to get this fixed since we have a few more services to migrate over the next sprint.
