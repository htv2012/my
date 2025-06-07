# Names and UIDs

```
00000000-0000-0000-0000-000000000001 f5-caching-v1
00000000-0000-0000-0000-000000000002 f5-dns-v1
00000000-0000-0000-0000-000000000003 f5-empty-v1-example
00000000-0000-0000-0000-000000000004 f5-gateway-comments-v1-example
00000000-0000-0000-0000-000000000005 f5-headers-v1
00000000-0000-0000-0000-000000000006 f5-health-monitor-v1
00000000-0000-0000-0000-000000000007 f5-listen-options-v1
00000000-0000-0000-0000-000000000008 f5-load-modules-v1-example
00000000-0000-0000-0000-000000000009 f5-oidc-v1
00000000-0000-0000-0000-00000000000a f5-rate-limiting-v1
00000000-0000-0000-0000-00000000000b f5-rewrite-rules-v1
00000000-0000-0000-0000-00000000000c f5-tls-settings-v1
00000000-0000-0000-0000-00000000000d f5-traffic-settings-v1
00000000-0000-0000-0000-00000000000e f5-waf-v1
```

# POST

Here is a sample request payload for creating a new usecase:

```json
{
    "metadata": {
        "name": "custom-oidc",
        "tags": ["foo"],
        "description": "Updated and improved OIDC implementation"
    },
    "version": "v1.0.0",
    "author": "acme",
    "compatibility": {
        "adm": {
            "min": "v4.0.0"
        },
        "nginx": {
            "modules": [
                {
                    "name": "ngx_http_js_module"
                }
            ],
            "compiledModules": []
        }
    }
}
```

Here is a sample response payload

```json
{
  "author": "acme",
  "compatibility": {
    "adm": {
      "min": "v4.0.0"
    },
    "nginx": {
      "compiledModules": [],
      "modules": [
        {
          "name": "ngx_http_js_module"
        }
      ]
    }
  },
  "environmentRefs": [],
  "files": [
    {
      "path": "README.md",
      "size": "0b"
    },
    {
      "path": "USAGE.md",
      "size": "0b"
    }
  ],
  "metadata": {
    "createTime": "2023-10-03T14:40:42.170194518Z",
    "description": "Updated and improved OIDC implementation",
    "name": "custom-oidc",
    "tags": [
      "foo"
    ],
    "uid": "a6e56fe0-61eb-41b3-adc3-915a20c482fa",
    "updateTime": "2023-10-03T14:40:42.170194518Z"
  },
  "version": "v1.0.0"
}
```
