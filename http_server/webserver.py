import socket
from datetime import datetime
from pathlib import Path


class WebServer:
    BASE_DIR = Path(__file__).parent.resolve()
    STATIC_ROOT = BASE_DIR / "static"

    def serve(self):
        print("Starting web server...")

        try:
            # create socket
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # socketをlocalhostのポート8080番に割り当てる
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # 外部からの接続を待ち、接続があったらコネクションを確立する
            print("Waiting for connection...")
            (client_socket, address) = server_socket.accept()
            print("Connected to: ", address)

            # クライアントから送られてきたデータを取得する
            request = client_socket.recv(4096)

            # requestをパース
            # 1. request_line
            # 2. request_header
            # 3. request_body
            # に分割する
            request_line, remain = request.split(b"\r\n", maxsplit=1)
            request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

            # request_lineをパースする
            method, path, http_version = request_line.decode().split(" ")

            # pathの先頭の/を削除し、相対パスにしておく
            relative_path = path.lstrip("/")
            # filepathを作成する
            static_filepath = self.STATIC_ROOT / relative_path

            # ファイルからレスポンスボディを生成
            try:
                with open(static_filepath, "rb") as f:
                    response_body = f.read()

                # レスポンスラインを作成する
                response_line = "HTTP/1.1 200 OK\r\n"

            except OSError:
                # ファイルが見つからなかった場合は、404 Not Foundを返す
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_line = "HTTP/1.1 404 Not Found\r\n"

            # レスポンスヘッダーを作成する
            response_header = ""
            response_header += (
                f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            )
            response_header += "Host: HenaServer/0.1\r\n"
            response_header += "Connection: close\r\n"
            response_header += "Content-Type: text/html\r\n"

            # ヘッダーとボディを空行でくっつけた上でbytesに変換し、レスポンス全体を生成する
            response = (
                response_line + response_header + "\r\n"
            ).encode() + response_body

            # クライアントへレスポンスを送信する
            client_socket.send(response)

            # 通信を終了させる
            client_socket.close()

        finally:
            print("Stopping web server...")


if __name__ == "__main__":
    server = WebServer()
    server.serve()
