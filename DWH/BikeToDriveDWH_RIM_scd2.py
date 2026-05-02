import sqlite3


def main():
    con = sqlite3.connect("BikeToDriveDWH_SCD2.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.executescript("""--sql

    -- =========================================================
    -- DIMENSIES  (SCD Type 2: surrogate key als PRIMARY KEY)
    -- =========================================================

    -- DIM PARTNER
    CREATE TABLE IF NOT EXISTS Dim_Partner (
        partner_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
        partnernr    INTEGER NOT NULL,        -- business key
        naam         TEXT,
        adres        TEXT,
        plaats       TEXT,
        type_partner TEXT,
        -- SCD Type 2
        geldig_van   TEXT NOT NULL DEFAULT '1900-01-01',
        geldig_tot   TEXT NOT NULL DEFAULT '9999-12-31',
        is_huidig    INTEGER NOT NULL DEFAULT 1
    );

    -- DIM PRODUCT
    CREATE TABLE IF NOT EXISTS Dim_Product (
        product_sk     INTEGER PRIMARY KEY AUTOINCREMENT,
        productnr      INTEGER NOT NULL,      -- business key
        categorie      TEXT,
        soort          TEXT,
        merk           TEXT,
        type_product   TEXT,
        standaardprijs REAL,
        inkoopprijs    REAL,
        omzet          REAL,
        kleur          TEXT,
        partnernr      INTEGER,
        partner_sk     INTEGER,
        -- SCD Type 2
        geldig_van     TEXT NOT NULL DEFAULT '1900-01-01',
        geldig_tot     TEXT NOT NULL DEFAULT '9999-12-31',
        is_huidig      INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (partnernr) REFERENCES Dim_Partner(partnernr)
    );

    -- DIM MAAND  (geen SCD — tijdsdimensie verandert nooit)
    CREATE TABLE IF NOT EXISTS Dim_Maand (
        maand_id INTEGER PRIMARY KEY,
        maandnr  INTEGER,
        maand    TEXT,
        kwartaal TEXT,
        jaar     INTEGER
    );

    -- DIM DATUM  (geen SCD — tijdsdimensie verandert nooit)
    CREATE TABLE IF NOT EXISTS Dim_Datum (
        datum    TEXT PRIMARY KEY,
        dag      INTEGER,
        maand_id INTEGER,
        FOREIGN KEY (maand_id) REFERENCES Dim_Maand(maand_id)
    );

    -- DIM KLANT
    CREATE TABLE IF NOT EXISTS Dim_Klant (
        klant_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
        klantnr       INTEGER NOT NULL,       -- business key
        naam          TEXT,
        adres         TEXT,
        woonplaats    TEXT,
        geslacht      TEXT,
        geboortedatum TEXT,
        -- SCD Type 2
        geldig_van    TEXT NOT NULL DEFAULT '1900-01-01',
        geldig_tot    TEXT NOT NULL DEFAULT '9999-12-31',
        is_huidig     INTEGER NOT NULL DEFAULT 1
    );

    -- DIM FILIAAL
    CREATE TABLE IF NOT EXISTS Dim_Filiaal (
        filiaal_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        filiaalnr  INTEGER NOT NULL,          -- business key
        naam       TEXT,
        adres      TEXT,
        provincie  TEXT,
        -- SCD Type 2
        geldig_van TEXT NOT NULL DEFAULT '1900-01-01',
        geldig_tot TEXT NOT NULL DEFAULT '9999-12-31',
        is_huidig  INTEGER NOT NULL DEFAULT 1
    );

    -- DIM MONTEUR
    CREATE TABLE IF NOT EXISTS Dim_Monteur (
        monteur_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        monteurnr  INTEGER NOT NULL,          -- business key
        naam       TEXT,
        woonplaats TEXT,
        uurloon    REAL,
        filiaal    INTEGER,
        -- SCD Type 2
        geldig_van TEXT NOT NULL DEFAULT '1900-01-01',
        geldig_tot TEXT NOT NULL DEFAULT '9999-12-31',
        is_huidig  INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (filiaal) REFERENCES Dim_Filiaal(filiaalnr)
    );

    -- =========================================================
    -- FEITENTABELLEN  (foreign keys naar surrogate keys)
    -- =========================================================

    -- FEIT VERKOOP
    CREATE TABLE IF NOT EXISTS Feit_Verkoop (
        verkoopnr      INTEGER PRIMARY KEY,
        datum          TEXT,
        aantal         INTEGER,
        standaardprijs REAL,
        verkoopprijs   REAL,
        totaalprijs    REAL,
        korting        REAL,
        klant_sk       INTEGER,
        product_sk     INTEGER,
        monteur_sk     INTEGER,
        FOREIGN KEY (datum)      REFERENCES Dim_Datum(datum),
        FOREIGN KEY (klant_sk)   REFERENCES Dim_Klant(klant_sk),
        FOREIGN KEY (product_sk) REFERENCES Dim_Product(product_sk),
        FOREIGN KEY (monteur_sk) REFERENCES Dim_Monteur(monteur_sk)
    );

    -- FEIT INKOOP
    CREATE TABLE IF NOT EXISTS Feit_Inkoop (
        inkoopnr    INTEGER PRIMARY KEY,
        inkoopmaand INTEGER,
        inkoopjaar  INTEGER,
        aantal      INTEGER,
        inkoopprijs REAL,
        totaalprijs REAL,
        product_sk  INTEGER,
        partner_sk  INTEGER,
        productnr   INTEGER,
        FOREIGN KEY (inkoopmaand) REFERENCES Dim_Maand(maand_id),
        FOREIGN KEY (product_sk)  REFERENCES Dim_Product(product_sk),
        FOREIGN KEY (partner_sk)  REFERENCES Dim_Partner(partner_sk)
    );

    -- FEIT ONDERHOUD
    CREATE TABLE IF NOT EXISTS Feit_Onderhoud (
        onderhoudnr INTEGER PRIMARY KEY,
        datum       TEXT,
        starttijd   TEXT,
        eindtijd    TEXT,
        duur        TEXT,
        product_sk  INTEGER,
        monteur_sk  INTEGER,
        FOREIGN KEY (datum)      REFERENCES Dim_Datum(datum),
        FOREIGN KEY (product_sk) REFERENCES Dim_Product(product_sk),
        FOREIGN KEY (monteur_sk) REFERENCES Dim_Monteur(monteur_sk)
    );
        """)
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
