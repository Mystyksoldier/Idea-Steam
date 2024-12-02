def gemiddelde_uren(uren):
    som_uren = sum(uren)
    aantal_personen = len(uren)
    return som_uren / aantal_personen


online_uren = [3, 4, 2, 5, 6]
print(gemiddelde_uren(online_uren))


