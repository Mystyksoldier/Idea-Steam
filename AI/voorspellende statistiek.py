def lineaire_regressie(x, y, stapgrootte, herhalingen):
    # Begin bij 0 voor de helling (h) en het startpunt (s)
    h = 0  # Helling
    s = 0  # Startpunt
    aantal_data = len(x)

    # Herhaal dit proces een paar keer
    for i in range(herhalingen):
        # Bereken wat de lijn nu voorspelt
        voorspellingen = [(h * x[i] + s) for i in range(aantal_data)]

        # Kijk hoeveel de lijn fout doet
        fout_m = sum((y[i] - voorspellingen[i]) * -x[i] for i in range(aantal_data)) / aantal_data
        fout_b = sum((y[i] - voorspellingen[i]) * -1 for i in range(aantal_data)) / aantal_data

        # Verbeter de lijn een beetje
        h = h - stapgrootte * fout_m
        s = s - stapgrootte * fout_b

    # Geef de beste helling (m) en startpunt (b)
    return h, s
