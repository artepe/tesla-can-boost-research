# Tesla Model 3 CAN -tutkimusprojekti

> **KESKENERÄINEN / KOKEELLINEN — EI VALMIS KÄYTTÖÖN**

Tämä on **keskeneräinen Tesla Model 3 / Model Y CAN-väylän tutkimusprojekti**, jonka pohjana on **ColinM-sys:n Acceleration Boost / CAN Bus Toolkit -projekti**.

**Alkuperäinen lähde:** [ColinM-sys/tesla-can-boost](https://github.com/ColinM-sys/tesla-can-boost)  
**Alkuperäinen tekijä:** Colin McDonough ([ColinM-sys](https://github.com/ColinM-sys))  
**Tämän tutkimusversion dokumentointi ja paketointi:** [artepe](https://github.com/artepe)

Tämä paketti on alkuperäisen projektin pohjalta dokumentoitu tutkimusversio. Alkuperäisiä Python-tiedostoja ei ole muutettu, lukuun ottamatta neljän paikallisen web-palvelimen tietoturvakorjausta (`dashboard_server.py`, `drive_recorder.py`, `ghost3d.py`, `ghost_ui.py`): ne kuuntelevat oletuksena vain omaa konetta, vaativat joka käynnistyksellä vaihtuvan pääsytunnisteen eivätkä enää salli muiden sivustojen pyyntöjä tai mielivaltaisten tiedostojen lukemista (ks. [SECURITY.md](SECURITY.md)). Uutta ovat selkeytetty dokumentaatio, tekijätiedot ja riippuvuustiedostot. Alkuperäinen README on tallessa osoitteessa [`docs/UPSTREAM_README.md`](docs/UPSTREAM_README.md).

## Sisältö

- CAN-väylän tietojen lukemiseen, tallennukseen ja analysointiin tarkoitettuja Python-työkaluja.
- Selaimella katseltavia koenäyttöjä sekä mittausdatan käsittelyä.
- Model 3 -auton yhteisöpohjainen DBC-signaalitietokanta.
- Alkuperäisestä projektista perittyjä **kokeellisia ja riskialttiita CAN-kirjoitusskriptejä**, joita **ei ole vahvistettu turvallisiksi eikä toimiviksi**.

## Mitä ei ole vielä todistettu?

- Teslan virallista **Acceleration Boost -ominaisuutta ei ole osoitettu avatuksi** tämän koodin avulla.
- Ajotilaan liittyvän CAN-arvon muuttaminen ei yksin todista auton todellisen huipputehon kasvavan.
- Toimintaa vuoden 2019 Tesla Model 3 Long Range AWD -mallilla ei ole vahvistettu.
- S3XY Commander / ESP32 -laitteiden yhteensopivuutta ei ole vahvistettu.
- Dokumentaatiossa esiintyviä alkuperäisen tekijän testiväitteitä ei ole itsenäisesti varmennettu tässä versiossa.

## Turvallinen aloitus

Suosituksena on aloittaa lähdekoodin tarkastelulla sekä **offline-analyysillä ja passiivisella tiedonkeruulla**, ei CAN-viestien lähettämisellä. Osassa skriptejä on Windowsin COM-porttiin sidottuja oletusasetuksia.

Python 3.10+:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/scan_ports.py
```

**Älä suorita auton ohjaukseen, momenttiin tai kaasupolkimeen vaikuttavia CAN-kirjoitusskriptejä käytössä olevaan autoon.** Auton järjestelmiin vaikuttavat kokeilut kuuluvat vain asianmukaisesti eristettyyn laboratorioympäristöön.

## Lisenssit ja tekijät

Alkuperäinen projekti on Colin McDonough'n työtä. Pääprojektin mukana ollut [`LICENSE`](LICENSE) määrittää ehdoksi **CC BY-NC 4.0**, joka sallii jakamisen ja muokkaamisen nimeämisvelvoitteen puitteissa **ei-kaupallisesti**. DBC-tiedoston lähde on [joshwardell/model3dbc](https://github.com/joshwardell/model3dbc), jonka lisenssi on MIT (`dbc/LICENSE`). Lue [`ATTRIBUTION.md`](ATTRIBUTION.md).

Alkuperäisessä README:ssä lukee ristiriitaisesti MIT. Tätä ei pidä tulkita koko projektin lisenssiksi alkuperäisen `LICENSE`-tiedoston vastaisesti.

**Kyseessä on riippumaton harrastajatutkimus, ei Teslan hyväksymä tai valmistajan tukema ohjelmisto.** Katso myös [`SECURITY.md`](SECURITY.md) ja [`ROADMAP.md`](ROADMAP.md).
