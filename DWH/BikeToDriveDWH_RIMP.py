import sqlite3


def main():
    con = sqlite3.connect("BikeToDriveDWH.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.executescript(
        """--sql
        CREATE TABLE IF NOT EXISTS Dim_Maand (
            maand_id    INTEGER PRIMARY KEY,
            maandnr     TINYINT,
            maand       TEXT,
            kwartaal    TEXT,
            jaar        SMALLINT
        );

        CREATE TABLE IF NOT EXISTS Dim_Datum (
            datum       DATE PRIMARY KEY,
            dag         TINYINT,
            maand_id    INTEGER,
            FOREIGN KEY (maand_id) REFERENCES Dim_Maand(maand_id)
        );

        CREATE TABLE IF NOT EXISTS Dim_Klant (
            klantnr       INTEGER PRIMARY KEY,
            naam          TEXT,
            adres         TEXT,
            woonplaats    TEXT,
            geslacht      TEXT,
            geboortedatum DATE
        );

        CREATE TABLE IF NOT EXISTS Dim_Filiaal (
            filiaalnr INTEGER PRIMARY KEY,
            naam      TEXT,
            adres     TEXT,
            provincie TEXT
        );

        CREATE TABLE IF NOT EXISTS Dim_Monteur (
            monteurnr  INTEGER PRIMARY KEY,
            naam       TEXT,
            woonplaats TEXT,
            uurloon    REAL,
            filiaal    INTEGER,
            FOREIGN KEY (filiaal) REFERENCES Dim_Filiaal(filiaalnr)
        );

        CREATE TABLE IF NOT EXISTS Dim_Product (
            productnr      INTEGER PRIMARY KEY,
            categorie      TEXT,
            soort          TEXT,
            merk           TEXT,
            type_product   TEXT,
            standaardprijs REAL,
            inkoopprijs    REAL,
            omzet          REAL,
            kleur          TEXT
        );

        CREATE TABLE IF NOT EXISTS Dim_Partner (
            partnernr    INTEGER PRIMARY KEY,
            naam         TEXT,
            adres        TEXT,
            plaats       TEXT,
            type_partner TEXT
        );

        CREATE TABLE IF NOT EXISTS Feit_Onderhoud (
            onderhoudnr INTEGER PRIMARY KEY,
            datum       DATE,
            starttijd   TIME,
            eindtijd    TIME,
            duur        REAL,
            fiets       INTEGER,
            monteur     INTEGER,
            FOREIGN KEY (datum)    REFERENCES Dim_Datum(datum),
            FOREIGN KEY (fiets)    REFERENCES Dim_Product(productnr),
            FOREIGN KEY (monteur)  REFERENCES Dim_Monteur(monteurnr)
        );

        CREATE TABLE IF NOT EXISTS Feit_Verkoop (
            verkoopnr      INTEGER PRIMARY KEY,
            datum          DATE,
            aantal         INTEGER,
            standaardprijs REAL,
            verkoopprijs   REAL,
            korting        REAL,
            klant          INTEGER,
            accessoire     TEXT,
            product        INTEGER,
            monteur        INTEGER,
            FOREIGN KEY (datum)    REFERENCES Dim_Datum(datum),
            FOREIGN KEY (klant)    REFERENCES Dim_Klant(klantnr),
            FOREIGN KEY (product)  REFERENCES Dim_Product(productnr),
            FOREIGN KEY (monteur)  REFERENCES Dim_Monteur(monteurnr)
        );

        CREATE TABLE IF NOT EXISTS Feit_Inkoop (
            inkoopnr        INTEGER PRIMARY KEY,
            inkoopmaandnr   INTEGER,
            inkoopjaar      INTEGER,
            partnernr       INTEGER,
            productnr       INTEGER,
            aantal          INTEGER,
            inkoopprijs     REAL,
            FOREIGN KEY (inkoopmaandnr) REFERENCES Dim_Maand(maandnr),
            FOREIGN KEY (partnernr)  REFERENCES Dim_Partner(partnernr),
            FOREIGN KEY (productnr)  REFERENCES Dim_Product(productnr)
        );
        """
    )
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
