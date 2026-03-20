import pandas as pd, numpy as np, random, datetime as dt

random.seed(42)
np.random.seed(42)

def season_es(date):
    m = date.month
    if m in [12,1,2]:
        return "Verano"
    if m in [3,4,5]:
        return "Otoño"
    if m in [6,7,8]:
        return "Invierno"
    return "Primavera"

countries = {
    "Peru": {"cities": [("Lima","Costa"),("Arequipa","Sierra"),("Trujillo","Costa"),("Cusco","Sierra")], "weight": 0.42},
    "Colombia": {"cities": [("Bogotá","Andina"),("Medellín","Andina"),("Cali","Pacífico"),("Barranquilla","Caribe")], "weight": 0.28},
    "Chile": {"cities": [("Santiago","Centro"),("Valparaíso","Centro"),("Concepción","Sur"),("Antofagasta","Norte")], "weight": 0.18},
    "Mexico": {"cities": [("CDMX","Centro"),("Guadalajara","Occidente"),("Monterrey","Norte"),("Puebla","Centro")], "weight": 0.12},
}
country_list = list(countries.keys())
country_weights = np.array([countries[c]["weight"] for c in country_list])
country_weights = country_weights / country_weights.sum()

segments = ["Premium","Estandar","Basico"]
segment_w = [0.25,0.5,0.25]

categories = {
    "Electronica": {"products": [("Audifonos",120),("Smartwatch",180),("Tablet",350),("Parlante",140)]},
    "Hogar": {"products": [("Licuadora",90),("Aspiradora",220),("Cafetera",130),("Lampara",60)]},
    "Moda": {"products": [("Zapatillas",110),("Chaqueta",150),("Jeans",80),("Bolso",95)]},
    "Deportes": {"products": [("Bicicleta",520),("Guantes",35),("Cuerda",18),("Mancuernas",65)]},
}
channels = ["Online","Tienda"]
channel_w = [0.62,0.38]
campaigns = ["Siempre activo","Back to School","Black Friday","Navidad","Temporada baja"]
campaign_w = [0.55,0.1,0.12,0.13,0.1]

def make_orders(n_rows=9000):
    start = dt.date(2022,1,1)
    end = dt.date(2025,12,31)
    days = (end-start).days + 1
    dates = [start + dt.timedelta(days=int(np.random.randint(0, days))) for _ in range(n_rows)]
    out = []
    for i, d in enumerate(dates):
        country = np.random.choice(country_list, p=country_weights)
        city, region = random.choice(countries[country]["cities"])
        seg = np.random.choice(segments, p=segment_w)
        cat = random.choice(list(categories.keys()))
        prod, base_price = random.choice(categories[cat]["products"])
        channel = np.random.choice(channels, p=channel_w)
        campaign = np.random.choice(campaigns, p=campaign_w)
        units = int(np.random.choice([1,1,1,2,2,3,4,5], p=[0.32,0.14,0.10,0.18,0.10,0.08,0.05,0.03]))

        seg_mult = {"Premium":1.15,"Estandar":1.0,"Basico":0.9}[seg]
        country_mult = {"Peru":1.08,"Colombia":1.0,"Chile":1.05,"Mexico":0.98}[country]
        chan_mult = {"Online":1.0,"Tienda":1.03}[channel]

        season = season_es(d)
        season_mult = {"Verano":1.05,"Otoño":1.0,"Invierno":0.78,"Primavera":1.02}[season]

        disc_base = {"Siempre activo":0.05,"Back to School":0.08,"Black Friday":0.20,"Navidad":0.12,"Temporada baja":0.10}[campaign]
        disc_jitter = float(np.clip(np.random.normal(0, 0.03), -0.05, 0.08))
        discount = float(np.clip(disc_base + disc_jitter, 0, 0.35))

        price = base_price * seg_mult * country_mult * chan_mult * season_mult
        ingresos = units * price * (1 - discount)
        ingresos *= float(np.clip(np.random.normal(1, 0.06), 0.85, 1.18))

        cost_ratio = {"Electronica":0.70,"Hogar":0.66,"Moda":0.62,"Deportes":0.68}[cat] + float(np.clip(np.random.normal(0, 0.03), -0.05, 0.05))
        costo = ingresos * cost_ratio
        ganancia = ingresos - costo

        # nulos y tipos mixtos
        if np.random.rand() < 0.015:
            discount = np.nan
        unidades_val = str(units) if np.random.rand() < 0.35 else units
        ingresos_val = f"{ingresos:.2f}" if np.random.rand() < 0.25 else ingresos

        out.append({
            "ID_Pedido": f"ORD-{d.year}{d.month:02d}-{i:05d}",
            "Fecha_pedido": d.strftime("%d/%m/%Y"),   # texto dd/mm/yyyy (para practicar locale)
            "ID_Cliente": f"CLI-{np.random.randint(1000,9999)}",
            "Segmento_Cliente": seg,
            "Pais": country,
            "Region": region,
            "Ciudad": city,
            "Categoria_Producto": cat,
            "Producto": prod,
            "Canal": channel,
            "Campaña": campaign,
            "Estación": season,
            "Unidades": unidades_val,
            "Descuento_pct": discount,
            "Ingresos": ingresos_val,                 # a veces texto
            "Costo": costo,
            "Ganancia": ganancia
        })
    return pd.DataFrame(out)

df = make_orders(30000)

excel_path = "S10_AndesRetail_Desempeno_Comercial_2022_2025.xlsx"
csv_path = "S10_AndesRetail_Desempeno_Comercial_2022_2025.csv"

df.to_csv(csv_path, index=False, encoding="utf-8")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Ventas", index=False)

print("Listo")
print("Archivo Excel:", excel_path)
print("Archivo CSV:", csv_path)
print("Filas/columnas:", df.shape)