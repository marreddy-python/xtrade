li = [[200, 100], [300, 234], [400, 131]]
import operator

a = sorted(li, key=operator.itemgetter(0))  
b = sorted(li, key=operator.itemgetter(0), reverse=True)  

print a 
print b


dict = {
        'a':None,
        'b':"name"
}
list = []
for x in range(0, 0):
       dict['a'] = x
       list.append(dict)
       dict = {
               'a':None,
               'b':'name'
       }

print list

lis = [{ "name" : "Nandini", "age" : 20},  
{ "name" : "Manjeet", "age" : 20 }, 
{ "name" : "Nikhil" , "age" : 19 }] 


print sorted(lis, key = lambda i: i['age']) 

a = 1.2345
a = round(a,2)
print a 

a = [{'x': 1567172040000, 'text': 'Buy', 'title': 'B'}, {'x': 1567174560000, 'text': 'Buy', 'title': 'B'}, {'x': 1567175580000, 'text': 'Buy', 'title': 'B'}, {'x': 1567176420000, 'text': 'Buy', 'title': 'B'}, {'x': 1567180920000, 'text': 'Buy', 'title': 'B'}, {'x': 1567185060000, 'text': 'Buy', 'title': 'B'}, {'x': 1567187040000, 'text': 'Buy', 'title': 'B'}, {'x': 1567190100000, 'text': 'Buy', 'title': 'B'}, {'x': 1567192800000, 'text': 'Buy', 'title': 'B'}, {'x': 1567195680000, 'text': 'Buy', 'title': 'B'}, {'x': 1567517580000, 'text': 'Buy', 'title': 'B'}, {'x': 1567519380000, 'text': 'Buy', 'title': 'B'}, {'x': 1567523520000, 'text': 'Buy', 'title': 'B'}, {'x': 1567526700000, 'text': 'Buy', 'title': 'B'}, {'x': 1567540860000, 'text': 'Buy', 'title': 'B'}, {'x': 1567545000000, 'text': 'Buy', 'title': 'B'}, {'x': 1567585020000, 'text': 'Buy', 'title': 'B'}, {'x': 1567604100000, 'text': 'Buy', 'title': 'B'}, {'x': 1567606380000, 'text': 'Buy', 'title': 'B'}, {'x': 1567613940000, 'text': 'Buy', 'title': 'B'}, {'x': 1567701000000, 'text': 'Buy', 'title': 'B'}, {'x': 1567713180000, 'text': 'Buy', 'title': 'B'}, {'x': 1567774680000, 'text': 'Buy', 'title': 'B'}, {'x': 1567777080000, 'text': 'Buy', 'title': 'B'}, {'x': 1567779120000, 'text': 'Buy', 'title': 'B'}, {'x': 1567785480000, 'text': 'Buy', 'title': 'B'}, {'x': 1567788540000, 'text': 'Buy', 'title': 'B'}, {'x': 1567799520000, 'text': 'Buy', 'title': 'B'}, {'x': 1568036040000, 'text': 'Buy', 'title': 'B'}, {'x': 1568037360000, 'text': 'Buy', 'title': 'B'}, {'x': 1568043840000, 'text': 'Buy', 'title': 'B'}, {'x': 1568045340000, 'text': 'Buy', 'title': 'B'}, {'x': 1568049780000, 'text': 'Buy', 'title': 'B'}, {'x': 1568052660000, 'text': 'Buy', 'title': 'B'}, {'x': 1568122920000, 'text': 'Buy', 'title': 'B'}, {'x': 1568127480000, 'text': 'Buy', 'title': 'B'}, {'x': 1568129880000, 'text': 'Buy', 'title': 'B'}, {'x': 1568131500000, 'text': 'Buy', 'title': 'B'}, {'x': 1568138700000, 'text': 'Buy', 'title': 'B'}, {'x': 1568141340000, 'text': 'Buy', 'title': 'B'}, {'x': 1568192880000, 'text': 'Buy', 'title': 'B'}, {'x': 1568224440000, 'text': 'Buy', 'title': 'B'}, {'x': 1568230440000, 'text': 'Buy', 'title': 'B'}, {'x': 1568243520000, 'text': 'Buy', 'title': 'B'}, {'x': 1568275260000, 'text': 'Buy', 'title': 'B'}, {'x': 1568285940000, 'text': 'Buy', 'title': 'B'}, {'x': 1568285940000, 'text': 'Buy', 'title': 'B'}, {'x': 1568285940000, 'text': 'Buy', 'title': 'B'}, {'x': 1568380140000, 'text': 'Buy', 'title': 'B'}, {'x': 1568381580000, 'text': 'Buy', 'title': 'B'}, {'x': 1568388660000, 'text': 'Buy', 'title': 'B'}, {'x': 1568391840000, 'text': 'Buy', 'title': 'B'}, {'x': 1568396580000, 'text': 'Buy', 'title': 'B'}, {'x': 1568401680000, 'text': 'Buy', 'title': 'B'}, {'x': 1568620860000, 'text': 'Buy', 'title': 'B'}, {'x': 1568624580000, 'text': 'Buy', 'title': 'B'}, {'x': 1568631420000, 'text': 'Buy', 'title': 'B'}] 

b = [{'x': 1567173360000, 'text': 'Sell', 'title': 'S'}, {'x': 1567175400000, 'text': 'Sell', 'title': 'S'}, {'x': 1567175760000, 'text': 'Sell', 'title': 'S'}, {'x': 1567179000000, 'text': 'Sell', 'title': 'S'}, {'x': 1567181640000, 'text': 'Sell', 'title': 'S'}, {'x': 1567186200000, 'text': 'Sell', 'title': 'S'}, {'x': 1567187520000, 'text': 'Sell', 'title': 'S'}, {'x': 1567191180000, 'text': 'Sell', 'title': 'S'}, {'x': 1567193280000, 'text': 'Sell', 'title': 'S'}, {'x': 1567196700000, 'text': 'Sell', 'title': 'S'}, {'x': 1567517760000, 'text': 'Sell', 'title': 'S'}, {'x': 1567520400000, 'text': 'Sell', 'title': 'S'}, {'x': 1567524360000, 'text': 'Sell', 'title': 'S'}, {'x': 1567527300000, 'text': 'Sell', 'title': 'S'}, {'x': 1567541400000, 'text': 'Sell', 'title': 'S'}, {'x': 1567546440000, 'text': 'Sell', 'title': 'S'}, {'x': 1567586400000, 'text': 'Sell', 'title': 'S'}, {'x': 1567605720000, 'text': 'Sell', 'title': 'S'}, {'x': 1567606920000, 'text': 'Sell', 'title': 'S'}, {'x': 1567614720000, 'text': 'Sell', 'title': 'S'}, {'x': 1567701480000, 'text': 'Sell', 'title': 'S'}, {'x': 1567714500000, 'text': 'Sell', 'title': 'S'}, {'x': 1567775340000, 'text': 'Sell', 'title': 'S'}, {'x': 1567777800000, 'text': 'Sell', 'title': 'S'}, {'x': 1567779420000, 'text': 'Sell', 'title': 'S'}, {'x': 1567786260000, 'text': 'Sell', 'title': 'S'}, {'x': 1567789200000, 'text': 'Sell', 'title': 'S'}, {'x': 1567800000000, 'text': 'Sell', 'title': 'S'}, {'x': 1568037060000, 'text': 'Sell', 'title': 'S'}, {'x': 1568038020000, 'text': 'Sell', 'title': 'S'}, {'x': 1568044680000, 'text': 'Sell', 'title': 'S'}, {'x': 1568047560000, 'text': 'Sell', 'title': 'S'}, {'x': 1568050680000, 'text': 'Sell', 'title': 'S'}, {'x': 1568053560000, 'text': 'Sell', 'title': 'S'}, {'x': 1568123760000, 'text': 'Sell', 'title': 'S'}, {'x': 1568128140000, 'text': 'Sell', 'title': 'S'}, {'x': 1568130480000, 'text': 'Sell', 'title': 'S'}, {'x': 1568132040000, 'text': 'Sell', 'title': 'S'}, {'x': 1568139540000, 'text': 'Sell', 'title': 'S'}, {'x': 1568141760000, 'text': 'Sell', 'title': 'S'}, {'x': 1568196120000, 'text': 'Sell', 'title': 'S'}, {'x': 1568224740000, 'text': 'Sell', 'title': 'S'}, {'x': 1568231400000, 'text': 'Sell', 'title': 'S'}, {'x': 1568243820000, 'text': 'Sell', 'title': 'S'}, {'x': 1568276760000, 'text': 'Sell', 'title': 'S'}, {'x': 1568285940000, 'text': 'Sell', 'title': 'S'}, {'x': 1568285940000, 'text': 'Sell', 'title': 'S'}, {'x': 1568285940000, 'text': 'Sell', 'title': 'S'}, {'x': 1568285940000, 'text': 'Sell', 'title': 'S'}, {'x': 1568380800000, 'text': 'Sell', 'title': 'S'}, {'x': 1568381760000, 'text': 'Sell', 'title': 'S'}, {'x': 1568389500000, 'text': 'Sell', 'title': 'S'}, {'x': 1568392680000, 'text': 'Sell', 'title': 'S'}, {'x': 1568397060000, 'text': 'Sell', 'title': 'S'}, {'x': 1568402880000, 'text': 'Sell', 'title': 'S'}, {'x': 1568621760000, 'text': 'Sell', 'title': 'S'}, {'x': 1568625300000, 'text': 'Sell', 'title': 'S'}]

print len(a)

print len(b)