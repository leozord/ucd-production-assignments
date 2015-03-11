import addressbook_pb2

_TIMEOUT_SECONDS = 10


def run():
  with addressbook_pb2.early_adopter_create_AddressBookService_stub('localhost', 50051) as stub:
        request = addressbook_pb2.AddRequest()
        ab = request.addressBook.new()
        person = ab.person.add()
        person.id = 1
        person.name = 'Test'
        response = stub.Add(request, _TIMEOUT_SECONDS)
        print "Response from Server: " + response.message


if __name__ == '__main__':
  run()
