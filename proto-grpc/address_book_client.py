import addressbook_pb2

_TIMEOUT_SECONDS = 10


def run():
  with addressbook_pb2.early_adopter_create_AddressBookService_stub('localhost', 50051) as stub:
        request = addressbook_pb2.AddRequest()
        ab = request.addressBook.add()
        john = ab.person.add()
        john.id = 1
        john.name = 'John'
        john_phone = john.phone.add()
        john_phone.number = '085 85 12345'
        john_phone.type = 0

        peter = ab.person.add()
        peter.id = 2
        peter.name = 'Peter'
        peter_phone = peter.phone.add()
        peter_phone.number = '123 123 1234'

        print("Inserting address books...")
        response = stub.Add(request, _TIMEOUT_SECONDS)
        print("Response from Server: " + response.response)

        print("Listing all address books")
        request_list = addressbook_pb2.ListRequest()
        response_list = stub.List(request_list, _TIMEOUT_SECONDS)
        print("Response from server: ")
        for ab in response_list.addressBook:
            print(ab)

        print("Listing all address books that starts with Pe")
        request_find = addressbook_pb2.FindRequest()
        request_find.name = 'Pe'
        response_find = stub.Find(request_find, _TIMEOUT_SECONDS)
        print("Response from server: ")
        for ab in response_find.addressBook:
            print(ab)

        print("Done!")

if __name__ == '__main__':
  run()
