from aiwork.api import server


def test_api_main_uses_cli_arguments(monkeypatch):
    called = {}

    def fake_start_server(host="127.0.0.1", port=5000, debug=False, auto_port=False):
        called["host"] = host
        called["port"] = port
        called["debug"] = debug
        called["auto_port"] = auto_port

    monkeypatch.setattr(server, "start_server", fake_start_server)

    server.main(["--host", "127.0.0.1", "--port", "8081", "--debug", "--auto-port"])

    assert called == {
        "host": "127.0.0.1",
        "port": 8081,
        "debug": True,
        "auto_port": True,
    }


def test_build_parser_defaults():
    args = server.build_parser().parse_args([])

    assert args.host == "127.0.0.1"
    assert args.port == 5000
    assert args.debug is False
    assert args.auto_port is False


def test_server_defaults_to_loopback(monkeypatch):
    called = {}
    monkeypatch.setattr(server, "is_port_available", lambda port, host: True)
    monkeypatch.setattr(server.app, "run", lambda **kwargs: called.update(kwargs))
    server.start_server()
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 5000
