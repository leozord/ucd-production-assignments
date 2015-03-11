__author__ = 'elerafa'

import addressbook_pb21
person = addressbook_pb21.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phone.add()
phone.number = "555-4321"
phone.type = addressbook_pb21.Person.HOME
addressbook = addressbook_pb21.AddressBook()
person1 = addressbook.person.add()
person1.id = 1
person1.name = 'Person 1'
person2 = addressbook.person.add()
person2.name = 'Person 2'
person2.id = 2


print(addressbook.SerializeToString())
