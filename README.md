# uk-send
___
Send a heartbeat to [uptime kuma](https://github.com/louislam/uptime-kuma) in a separate thread without blocking the main program.

## Examples:
### Base usage
```python
import uk_send as uk

url = "https://uk.example.xom/api/push/YhYAt5t6qiRJ60b16g8326vAGYQw7Ty0"

uk.send("test message", url=url)
```
### Env usage
```
UK_URL="https://uk.example.xom/api/push/YhYAt5t6qiRJ60b16g8326vAGYQw7Ty0"
UK_PROXY="http://127.0.0.1:1080"
```
```python
import uk_send as uk

uk.send("test message")
```

## Defaults:
```python
import uk_send as uk

url = "https://uk.example.xom/api/push/YhYAt5t6qiRJ60b16g8326vAGYQw7Ty0"

uk.send(
    msg="test message",              # default ""
    url=url,                         # required
    ping=1,                          # default 1
    status="up",                     # default "up"
    proxy="http://127.0.0.1:1080",   # default None
)
```

## Options:
- uk-send - Base module, uses standart urllib module. No additional dependences. 
- uk-send[requests] - Uses requests module.
- uk-send[httpx] - Uses httpx module.
- uk-send[requests-socks] - Uses request module. Supports socks5 proxy.
- uk-send[httpx-socks] - Uses httpx module. Supports sosks5 proxy.


## Priority
### Send modules:
The uk-send module uses modules in the next priority if they are available:
#### No-proxy or http-proxy:
1. httpx
2. requests
3. urllib
#### Socks-proxy:
1. httpx[socks]
2. requests[socks]
3. ERROR
### Parameters
#### URL:
1. function argument
2. env
#### Proxy:
1. function argument
2. env
#### Message:
1. function argument
2. url parameter
3. default ("")
#### Status:
1. function argument
2. url parameter
3. default ("up")
#### Ping:
1. function argument
2. url parameter
3. default (1)