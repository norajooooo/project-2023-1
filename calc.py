import add_mul
import sub_div

a=int(input())
b=int(input())

c=input('add? sub? mul? div?')
if c=='add':
    print('%d + %d = %d' %(a,b,add_mul.add(a,b)))