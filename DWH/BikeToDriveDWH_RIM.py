import sqlite3


def main():
    con = sqlite3.connect("BikeToDriveDWH.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.executescript(
        """--sql
    -- DIM PARTNER
    CREATE TABLE IF NOT EXISTS Dim_Partner (
        partnernr    INTEGER PRIMARY KEY,
        naam         TEXT,
        adres        TEXT,
        plaats       TEXT,
        type_partner TEXT
    );

    -- DIM PRODUCT
    CREATE TABLE IF NOT EXISTS Dim_Product (
        productnr      INTEGER PRIMARY KEY,
        categorie      TEXT,
        soort          TEXT,
        merk           TEXT,
        type_product   TEXT,
        standaardprijs REAL,
        inkoopprijs    REAL,
        omzet          REAL,
        kleur          TEXT,
        partnernr        INTEGER,
        FOREIGN KEY (partnernr) REFERENCES Dim_Partner(partnernr)
    );

    -- DIM MAAND
    CREATE TABLE IF NOT EXISTS Dim_Maand (
        maand_id INTEGER PRIMARY KEY,
        maandnr  INTEGER,
        maand    TEXT,
        kwartaal TEXT,
        jaar     INTEGER
    );

    -- DIM DATUM
    CREATE TABLE IF NOT EXISTS Dim_Datum (
        datum     TEXT PRIMARY KEY,
        dag       INTEGER,
        maand_id  INTEGER,
        FOREIGN KEY (maand_id) REFERENCES Dim_Maand(maand_id)
    );

    -- DIM KLANT
    CREATE TABLE IF NOT EXISTS Dim_Klant (
        klantnr       INTEGER PRIMARY KEY,
        naam          TEXT,
        adres         TEXT,
        woonplaats    TEXT,
        geslacht      TEXT,
        geboortedatum TEXT
    );

    -- DIM FILIAAL
    CREATE TABLE IF NOT EXISTS Dim_Filiaal (
        filiaalnr INTEGER PRIMARY KEY,
        naam      TEXT,
        adres     TEXT,
        provincie TEXT
    );

    -- DIM MONTEUR
    CREATE TABLE IF NOT EXISTS Dim_Monteur (
        monteurnr  INTEGER PRIMARY KEY,
        naam       TEXT,
        woonplaats TEXT,
        uurloon    REAL,
        filiaal    INTEGER,
        FOREIGN KEY (filiaal) REFERENCES Dim_Filiaal(filiaalnr)
    );

    -- FEIT VERKOOP
    CREATE TABLE IF NOT EXISTS Feit_Verkoop (
        verkoopnr      INTEGER PRIMARY KEY,
        datum          TEXT,
        aantal         INTEGER,
        standaardprijs REAL,
        verkoopprijs   REAL,
        totaalprijs    REAL,
        korting        REAL,
        klantnr        INTEGER,
        productnr      INTEGER,
        monteurnr      INTEGER,
        FOREIGN KEY (datum)     REFERENCES Dim_Datum(datum),
        FOREIGN KEY (klantnr)   REFERENCES Dim_Klant(klantnr),
        FOREIGN KEY (productnr) REFERENCES Dim_Product(productnr),
        FOREIGN KEY (monteurnr) REFERENCES Dim_Monteur(monteurnr)
    );

    -- FEIT INKOOP
    CREATE TABLE IF NOT EXISTS Feit_Inkoop (
        inkoopnr      INTEGER PRIMARY KEY,
        inkoopmaand   INTEGER,
        inkoopjaar    INTEGER,
        partnernr     INTEGER,
        productnr     INTEGER,
        aantal        INTEGER,
        inkoopprijs   REAL,
        totaalprijs   REAL,
        FOREIGN KEY (inkoopmaand)  REFERENCES Dim_Maand(maand_id),
        FOREIGN KEY (partnernr)  REFERENCES Dim_Partner(partnernr),
        FOREIGN KEY (productnr)  REFERENCES Dim_Product(productnr)
    );

    -- FEIT ONDERHOUD
    CREATE TABLE IF NOT EXISTS Feit_Onderhoud (
        onderhoudnr INTEGER PRIMARY KEY,
        datum       TEXT,
        starttijd   TEXT,
        eindtijd    TEXT,
        duur        INTEGER,
        productnr       INTEGER,
        monteurnr     INTEGER,
        FOREIGN KEY (datum)   REFERENCES Dim_Datum(datum),
        FOREIGN KEY (productnr)   REFERENCES Dim_Product(productnr),
        FOREIGN KEY (monteurnr) REFERENCES Dim_Monteur(monteurnr)
    );
    """
    )

    con.commit()
    con.close()


if __name__ == "__main__":
    main()
