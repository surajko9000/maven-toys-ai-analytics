import sys, json, pandas as pd
D=sys.argv[1]
s=pd.read_csv(f"{D}/sales.csv",parse_dates=["Date"]); p=pd.read_csv(f"{D}/products.csv"); st=pd.read_csv(f"{D}/stores.csv"); inv=pd.read_csv(f"{D}/inventory.csv")
for c in ("Product_Cost","Product_Price"): p[c]=p[c].str.replace(r"[$ ]","",regex=True).astype(float)
st["Store_City"]=st.Store_City.replace({"Cuidad de Mexico":"Ciudad de Mexico"})
st["Store_Name"]=st.Store_Name.str.replace("Cuidad","Ciudad")
s["mi"]=(s.Date.dt.year-2022)*12+s.Date.dt.month-1
smp=s.groupby(["Store_ID","Product_ID","mi"]).Units.sum().reset_index()
out={"P":[dict(id=int(r.Product_ID),name=r.Product_Name,cat=r.Product_Category,cost=r.Product_Cost,price=r.Product_Price) for r in p.itertuples()],
"ST":[dict(id=int(r.Store_ID),name=r.Store_Name,city=r.Store_City,loc=r.Store_Location) for r in st.itertuples()],
"SMP":smp.values.tolist(),"INVS":inv.values.tolist()}
print(json.dumps(out,separators=(",",":")))
