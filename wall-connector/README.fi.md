# Wall Connector Gen 3 -kuormanhallinta (ESPHome)

> **KOKEELLINEN – konfiguraatiot on validoitu `esphome config` -komennolla, mutta niitä ei ole vielä flashattu eikä testattu omalla laitteistolla.**
> Englanniksi: [README.md](README.md).

Paikallinen, pilvetön dynaaminen kuormanhallinta Tesla Wall Connector Gen 3 -laturille suomalaisessa kolmivaiheliittymässä. ESP32 esittää laturin RS-485-väylässä Neurio-energiamittaria, jolloin laturin oma Dynamic Power Management pitää kuormitetuimman vaiheen pääsulakkeen budjetin alla. Vaihevirrat tulevat pääkeskuksen Shelly Pro 3EM:ltä.

Tämä kansio on **erillään** repositorion CAN-tutkimustyökaluista. Mikään täällä ei lähetä mitään auton CAN-väylään.

## Toimintaperiaate

- Laturilla ei ole paikallista käskyä "lataa X A:lla", ja sen paikallinen API on vain luku.
- ESP32 vastaa laturin Modbus-kyselyihin Neurio-mittarina ja julkaisee muokatun version oikeasta pääkeskuksen mittauksesta ([Tesla LoadPilot](https://github.com/zany92/tesla-loadpilot) -säätölaki).
- Laturi reagoi vain siihen, onko julkaistu arvo sen Max Conductor Limit -rajan yli vai ali ja kuinka paljon. LoadPilot kuvaa tämän rajan (21 A) talon budjetiksi (pääsulake × 90 %).
- Laturi ottaa saman virran kaikilta kolmelta vaiheelta, joten kuormitetuin vaihe määrää latausvirran. Yksivaiheinen lämpöpumppu tekee tästä tärkeää.

## Kortit

| Kortti | Tiedosto | Sijainti | Tehtävä |
|---|---|---|---|
| ESP32-S3 | `esphome/loadpilot-twc.yaml` | Laturin RS-485-liittimissä | Neurio-emulointi ja säätölaki |
| ESP32-C3 | `esphome/loadpilot-meter.yaml` | Missä tahansa WiFin kantamalla | Lukee Shelly Pro 3EM:n HTTP:llä (1 Hz) ja lähettää kuusi suuretta salattuna UDP:nä |
| ESP32-S3 (valinnainen) | `esphome/tesla-ble.yaml` | Autotallissa auton lähellä | Tarkka latausvirta sekä lataus päälle/pois auton kautta BLE:llä |

C3 on valinnainen. Ilman sitä S3 lukee Shellyn Home Assistantin kautta, mutta lataus estyy aina, kun Home Assistant käynnistyy uudelleen. Bluetooth on omalla kortillaan, koska laturisolmun on vastattava jokaiseen Modbus-kyselyyn noin 66 ms:ssa.

## Firmware-yhteensopivuus

- Tesla LoadPilot on todettu toimivaksi Wall Connectorin firmwareilla **26.18** ja **26.26.1**.
- Aiempi Klangen82:n emulaattori **ei** toimi firmwaresta 26.2 alkaen.
- Uudempaa firmwarea (esimerkiksi 26.34) ei ole testattu: käy läpi testiportaat RAW → OMBRE-MAX → ACTIF-MAX ennen kuin luotat siihen.

## Käyttöönotto lyhyesti

1. Kopioi `esphome/secrets.example.yaml` ESPHomen `secrets.yaml`-tiedostoon ja täytä arvot.
2. Aseta `loadpilot-twc.yaml`-tiedostoon pääsulakkeen koko ja korvaa `XXXXXXXXXXXX` Shellysi tunnisteella. Aseta `loadpilot-meter.yaml`-tiedostoon Shellyn IP-osoite.
3. Flashaa USB:llä. Vaihda laturisolmun **Signal Mode** heti tilaan **RAW**, koska solmu käynnistyy aktiivitilaan.
4. Kytke ryhmäsulake pois ja liitä 3,3 V:n RS-485-moduuli laturiin: A punaiseen, B valkoiseen (tarkemmin YAMLin alussa).
5. Tesla One: lisää mittari (tunnistuu Neuriona), aseta CT1–3 tilaan Conductor, laske ensin Max Output Current 16 A:iin ja aseta sitten Max Conductor Limit 21 A:iin.
6. Tarkista Polling Active, noin 200 ms:n poll-väli ja Source Active = UDP. Siirry sitten latauksen aikana tiloihin OMBRE-MAX ja ACTIF-MAX.

## Demo

`demo/kuormanhallinta.html` on itsenäinen simulaatio toiminnasta: kytke kodin kuormia, vaihda pääsulakkeen kokoa ja kytke kuormanhallinta pois. Avaa tiedosto selaimessa. Arvot ovat esimerkkejä, eivät mittauksia.

## Turvallisuus

RS-485-kytkentä tehdään Wall Connectorin sisällä 230 V:n vieressä. Tee työ ryhmäsulake pois päältä ja jätä se pätevälle sähköasentajalle, jos et itse ole sellainen. Älä OTA-päivitä laturisolmua latauksen aikana.

## Tekijät

- [Tesla LoadPilot](https://github.com/zany92/tesla-loadpilot), zany92 (MIT): säätölaki ja laturisolmun paketti, käytössä ESPHomen etäpakettina versiossa `v1.4.0`.
- [PVi1/esphome-twc-control](https://github.com/PVi1/esphome-twc-control): Neurio-emuloinnin idea. Rekisterikartta: LucaTNT:n gist.
- [yoziru/esphome-tesla-ble](https://github.com/yoziru/esphome-tesla-ble) (AGPL-3.0): käytössä etäpakettina versiossa `v2026.10.4`, ei kopioitu tähän.

Ei Teslan tuote eikä Tesla, Inc.:n tukema.
