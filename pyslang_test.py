import pyslang
tree = pyslang.SyntaxTree.fromFile('test.sv')
mod = tree.root.members[0]
# print(mod.header.name.value)
# print(type(mod.header.ports))
counter =0
# for port in mod.header.ports:
#     print(port)
#     print(counter)
#     counter = counter + 1
# print()
print(type(tree.root.members[0]))
for member in tree.root.members[0]:
    print(type(member))
    print(member)
    print(counter)
    counter = counter + 1
# print(type(tree.root.members[1]))

for port in mod.header.ports[1]:
    print(port)
    print(counter)
    