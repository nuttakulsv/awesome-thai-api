# awesome-thai-api

[ภาษาไทย](README.md) · From the maker of [thaiproof](https://github.com/nuttakulsv/thaiproof) and [thai-id-card-kit](https://github.com/nuttakulsv/thai-id-card-kit)

Thai APIs that actually work: government services and the platforms Thai developers use every day. PM2.5 and air quality, today's fuel prices, earthquakes, water levels, tax ID lookups, government open data and more.

Most lists of Thai APIs you'll find are half dead links. This one **calls every API daily** and updates the "Working" column itself. For APIs that need no key it also checks that the response still looks the same, and each of them comes with a `curl` you can paste right away.

<!-- apis:start -->
_Last checked 2026-11-01 (UTC) from GitHub's servers outside Thailand_

### Weather and disasters

| API | What it gives you | Key | Working |
|---|---|---|---|
| [TMD Earthquake feed](https://earthquake.tmd.go.th/)<br><sub>Thai Meteorological Department</sub> | Recent earthquakes in Thailand and the region, as RSS | no key | ✅ |
| [TMD Weather API](https://data.tmd.go.th/api/index1.php)<br><sub>Thai Meteorological Department</sub> | Daily weather, 7-day forecasts, warnings, rainfall, earthquakes (XML). The docs include a sample uid/ukey to try; register your own for real use | free sign-up | ✅ |
| [TMD NWP Forecast API](https://data.tmd.go.th/nwpapi/doc/)<br><sub>Thai Meteorological Department</sub> | Numerical hourly and daily forecasts by coordinates or province (JSON) | free sign-up | ✅ |

<details><summary>Example requests</summary>

**TMD Earthquake feed**

```sh
curl -s https://earthquake.tmd.go.th/feed/rss_tmd.xml
```

**TMD Weather API**

```sh
curl -s 'https://data.tmd.go.th/api/WeatherToday/V2/?uid=api&ukey=api12345'
```

**TMD NWP Forecast API**

```sh
curl -s -H 'authorization: Bearer YOUR_TOKEN' 'https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at?lat=13.75&lon=100.5&fields=tc,rh'
```

</details>

### Air quality and PM2.5

| API | What it gives you | Key | Working |
|---|---|---|---|
| [Air4Thai](https://air4thai.pcd.go.th/webV3/)<br><sub>Pollution Control Department</sub> | Latest AQI, PM2.5, PM10, O3, CO and NO2 from monitoring stations nationwide | no key | ✅ ¹ |
| [GISTDA PM2.5](https://pm25.gistda.or.th/)<br><sub>GISTDA</sub> | PM2.5 by province from satellite data, including the 24-hour average | no key | ⚠️ HTTP 503 |

<details><summary>Example requests</summary>

**Air4Thai**

```sh
curl -s https://air4thai.pcd.go.th/services/getNewAQI_JSON.php
```

**GISTDA PM2.5**

```sh
curl -s https://pm25.gistda.or.th/rest/getPm25byProvince
```

</details>

### Water and floods

| API | What it gives you | Key | Working |
|---|---|---|---|
| [ThaiWater](https://www.thaiwater.net/)<br><sub>HII</sub> | Water levels, dam storage and conditions from telemetry stations nationwide | no key | ✅ |

<details><summary>Example requests</summary>

**ThaiWater**

```sh
curl -s https://api-v3.thaiwater.net/api/v1/thaiwater30/public/waterlevel_load
```

</details>

### Fuel prices

| API | What it gives you | Key | Working |
|---|---|---|---|
| [PTT OR Oil Price](https://orapiweb.pttor.com/oilservice/OilPrice.asmx)<br><sub>PTT OR</sub> | Today's retail fuel prices at PTT Station (SOAP) | no key | ✅ |
| [Bangchak Oil Price](https://www.bangchak.co.th/th/oilprice)<br><sub>Bangchak</sub> | Bangchak fuel prices today and tomorrow (JSON) | no key | ✅ |

<details><summary>Example requests</summary>

**PTT OR Oil Price**

```sh
curl -s https://orapiweb.pttor.com/oilservice/OilPrice.asmx -H 'Content-Type: text/xml; charset=utf-8' -H 'SOAPAction: "http://www.pttor.com/CurrentOilPrice"' -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><CurrentOilPrice xmlns="http://www.pttor.com"><Language>TH</Language></CurrentOilPrice></soap:Body></soap:Envelope>'
```

**Bangchak Oil Price**

```sh
curl -s https://oil-price.bangchak.co.th/ApiOilPrice2/th
```

</details>

### Finance and exchange rates

| API | What it gives you | Key | Working |
|---|---|---|---|
| [BOT API](https://portal.api.bot.or.th/)<br><sub>Bank of Thailand</sub> | Exchange rates, interest rates, financial institution holidays and economic statistics. Free sign-up on the API portal | free sign-up | ✅ |
| [Bitkub Public API](https://github.com/bitkub/bitkub-official-api-docs)<br><sub>Bitkub</sub> | Crypto prices in baht (ticker, order book, trades). The public endpoints need no key | no key | ✅ |

<details><summary>Example requests</summary>

**Bitkub Public API**

```sh
curl -s 'https://api.bitkub.com/api/v3/market/ticker?sym=btc_thb'
```

</details>

### Tax and company data

| API | What it gives you | Key | Working |
|---|---|---|---|
| [RD VAT Service](https://rdws.rd.go.th/serviceRD3/vatserviceRD3.asmx)<br><sub>Revenue Department</sub> | Look up a VAT-registered business by tax ID: name and address (SOAP, username and password are anonymous) | no key | ✅ |
| [DBD Open Data](https://opendata.dbd.go.th/)<br><sub>Department of Business Development</sub> | Registered companies, financial statements and business statistics. Some datasets need sign-up | free sign-up | ⚠️ HTTP 403 |

<details><summary>Example requests</summary>

**RD VAT Service**

```sh
curl -s https://rdws.rd.go.th/serviceRD3/vatserviceRD3.asmx -H 'Content-Type: text/xml; charset=utf-8' -H 'SOAPAction: "https://rdws.rd.go.th/serviceRD3/vatserviceRD3/Service"' -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Service xmlns="https://rdws.rd.go.th/serviceRD3/vatserviceRD3"><username>anonymous</username><password>anonymous</password><TIN>TAX_ID_13_DIGITS</TIN><ProvinceCode>0</ProvinceCode><BranchNumber>0</BranchNumber><AmphurCode>0</AmphurCode></Service></soap:Body></soap:Envelope>'
```

</details>

### Government open data

| API | What it gives you | Key | Working |
|---|---|---|---|
| [data.go.th (CKAN)](https://data.go.th/)<br><sub>DGA</sub> | Search over 40,000 government open datasets through the standard CKAN API | no key | ⚠️ HTTP 403 |
| [Bangkok Open Data (CKAN)](https://data.bangkok.go.th/)<br><sub>BMA</sub> | Bangkok's open datasets (flood risk points, CCTV, parks and more) through the CKAN API | no key | ⚠️ ConnectionResetError |

<details><summary>Example requests</summary>

**data.go.th (CKAN)**

```sh
curl -sG https://data.go.th/api/3/action/package_search --data-urlencode q=โรงพยาบาล -d rows=5
```

**Bangkok Open Data (CKAN)**

```sh
curl -sG https://data.bangkok.go.th/api/3/action/package_search --data-urlencode q=สวนสาธารณะ -d rows=5
```

</details>

### Maps and delivery

| API | What it gives you | Key | Working |
|---|---|---|---|
| [Longdo Map API](https://map.longdo.com/api)<br><sub>Metamedia Technology</sub> | Maps of Thailand, place search, geocoding and routing, with a free tier | free sign-up | ✅ |
| [Thailand Post Track & Trace API](https://track.thailandpost.co.th/developerGuide)<br><sub>Thailand Post</sub> | Track parcels by tracking number. Free token on sign-up | free sign-up | ✅ |

### Thai language and AI

| API | What it gives you | Key | Working |
|---|---|---|---|
| [AI for Thai](https://www.aiforthai.in.th/)<br><sub>NECTEC</sub> | Thai word segmentation, translation, speech-to-text, Thai text-to-speech, OCR and more. Free key | free sign-up | ✅ |
| [Typhoon](https://opentyphoon.ai/)<br><sub>SCB 10X</sub> | Large language models tuned for Thai, with an OpenAI-compatible API | free sign-up | ✅ |

### Messaging and payments

| API | What it gives you | Key | Working |
|---|---|---|---|
| [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)<br><sub>LINE</sub> | Build LINE bots and message your LINE Official Account's users | free sign-up | ✅ |
| [Opn Payments (Omise)](https://www.omise.co/docs)<br><sub>Opn</sub> | Accept cards, PromptPay, mobile banking and TrueMoney. Test keys available | paid | ✅ |
| [SCB Open API](https://developer.scb/)<br><sub>SCB</sub> | QR payments, slip verification and other banking services, with a sandbox | free sign-up | ✅ |
| [KBank API](https://apiportal.kasikornbank.com/)<br><sub>KBank</sub> | QR payments, slip verification and other banking services, with a sandbox | free sign-up | ✅ |

¹ Works, but the server sends an incomplete certificate chain. Browsers and curl cope; Python, Java and many HTTP clients fail with `CERTIFICATE_VERIFY_FAILED`. Add the intermediate certificate to your CA bundle rather than turning verification off.
<!-- apis:end -->

## Reading the "Working" column

- **✅** reachable and, for keyless APIs, the response still has the expected shape
- **⚠️** unreachable or the response changed, with what was seen
- Checks run from GitHub's servers outside Thailand. Some government sites block foreign traffic, so if you see ⚠️, try from a machine in Thailand.
- For APIs that need a key, only the documentation page is checked.

## As data

Everything is in [`apis.json`](apis.json) (names, descriptions, docs, auth, examples) and the latest results in [`status.json`](status.json).

## Add an API

Pull requests welcome:

1. Add it to [`apis.json`](apis.json) with Thai and English descriptions, and a `check.expect` string for keyless APIs.
2. Run `python3 check.py --update` and confirm it's ✅.
3. Public or open-sign-up APIs only, not internal endpoints scraped from a website.

Wanted: official lottery results, Gold Traders Association prices, train timetables, power outages, keyless exchange rates.

## Run it yourself

```sh
python3 check.py            # check everything
python3 check.py --update   # check and rewrite both READMEs and status.json
python3 check.py --test     # self-check, no network
```

Python standard library only.

## License

MIT
