
# Create your tests here.
QAPL = {'QAPL': 'NAME1'}
EPL = {'EPL': 'NAME2'}
direct = (lambda *args: args)(QAPL, EPL)
print(direct)
for item in direct:
    key=item.keys()
    print(str(key))
