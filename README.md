# tcprelay

`tcprelay` is a small tool that acts as a TCP relay, except it keeps a copy of all messages for itself. This tool was designed to help me reverse-engineer a closed game protocol.

## Usage

To use, clone this repo and run:

```sh
python3 -m tcprelay [remote host address] [remote host port] [local port]
```

As soon as a client connects to the `tcprelay` server, a new connection will be opened to the remote host. server -> client and client -> server communications are handled asynchronously.