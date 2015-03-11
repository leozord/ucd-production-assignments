__author__ = 'elerafa'

import time

import addressbook_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class AddressBookServer(addressbook_pb2.EarlyAdopterAddressBookServiceServicer):

  def __init__(self):
    self.data = []

  def Find(self, request, context):
      print("FIND request received")
      result = []
      for ab in self.data:
        for p in ab.person:
          if str(p.name.lower()).find(request.name.lower()) != 0:
            result.append(ab)
            break
      response = addressbook_pb2.FindResponse()
      for ab in result:
        response.addressBook._values.append(ab)
      return response

  def List(self, request, context):
      print("LIST request received")
      response = addressbook_pb2.ListResponse()
      for ab in self.data:
        response.addressBook._values.append(ab)
      return response

  def Add(self, request, context):
      print("ADD request received")
      for ab in request.addressBook:
        self.data.append(ab)
      responseMessage="Added succesfully. Number of Address Books: " + str(len(self.data))
      response = addressbook_pb2.AddResponse()
      response.response = responseMessage
      return response


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
