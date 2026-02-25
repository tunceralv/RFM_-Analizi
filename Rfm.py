import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def Rfm_Analiz(regex=False):
    pd.set_option('display.max_columns',50)
    pd.set_option('display.float_format',lambda x:'%.3f'%x)
    data=pd.read_excel("yours FilePath",sheet_name="Year 2010-2011")
    df=pd.DataFrame(data)

    print(f"Boyut Bilgisi: {df.shape}\n")
    print(f"Eksik Degerler:\n*****\n{df.isnull().sum()}\n")
    print(f"Ürün Özelinde eşşiz değerler:\n*****\n{df["Description"].nunique()}\n")
    print(f"En cok satan ürünler:\n*****\n{df["Description"].value_counts().head}")
    print(f"Fatura Özelinde eşşiz değerler:\n*****\n{df["Invoice"].nunique()}\n")

    df["Toplam_Ucret"]=(df["Quantity"]*df["Price"])
    #df.groupby(["Invoice"]).agg({"Toplam_Ucret":"sum"})
    df.groupby(["Description"]).agg({"Toplam_Ucret":"sum"})

    df.dropna(inplace=True)
    print(f"Eksik Degerler:\n*****\n{df.isnull().sum()}\n")
    #İade işlemlerini silme
    df=df[~df["Invoice"].str.contains("C",na=False)]

    df.groupby(["Description"]).agg({"Toplam_Ucret":"sum"})


    analiz_tarihi=df["InvoiceDate"].max()+pd.Timedelta(days=1)
    rfm=df.groupby("Customer ID").agg({"InvoiceDate":lambda date:(analiz_tarihi-date.max()).days,
                                    "Invoice": lambda num: num.nunique(),
                                    "Toplam_Ucret": lambda toplam_ucret:toplam_ucret.sum()})


    rfm.columns=["Recency","Frequency","Monetary"]

    rfm.describe().T
    #monetary de cıkan 0 degerini yok etmeliyiz

    rfm = rfm[rfm["Monetary"]>0]

    rfm["recency_score"]=pd.qcut(rfm["Recency"].rank(method="first"),
                             5,
                             labels=[5,4,3,2,1])
    rfm["frequency_score"]=pd.qcut(rfm["Frequency"].rank(method="first"),
                                5,
                                labels=[1,2,3,4,5])
    rfm["monetary_score"]=pd.qcut(rfm["Monetary"].rank(method="first"),
                                5,
                                labels=[1,2,3,4,5])

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    rfm["RFM_SCORES"]=(rfm["recency_score"].astype(str)+rfm["frequency_score"].astype(str))
  
    #rfm isimlendirmeleri
    seg_map= {
        r'[1-2][1-2]':'hibernating',
        r'[1-2][3-4]':'at_Risk',
        r'[1-2]5':'cant_loose',
        r'3[1-2]':'about_to_sleep',
        r'33':'need_attention',
        r'[3-4][4-5]':'loyal_customers',
        r'41':'promising',
        r'51':'new_customers',
        r'[4-5][2-3]':'potential_loyalists',
        r'5[4-5]':'champions'
    }

    rfm["segment"]=rfm["RFM_SCORES"].replace(seg_map,regex=True)

    print(rfm.head(10))




Rfm_Analiz(regex=True)
