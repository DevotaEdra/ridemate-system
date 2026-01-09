# RideMate System

RideMate adalah sistem penyewaan kendaraan berbasis **microservices** yang dibangun untuk memenuhi Tugas Besar mata kuliah **Integrasi Aplikasi Enterprise (IAE)**. Sistem ini berfokus pada manajemen identitas pelanggan dan transaksi booking, serta terintegrasi dengan layanan armada eksternal (lintas kelompok) menggunakan **GraphQL**.

---

## 🧩 Arsitektur Sistem

RideMate menerapkan arsitektur **Microservices** dengan pemisahan tanggung jawab sebagai berikut:

1. **User Service**
   Mengelola autentikasi, identitas pengguna, dan reputasi user.

2. **Booking Service**
   Mengelola transaksi penyewaan kendaraan dan orkestrasi proses booking.

3. **External Fleet Service (AutoLink Provider)**
   Layanan eksternal (lintas kelompok) yang menyediakan data kendaraan dan validasi ketersediaan.

Setiap service memiliki database terpisah dan dijalankan dalam container Docker yang berbeda.

---

## 📦 Struktur Folder

```ridemate-system/
│
├── booking-service/
│ ├── app/
│ │ ├── schema/
│ │ │ ├── __init__.py
│ │ │ ├── resolvers.py
│ │ │ └── schema.graphql
│ │ ├── __init__.py
│ │ ├── database.py
│ │ ├── fleet_client.py
│ │ ├── user_client.py
│ │ ├── main.py
│ │ └── models.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── user-service/
│ ├── app/
│ │ ├── schema/
│ │ │ ├── __init__.py
│ │ │ ├── resolvers.py
│ │ │ └── schema.graphql
│ │ ├── utils/
│ │ │ ├── __init__.py
│ │ │ └── jwt.py
│ │ ├── auth.py
│ │ ├── database.py
│ │ ├── main.py
│ │ └── models.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## 🔐 Mekanisme Keamanan (JWT)

* Autentikasi dilakukan **hanya melalui User Service**.
* User Service menghasilkan **JWT (JSON Web Token)** saat login.
* Booking Service **tidak menyimpan data user atau password**.
* Setiap request ke Booking Service wajib menyertakan token JWT.
* Validasi token dilakukan dengan memanggil endpoint validasi milik User Service (centralized token validation).

---

## 🔗 Kontrak GraphQL

### User Service

```graphql
type Query {
  me: User
  checkUserReputation(userId: ID!): Reputation
}

type Mutation {
  login(email: String!, password: String!): Token
}
```

### Booking Service

```graphql
type Query {
  myBookings: [Booking!]
}

type Mutation {
  createBooking(vehicleId: ID!, date: String!): Booking
}
```

---

## 🔄 Alur Booking

1. User melakukan login ke **User Service** dan mendapatkan JWT.
2. User mengirim request booking ke **Booking Service** dengan JWT.
3. Booking Service memvalidasi token ke User Service.
4. Booking Service memanggil **External Fleet Service** untuk mengecek ketersediaan kendaraan.
5. Jika kendaraan tersedia, booking disimpan ke database.
6. Jika tidak tersedia, sistem mengembalikan error.

---

## 🐳 Deployment dengan Docker

Seluruh service dijalankan menggunakan **Docker Compose**.

### Menjalankan Aplikasi

```bash
docker-compose up --build
```

### Menghentikan Aplikasi

```bash
docker-compose down
```

Pastikan Docker dan Docker Compose telah terinstal.

---

## 🧪 Pengujian

Beberapa skenario pengujian utama:

1. Login berhasil dan menghasilkan JWT.
2. Request booking dengan token valid dan kendaraan tersedia.
3. Request booking gagal jika kendaraan tidak tersedia.
4. Request booking gagal jika token tidak valid.
5. Container Docker berjalan dengan normal.

---

## 👥 Tim Pengembang

* **Devota Edra Athaloma (102022300344)**
  Service: User Service

* **Yudistira Sebastian Saftari (102022300313)**
  Service: Booking Service

---

## 📌 Catatan

Sistem ini dikembangkan untuk keperluan akademik dan demonstrasi integrasi aplikasi enterprise, khususnya penggunaan GraphQL, JWT, Docker, dan integrasi lintas kelompok berbasis microservices.

---

✅ **RideMate System – Integrasi Sederhana, Arsitektur Terstruktur**
