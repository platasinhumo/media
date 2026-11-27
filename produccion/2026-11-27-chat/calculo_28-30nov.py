# Día 28: carro nuevo vs usado 3 años, 100% financiado 60 meses al 1,4% mensual
def pmt(P,r,n): return P*r/(1-(1+r)**-n)
def interes_total(P,r,n): return pmt(P,r,n)*n-P
nuevo=15000; usado=nuevo*0.8*0.85*0.85
def valor(v0, edad0, años):
    v=v0
    for a in range(edad0+1, edad0+años+1):
        v*= 0.8 if a==1 else 0.85
    return v
for nom,p,e in [("nuevo",nuevo,0),("usado",usado,3)]:
    i=interes_total(p,0.014,60); dep=p-valor(p,e,5); print(nom, round(p), "cuota",round(pmt(p,0.014,60)),"int",round(i),"dep",round(dep),"total",round(i+dep))
# Día 29
r=1.08**(1/12)-1
fv=lambda n: 8*((1+r)**n-1)/r
print("cajero anual",8*12,"10a",round(fv(120)),"20a",round(fv(240)),"aportes10",8*120)
# Día 30
def deuda(compras):
    b=2000; pag=0; it=0
    for m in range(24):
        b+=compras
        intm=b*0.025; it+=intm; b+=intm  # supuesto 1
        p=max(0.03*b,40); p=min(p,b); b-=p; pag+=p
    return round(b),round(pag),round(it)
print("con compras",deuda(100),"sin",deuda(0))
