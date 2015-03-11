__author__ = 'elerafa'

import time

import addressbook_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class AddressBookServer(addressbook_pb2.EarlyAdopterAddressBookServiceServicer):

  def Find(self, request, context):
      pass

  def List(self, request, context):
      pass

  def Add(self, request, context):
      print("REQUEST RECEIVED")
      print(request.SerializeToString())
      print("REQUEST ENDED")


def serve():
  server = addressbook_pb2.early_adopter_create_AddressBookService_server(
      AddressBookServer(), 50051, None, None)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop()

if __name__ == '__main__':
  serve()
