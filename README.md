# awesome-thai-api

[English](README.en.md) · จากคนทำ [thaiproof](https://github.com/nuttakulsv/thaiproof) และ [thai-id-card-kit](https://github.com/nuttakulsv/thai-id-card-kit)

รวม API ของไทยที่ใช้ได้จริง ทั้งของหน่วยงานรัฐและบริษัทที่นักพัฒนาไทยใช้กันบ่อย เช่น ค่าฝุ่น PM2.5 ราคาน้ำมันวันนี้ แผ่นดินไหว ระดับน้ำ ตรวจเลขผู้เสียภาษี และข้อมูลเปิดภาครัฐ

ลิสต์ API ไทยส่วนใหญ่ที่เจอในเน็ตมักลิงก์เสียไปครึ่งหนึ่งแล้ว ลิสต์นี้ต่างตรงที่**มีสคริปต์เรียกทุก API ให้ทุกวัน** แล้วอัปเดตคอลัมน์ "ใช้ได้ไหม" ให้เอง ตัวที่ไม่ต้องใช้ key จะตรวจถึงขั้นว่าข้อมูลที่ตอบกลับมายังหน้าตาเหมือนเดิม และทุกตัวที่ไม่ต้องใช้ key มีตัวอย่าง `curl` ให้ลองได้ทันที

<!-- apis:start -->
_ตรวจล่าสุด 2026-11-06 (UTC) จากเซิร์ฟเวอร์ของ GitHub ในต่างประเทศ_

### สภาพอากาศและภัยพิบัติ

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [TMD Earthquake feed](https://earthquake.tmd.go.th/)<br><sub>กรมอุตุนิยมวิทยา</sub> | รายการแผ่นดินไหวล่าสุดในไทยและภูมิภาค เป็น RSS | ไม่ต้องใช้ key | ✅ |
| [TMD Weather API](https://data.tmd.go.th/api/index1.php)<br><sub>กรมอุตุนิยมวิทยา</sub> | อากาศรายวัน พยากรณ์ 7 วัน ประกาศเตือนภัย ปริมาณฝน แผ่นดินไหว (XML) เอกสารมี uid/ukey ตัวอย่างให้ลอง ใช้จริงควรสมัคร key เอง | สมัครฟรี | ✅ |
| [TMD NWP Forecast API](https://data.tmd.go.th/nwpapi/doc/)<br><sub>กรมอุตุนิยมวิทยา</sub> | พยากรณ์อากาศเชิงตัวเลขรายชั่วโมงและรายวัน ระบุพิกัดหรือจังหวัดได้ (JSON) | สมัครฟรี | ✅ |

<details><summary>ตัวอย่างการเรียก</summary>

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

### คุณภาพอากาศและฝุ่น PM2.5

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [Air4Thai](https://air4thai.pcd.go.th/webV3/)<br><sub>กรมควบคุมมลพิษ</sub> | ค่า AQI, PM2.5, PM10, O3, CO, NO2 ล่าสุดจากสถานีตรวจวัดทั่วประเทศ | ไม่ต้องใช้ key | ✅ ¹ |
| [GISTDA PM2.5](https://pm25.gistda.or.th/)<br><sub>GISTDA</sub> | ค่าฝุ่น PM2.5 รายจังหวัดจากข้อมูลดาวเทียม รวมค่าเฉลี่ย 24 ชั่วโมง | ไม่ต้องใช้ key | ✅ |

<details><summary>ตัวอย่างการเรียก</summary>

**Air4Thai**

```sh
curl -s https://air4thai.pcd.go.th/services/getNewAQI_JSON.php
```

**GISTDA PM2.5**

```sh
curl -s https://pm25.gistda.or.th/rest/getPm25byProvince
```

</details>

### น้ำและน้ำท่วม

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [ThaiWater](https://www.thaiwater.net/)<br><sub>สถาบันสารสนเทศทรัพยากรน้ำ</sub> | ระดับน้ำ ปริมาณน้ำในเขื่อน และสถานการณ์น้ำจากสถานีโทรมาตรทั่วประเทศ | ไม่ต้องใช้ key | ✅ |

<details><summary>ตัวอย่างการเรียก</summary>

**ThaiWater**

```sh
curl -s https://api-v3.thaiwater.net/api/v1/thaiwater30/public/waterlevel_load
```

</details>

### ราคาน้ำมัน

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [PTT OR Oil Price](https://orapiweb.pttor.com/oilservice/OilPrice.asmx)<br><sub>ปตท. น้ำมันและการค้าปลีก</sub> | ราคาน้ำมันขายปลีกวันนี้ของ PTT Station (SOAP) | ไม่ต้องใช้ key | ✅ |
| [Bangchak Oil Price](https://www.bangchak.co.th/th/oilprice)<br><sub>บางจาก คอร์ปอเรชั่น</sub> | ราคาน้ำมันวันนี้และพรุ่งนี้ของบางจาก (JSON) | ไม่ต้องใช้ key | ✅ |

<details><summary>ตัวอย่างการเรียก</summary>

**PTT OR Oil Price**

```sh
curl -s https://orapiweb.pttor.com/oilservice/OilPrice.asmx -H 'Content-Type: text/xml; charset=utf-8' -H 'SOAPAction: "http://www.pttor.com/CurrentOilPrice"' -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><CurrentOilPrice xmlns="http://www.pttor.com"><Language>TH</Language></CurrentOilPrice></soap:Body></soap:Envelope>'
```

**Bangchak Oil Price**

```sh
curl -s https://oil-price.bangchak.co.th/ApiOilPrice2/th
```

</details>

### การเงินและอัตราแลกเปลี่ยน

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [BOT API](https://portal.api.bot.or.th/)<br><sub>ธนาคารแห่งประเทศไทย</sub> | อัตราแลกเปลี่ยน อัตราดอกเบี้ย วันหยุดสถาบันการเงิน และสถิติเศรษฐกิจ สมัครฟรีที่ API portal | สมัครฟรี | ✅ |
| [Bitkub Public API](https://github.com/bitkub/bitkub-official-api-docs)<br><sub>Bitkub</sub> | ราคาคริปโตเป็นเงินบาท (ticker, order book, trades) ส่วนที่เป็น public ไม่ต้องใช้ key | ไม่ต้องใช้ key | ✅ |

<details><summary>ตัวอย่างการเรียก</summary>

**Bitkub Public API**

```sh
curl -s 'https://api.bitkub.com/api/v3/market/ticker?sym=btc_thb'
```

</details>

### ภาษีและข้อมูลธุรกิจ

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [RD VAT Service](https://rdws.rd.go.th/serviceRD3/vatserviceRD3.asmx)<br><sub>กรมสรรพากร</sub> | ตรวจสอบผู้ประกอบการจดทะเบียนภาษีมูลค่าเพิ่มจากเลขประจำตัวผู้เสียภาษี ได้ชื่อและที่อยู่ (SOAP, username/password เป็น anonymous) | ไม่ต้องใช้ key | ✅ |
| [DBD Open Data](https://opendata.dbd.go.th/)<br><sub>กรมพัฒนาธุรกิจการค้า</sub> | ข้อมูลนิติบุคคล งบการเงิน และสถิติธุรกิจ บางชุดต้องสมัคร | สมัครฟรี | 🇹🇭 ² |

<details><summary>ตัวอย่างการเรียก</summary>

**RD VAT Service**

```sh
curl -s https://rdws.rd.go.th/serviceRD3/vatserviceRD3.asmx -H 'Content-Type: text/xml; charset=utf-8' -H 'SOAPAction: "https://rdws.rd.go.th/serviceRD3/vatserviceRD3/Service"' -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Service xmlns="https://rdws.rd.go.th/serviceRD3/vatserviceRD3"><username>anonymous</username><password>anonymous</password><TIN>TAX_ID_13_DIGITS</TIN><ProvinceCode>0</ProvinceCode><BranchNumber>0</BranchNumber><AmphurCode>0</AmphurCode></Service></soap:Body></soap:Envelope>'
```

</details>

### ข้อมูลเปิดภาครัฐ

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [data.go.th (CKAN)](https://data.go.th/)<br><sub>สำนักงานพัฒนารัฐบาลดิจิทัล</sub> | ค้นชุดข้อมูลเปิดภาครัฐกว่า 40,000 ชุด ผ่าน CKAN API มาตรฐาน | ไม่ต้องใช้ key | 🇹🇭 ² |
| [Bangkok Open Data (CKAN)](https://data.bangkok.go.th/)<br><sub>กรุงเทพมหานคร</sub> | ชุดข้อมูลเปิดของกรุงเทพฯ เช่น จุดเสี่ยงน้ำท่วม กล้อง CCTV สวนสาธารณะ ผ่าน CKAN API | ไม่ต้องใช้ key | 🇹🇭 ² |

<details><summary>ตัวอย่างการเรียก</summary>

**data.go.th (CKAN)**

```sh
curl -sG https://data.go.th/api/3/action/package_search --data-urlencode q=โรงพยาบาล -d rows=5
```

**Bangkok Open Data (CKAN)**

```sh
curl -sG https://data.bangkok.go.th/api/3/action/package_search --data-urlencode q=สวนสาธารณะ -d rows=5
```

</details>

### แผนที่และขนส่ง

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [Longdo Map API](https://map.longdo.com/api)<br><sub>Metamedia Technology</sub> | แผนที่ประเทศไทย ค้นหาสถานที่ แปลงที่อยู่เป็นพิกัด และเส้นทาง มี free tier | สมัครฟรี | ✅ |
| [Thailand Post Track & Trace API](https://track.thailandpost.co.th/developerGuide)<br><sub>ไปรษณีย์ไทย</sub> | ติดตามสถานะพัสดุด้วยเลขพัสดุ สมัครรับ token ฟรี | สมัครฟรี | ✅ |

### ภาษาไทยและ AI

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [AI for Thai](https://www.aiforthai.in.th/)<br><sub>NECTEC</sub> | ตัดคำ แปลภาษา แปลงเสียงเป็นข้อความ อ่านออกเสียงภาษาไทย OCR และอื่นๆ สมัคร key ฟรี | สมัครฟรี | ✅ |
| [Typhoon](https://opentyphoon.ai/)<br><sub>SCB 10X</sub> | โมเดลภาษาขนาดใหญ่ที่เก่งภาษาไทย เรียกผ่าน API แบบเดียวกับ OpenAI | สมัครฟรี | ✅ |

### แชตและการชำระเงิน

| API | ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |
|---|---|---|---|
| [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)<br><sub>LINE</sub> | ทำ LINE bot และส่งข้อความหาผู้ใช้ LINE OA | สมัครฟรี | ✅ |
| [Opn Payments (Omise)](https://www.omise.co/docs)<br><sub>Opn</sub> | รับชำระเงินด้วยบัตร PromptPay โมบายแบงกิ้ง และ TrueMoney มี test key ให้ลอง | มีค่าใช้จ่าย | ✅ |
| [SCB Open API](https://developer.scb/)<br><sub>ธนาคารไทยพาณิชย์</sub> | QR payment, ตรวจสลิป และบริการธนาคารอื่นๆ มี sandbox ให้ทดสอบ | สมัครฟรี | ✅ |
| [KBank API](https://apiportal.kasikornbank.com/)<br><sub>ธนาคารกสิกรไทย</sub> | QR payment, ตรวจสลิป และบริการธนาคารอื่นๆ มี sandbox ให้ทดสอบ | สมัครฟรี | ✅ |

¹ ใช้ได้ แต่เซิร์ฟเวอร์ส่งใบรับรอง SSL มาไม่ครบ เบราว์เซอร์กับ curl ไม่มีปัญหา แต่ Python, Java และ HTTP client หลายตัวจะเจอ `CERTIFICATE_VERIFY_FAILED` ให้เพิ่ม intermediate certificate ใน CA bundle เอง อย่าปิดการตรวจใบรับรอง

² เรียกจากต่างประเทศไม่ได้ แต่ใช้ได้เมื่อเรียกจากในไทย (ทดสอบล่าสุด 2026-11-01) ถ้า deploy บน cloud ต่างประเทศ เช่น Vercel หรือ AWS นอก region ไทย ต้องเรียกผ่านเซิร์ฟเวอร์ในไทย
<!-- apis:end -->

## อ่านคอลัมน์ "ใช้ได้ไหม" ยังไง

- **✅** เรียกได้ และ (สำหรับ API ที่ไม่ต้องใช้ key) ข้อมูลที่ได้ยังมีหน้าตาเหมือนเดิม
- **⚠️** เรียกไม่ได้ หรือข้อมูลเปลี่ยนรูปแบบไปแล้ว พร้อมบอกว่าเจออะไร
- **🇹🇭** บล็อกการเรียกจากต่างประเทศ ใช้ได้เฉพาะจากในไทย สคริปต์รันจากเซิร์ฟเวอร์ของ GitHub ที่อยู่ต่างประเทศ เลยบอกได้แค่ว่าโดนบล็อก ส่วนวันที่ทดสอบจากในไทยล่าสุดอยู่ในหมายเหตุใต้ตาราง
- ถ้าเห็น ⚠️ กับ API ของรัฐตัวอื่น อาจโดนบล็อกแบบเดียวกัน ให้ลองเรียกจากเครื่องในไทยอีกที
- API ที่ต้องสมัคร key จะตรวจแค่ว่าหน้าเอกสารยังเปิดได้

## ใช้งานแบบไม่ต้องอ่าน README

ข้อมูลทั้งหมดอยู่ใน [`apis.json`](apis.json) ชื่อ คำอธิบาย ลิงก์เอกสาร ต้องใช้ key ไหม และตัวอย่างการเรียก ส่วนผลตรวจล่าสุดอยู่ใน [`status.json`](status.json) เอาไปใช้ต่อได้เลย

```sh
curl -s https://raw.githubusercontent.com/nuttakulsv/awesome-thai-api/main/apis.json
```

## เพิ่ม API

ส่ง PR มาได้เลย ขอแค่

1. เพิ่มรายการใน [`apis.json`](apis.json) ใส่คำอธิบายทั้งไทยและอังกฤษ และใส่ `check.expect` เป็นข้อความที่ต้องเจอในผลลัพธ์ (ถ้าไม่ต้องใช้ key)
2. รัน `python3 check.py --update` แล้วดูว่าตัวที่เพิ่มขึ้น ✅
3. เป็น API ที่คนทั่วไปใช้ได้จริง เปิดสาธารณะหรือสมัครได้ ไม่ใช่ API ภายในที่แอบดึงมาจากหน้าเว็บ

อยากได้เพิ่ม: ผลสลากกินแบ่งรัฐบาลแบบทางการ, ราคาทองคำจากสมาคมค้าทองคำ, ตารางรถไฟ, ข้อมูลไฟดับ, อัตราแลกเปลี่ยนที่ไม่ต้องใช้ key ถ้ารู้ว่ามี API ทางการ บอกได้เลย

## รันเอง

```sh
python3 check.py            # ตรวจทุกตัว แสดงเป็นตาราง
python3 check.py --update   # ตรวจแล้วเขียนผลลง README ทั้งสองภาษาและ status.json
python3 check.py --test     # เทสต์ (ไม่ต่อเน็ต)
```

ใช้แค่ standard library ของ Python

## License

MIT
