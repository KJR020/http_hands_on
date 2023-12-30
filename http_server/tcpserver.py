import socket


class TCPServer:
    """
    TCP Server class
    """

    def serve(self):
        print("TCP Server is running...")

        try:
            # socketの作成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # socketをlocalhostのポート8080番に割り当てる
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # 外部からの接続をまち、接続があったらコネクションを確率する
            print("Waiting for connection...")
            (client_socket, address) = server_socket.accept()
            print("Connection established with: ", address)

            # クライアントから送られて生きたデータを取得する
            request = client_socket.recv(4096)
            # 4096って何?

            # クライアントから送られてきたデータをファイルに書き出す
            with open("server_recv.txt", "wb") as f:
                f.write(request)

            # 通信完了
            client_socket.close()

        finally:
            print("TCP Server is stopped...")


if __name__ == "__main__":
    server = TCPServer()
    server.serve()
