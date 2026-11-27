# 1-dic: préstamo en app $100 a 15 días, cobra $15 (interés + "tecnología/aval")
P=100; c=15; d=15
r15=c/P; anual=(1+r15)**(365/d)-1
tar=P*((1.025)**(15/30.4)-1)   # misma plata con tarjeta al 2,5 % mensual, 15 días
print("app costo",c,"15d %",r15*100,"EA %",round(anual*100), "tarjeta 15d",round(tar,2))
# si lo renueva 4 veces (2 meses)
print("renovando 2 meses (4x15d) costo", c*4)
# 2-dic: suscripciones olvidadas
subs=[10,8,13]; m=sum(subs); print("mes",m,"año",m*12,"3 años",m*36)
# 3-dic: crédito $5.000, 36 meses, 1,8 % mensual + seguro voluntario $12/mes
def pmt(P,r,n): return P*r/(1-(1+r)**-n)
c0=pmt(5000,0.018,36); c1=c0+12
# tasa equivalente con el seguro
lo,hi=0.0,0.1
for _ in range(100):
    mid=(lo+hi)/2
    if pmt(5000,mid,36)<c1: lo=mid
    else: hi=mid
print("cuota",round(c0,2),"con seguro",round(c1,2),"seguro total",12*36,"tasa equiv mensual %",round(mid*100,2), "EA sin",round(((1.018)**12-1)*100,1),"EA con",round(((1+mid)**12-1)*100,1))
# 4-dic: remesa $200/mes
a_fee=8; a_spread=0.03*200; b_fee=2; b_spread=0.005*200
A=a_fee+a_spread; B=b_fee+b_spread
print("A",A,"B",B,"año A",A*12,"año B",B*12,"dif año",(A-B)*12, "% A",A/200*100)
