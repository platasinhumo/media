import itertools
T=(4040,2159,1799); T0=1773
def sim(order, compras, months, minref, skip_first_pay):
    b=2000; pag=0; it=0
    for m in range(months):
        start=b
        for step in order:
            if step=="c": b+=compras
            elif step=="i":
                x=b*0.025; it+=x; b+=x
            elif step=="p":
                if skip_first_pay and m==0: continue
                base = start if minref=="start" else b
                p=min(max(0.03*base,40),b); b-=p; pag+=p
    return round(b),round(pag),round(it)
for o in itertools.permutations("cip"):
  for months in (23,24,25):
    for mr in ("start","cur"):
      for sk in (False,True):
        a=sim(o,100,months,mr,sk); z=sim(o,0,months,mr,sk)
        if abs(a[0]-T[0])<=6 and abs(z[0]-T0)<=6: print("".join(o),months,mr,sk,a,z)
