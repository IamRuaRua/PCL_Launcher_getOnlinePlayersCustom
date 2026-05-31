from __future__ import annotations

from pathlib import Path

from flask import Flask, Response, jsonify, request, send_file
from mcstatus import JavaServer

from layout_generator import PlayerLayoutRenderer

DEFAULT_OUTPUT_PATH = Path("Custom.xaml")
QUERY_FAILED_TEXT = "服务器信息获取失败"


class MissingServerParameterError(ValueError):
    pass


def fetch_players(server_address: str) -> list[str]:
    server = JavaServer.lookup(server_address)
    status = server.status()
    sample = status.players.sample or []
    return [player.name for player in sample]


def render_xaml(server_address: str) -> str:
    renderer = PlayerLayoutRenderer()
    return renderer.render(fetch_players(server_address))


def render_query_failed_xaml() -> str:
    renderer = PlayerLayoutRenderer()
    return renderer.render([], empty_text=QUERY_FAILED_TEXT)


def update_xaml_file(server_address: str, output_path: str | Path = DEFAULT_OUTPUT_PATH) -> Path:
    renderer = PlayerLayoutRenderer()
    path = Path(output_path)
    renderer.write(fetch_players(server_address), path)
    return path


def create_app() -> Flask:
    app = Flask(__name__)

    def get_server_arg() -> str:
        server_address = request.args.get("server", "").strip()
        if not server_address:
            raise MissingServerParameterError("missing server parameter")
        return server_address

    @app.get("/onlineplayers")
    def xaml_api() -> Response:
        try:
            server_address = get_server_arg()
            xaml = render_xaml(server_address)
            return Response(xaml, mimetype="application/xml")
        except MissingServerParameterError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            return Response(render_query_failed_xaml(), mimetype="application/xml")

    @app.get("/Custom.xaml")
    def xaml_file() -> Response:
        try:
            server_address = get_server_arg()
            output_path = update_xaml_file(server_address)
            if request.args.get("download") == "1":
                return send_file(output_path, mimetype="application/xml", as_attachment=True, download_name="Custom.xaml")
            return Response(output_path.read_text(encoding="utf-8"), mimetype="application/xml")
        except MissingServerParameterError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            return Response(render_query_failed_xaml(), mimetype="application/xml")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678)
