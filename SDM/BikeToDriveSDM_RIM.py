import sqlite3

def main():
    con = sqlite3.connect('BikeToDriveSDM.db')
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys = ON")

    cur.executescript("""

    -- ACCESSOIRE VERKOOP

    CREATE TABLE accessoire_verkoop_klant (
        klantnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        woonplaats TEXT,
        geslacht TEXT,
        geboortedatum TEXT,
        FOREIGN KEY (klantnr) REFERENCES fiets_verkoop_klant(klantnr)
    );

    CREATE TABLE accessoire_verkoop_filiaal (
        filiaalnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        provincie TEXT
    );

    CREATE TABLE accessoire_verkoop_monteur (
        monteurNr INTEGER PRIMARY KEY,
        naam TEXT,
        woonplaats TEXT,
        uurloon REAL,
        filiaal INTEGER,
        FOREIGN KEY (filiaal) REFERENCES accessoire_verkoop_filiaal(filiaalnr)
    );

    CREATE TABLE accessoire_verkoop_leverancier (
        leveranciernr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        woonplaats TEXT
    );

    CREATE TABLE accessoire_verkoop_accessoire (
        accessoirenr INTEGER PRIMARY KEY,
        naam TEXT,
        standaardprijs REAL,
        inkoopprijs REAL,
        soort TEXT,
        leverancier INTEGER,
        FOREIGN KEY (leverancier) REFERENCES accessoire_verkoop_leverancier(leveranciernr)
    );

    CREATE TABLE accessoire_verkoop_verkoop (
        verkoopnr INTEGER PRIMARY KEY,
        datum TEXT,
        aantal INTEGER,
        verkoopprijs REAL,
        klant INTEGER,
        accessoire INTEGER,
        monteur INTEGER,
        FOREIGN KEY (klant) REFERENCES accessoire_verkoop_klant(klantnr),
        FOREIGN KEY (accessoire) REFERENCES accessoire_verkoop_accessoire(accessoirenr),
        FOREIGN KEY (monteur) REFERENCES accessoire_verkoop_monteur(monteurNr)
    );

    -- ACCESSOIRE INKOOP

    CREATE TABLE accessoire_inkoop_leverancier (
        leveranciernr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        woonplaats TEXT
    );

    CREATE TABLE accessoire_inkoop_accessoire (
        accessoirenr INTEGER PRIMARY KEY,
        naam TEXT,
        standaardprijs REAL,
        inkoopprijs REAL,
        soort TEXT,
        leverancier INTEGER,
        FOREIGN KEY (leverancier) REFERENCES accessoire_inkoop_leverancier(leveranciernr)
    );

    CREATE TABLE accessoire_inkoop_inkoop (
        inkoopnr INTEGER PRIMARY KEY,
        inkoopmaand INTEGER,
        inkoopjaar INTEGER,
        aantal INTEGER,
        accessoire INTEGER,
        FOREIGN KEY (accessoire) REFERENCES accessoire_inkoop_accessoire(accessoirenr)
    );

    -- FIETS VERKOOP

    CREATE TABLE fiets_verkoop_klant (
        klantnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        woonplaats TEXT,
        geslacht TEXT,
        geboortedatum TEXT,
        FOREIGN KEY (klantnr) REFERENCES accessoire_verkoop_klant(klantnr)
    );

    CREATE TABLE fiets_verkoop_filiaal (
        filiaalnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        provincie TEXT
    );

    CREATE TABLE fiets_verkoop_monteur (
        monteurNr INTEGER PRIMARY KEY,
        naam TEXT,
        woonplaats TEXT,
        uurloon REAL,
        filiaal INTEGER,
        FOREIGN KEY (filiaal) REFERENCES fiets_verkoop_filiaal(filiaalnr)
    );

    CREATE TABLE fiets_verkoop_fabrikant (
        fabrikantnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        plaats TEXT,
        FOREIGN KEY (fabrikantnr) REFERENCES onderhoud_fabrikant(fabrikantnr),
        FOREIGN KEY (fabrikantnr) REFERENCES fiets_inkoop_fabrikant(fabrikantnr)
    );

    CREATE TABLE fiets_verkoop_fiets (
        fietsnr INTEGER PRIMARY KEY,
        soort TEXT,
        merk TEXT,
        type TEXT,
        standaardprijs REAL,
        inkoopprijs REAL,
        fabrikant INTEGER,
        FOREIGN KEY (fabrikant) REFERENCES fiets_verkoop_fabrikant(fabrikantnr),
        FOREIGN KEY (fietsnr) REFERENCES onderhoud_fiets(fietsnr),
        FOREIGN KEY (fietsnr) REFERENCES fiets_inkoop_fiets(fietsnr)
    );

    CREATE TABLE fiets_verkoop_verkoop (
        verkoopnr INTEGER PRIMARY KEY,
        datum TEXT,
        aantal INTEGER,
        verkoopprijs REAL,
        klant INTEGER,
        fiets INTEGER,
        monteur INTEGER,
        FOREIGN KEY (klant) REFERENCES fiets_verkoop_klant(klantnr),
        FOREIGN KEY (fiets) REFERENCES fiets_verkoop_fiets(fietsnr),
        FOREIGN KEY (monteur) REFERENCES fiets_verkoop_monteur(monteurNr)
    );

    -- FIETS INKOOP

    CREATE TABLE fiets_inkoop_fabrikant (
        fabrikantnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        plaats TEXT,
        FOREIGN KEY (fabrikantnr) REFERENCES onderhoud_fabrikant(fabrikantnr),
        FOREIGN KEY (fabrikantnr) REFERENCES fiets_verkoop_fabrikant(fabrikantnr)
    );

    CREATE TABLE fiets_inkoop_fiets (
        fietsnr INTEGER PRIMARY KEY,
        soort TEXT,
        merk TEXT,
        type TEXT,
        standaardprijs REAL,
        inkoopprijs REAL,
        kleur TEXT,
        fabrikant INTEGER,
        FOREIGN KEY (fabrikant) REFERENCES fiets_inkoop_fabrikant(fabrikantnr),
        FOREIGN KEY (fietsnr) REFERENCES onderhoud_fiets(fietsnr),
        FOREIGN KEY (fietsnr) REFERENCES fiets_verkoop_fiets(fietsnr)
    );

    CREATE TABLE fiets_inkoop_inkoop (
        inkoopnr INTEGER PRIMARY KEY,
        inkoopmaand INTEGER,
        inkoopjaar INTEGER,
        aantal INTEGER,
        fiets INTEGER,
        FOREIGN KEY (fiets) REFERENCES fiets_inkoop_fiets(fietsnr)
    );

    -- ONDERHOUD

    CREATE TABLE onderhoud_filiaal (
        filiaalnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        provincie TEXT
    );

    CREATE TABLE onderhoud_monteur (
        monteurNr INTEGER PRIMARY KEY,
        naam TEXT,
        woonplaats TEXT,
        uurloon REAL,
        filiaal INTEGER,
        FOREIGN KEY (filiaal) REFERENCES onderhoud_filiaal(filiaalnr)
    );

    CREATE TABLE onderhoud_fiets (
        fietsnr INTEGER PRIMARY KEY,
        soort TEXT,
        merk TEXT,
        type TEXT,
        kleur TEXT,
        FOREIGN KEY (fietsnr) REFERENCES fiets_verkoop_fiets(fietsnr),
        FOREIGN KEY (fietsnr) REFERENCES fiets_inkoop_fiets(fietsnr)
    );
                      
    CREATE TABLE onderhoud_fabrikant (
        fabrikantnr INTEGER PRIMARY KEY,
        naam TEXT,
        adres TEXT,
        plaats TEXT,
        FOREIGN KEY (fabrikantnr) REFERENCES fiets_verkoop_fabrikant(fabrikantnr),
        FOREIGN KEY (fabrikantnr) REFERENCES fiets_inkoop_fabrikant(fabrikantnr)
    );

    CREATE TABLE onderhoud_onderhoud (
        onderhoudnr INTEGER PRIMARY KEY,
        datum TEXT,
        starttijd TEXT,
        eindtijd TEXT,
        fiets INTEGER,
        monteur INTEGER,
        FOREIGN KEY (fiets) REFERENCES onderhoud_fiets(fietsnr),
        FOREIGN KEY (monteur) REFERENCES onderhoud_monteur(monteurNr)
    );

    """)

    con.commit()
    con.close()

if __name__ == "__main__":
    main()