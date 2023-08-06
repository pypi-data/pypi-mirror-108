from traceback import format_exc


def broadcast_sending(connections_list, data):
    """ Рассылает данные data по всем подключенным клиентам connections_list (список,содержащий словари,
    где ключом является connection (возвращаемый методом server.accept()), а значением - разная информация о
    соединении, не играющая роль в этом контексте """
    for connection in connections_list:
        for connection_key, connections_details in connection.items():
            try:
                self.send_data(connection_key, data)
            except:
                print(format_exc())