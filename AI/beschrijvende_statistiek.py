def mediaan_uren(uren):
    # Sorteer de lijst handmatig
    uren_sorted = sorted(uren)
    aantal_personen = len(uren_sorted)
    # Controleer of het aantal waarden oneven of even is
    if aantal_personen % 2 == 1:  # Oneven
        return uren_sorted[aantal_personen // 2]
    else:  # Even
        midden_links = uren_sorted[aantal_personen // 2 - 1]
        midden_rechts = uren_sorted[aantal_personen // 2]
        return (midden_links + midden_rechts) / 2


def gemiddelde_uren(uren):
    som_uren = sum(uren)
    aantal_personen = len(uren)
    return som_uren / aantal_personen


# Voorbeelddata
online_uren = [3, 4, 2, 5, 6]
print("Gemiddelde:", gemiddelde_uren(online_uren))
print("Mediaan:", mediaan_uren(online_uren))
