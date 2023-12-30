import socket


class TCPClient:
    """
    TCP通信を行うクライアントクラス
    """

    def request(self):
        print("TCP Client is running...")

        try:
            # scoketの作成
            client_socket = socket.socket()
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # serverに接続
            print("Waiting for connection...")
            client_socket.connect(("127.0.0.1", 80))
            print("Connection established!")

            # serverに送信するリクエストを、ファイルから取得する
            with open("client_send.txt", "rb") as f:
                request = f.read()

            # serverにリクエストを送信する
            client_socket.send(request)

            # serverからのレスポンスを取得する
            response = client_socket.recv(4096)

            # responseをファイルに書き出す
            with open("client_recv.txt", "wb") as f:
                f.write(response)

            # 通信完了
            client_socket.close()

        finally:
            print("TCP Client is stopped...")


if __name__ == "__main__":
    client = TCPClient()
    client.request()
