-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 29 Bulan Mei 2025 pada 03.37
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kursus`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `instruktur`
--

CREATE TABLE `instruktur` (
  `ID_Instruktur` int(11) NOT NULL,
  `Nama_Instruktur` varchar(100) NOT NULL,
  `Email_Instruktur` varchar(100) NOT NULL,
  `Bidang_keahlian` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `instruktur`
--

INSERT INTO `instruktur` (`ID_Instruktur`, `Nama_Instruktur`, `Email_Instruktur`, `Bidang_keahlian`) VALUES
(201, 'Dr. Siti Rahma', 'siti.rahma@email.com', 'Pemrograman'),
(202, 'Prof. Agus Salim', 'agus.salim@email.com', 'Basis Data'),
(203, 'Dr. Rina Kartika', 'rina.kartika@email.com', 'Algoritma & Struktur Data'),
(204, 'Prof. Bambang Sudirman', 'bambang.sudirman@email.com', 'Jaringan Komputer');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kursus`
--

CREATE TABLE `kursus` (
  `ID_Kursus` int(11) NOT NULL,
  `Nama_Kursus` varchar(100) NOT NULL,
  `Daya_Tampung` int(11) NOT NULL,
  `Deskripsi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kursus`
--

INSERT INTO `kursus` (`ID_Kursus`, `Nama_Kursus`, `Daya_Tampung`, `Deskripsi`) VALUES
(101, 'Pemrograman Web', 30, 'Belajar HTML, CSS, dan JavaScript'),
(102, 'Basis Data', 25, 'Belajar SQL dan manajemen database'),
(103, 'Struktur Data', 40, 'Belajar algoritma dan struktur data'),
(104, 'Jaringan Komputer', 35, 'Dasar komunikasi jaringan dan keamanan');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `id_mahasiswa` int(11) NOT NULL,
  `nama_mahasiswa` varchar(100) NOT NULL,
  `email_mahasiswa` varchar(100) NOT NULL,
  `program_studi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mahasiswa`
--

INSERT INTO `mahasiswa` (`id_mahasiswa`, `nama_mahasiswa`, `email_mahasiswa`, `program_studi`) VALUES
(12, 'alana don', 'don', 'jaringan');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mendaftar`
--

CREATE TABLE `mendaftar` (
  `kode` int(11) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `periode` int(11) NOT NULL,
  `nilai` int(3) NOT NULL,
  `id_kursusFK` int(11) DEFAULT NULL,
  `id_mhsFK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mendaftar`
--

INSERT INTO `mendaftar` (`kode`, `tanggal_mulai`, `periode`, `nilai`, `id_kursusFK`, `id_mhsFK`) VALUES
(16, '2025-05-25', 4, 0, 102, 12);

-- --------------------------------------------------------

--
-- Struktur dari tabel `mengampu`
--

CREATE TABLE `mengampu` (
  `id_instruktur` int(11) NOT NULL,
  `id_kursus` int(11) NOT NULL,
  `peran` varchar(50) DEFAULT NULL,
  `gaji` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mengampu`
--

INSERT INTO `mengampu` (`id_instruktur`, `id_kursus`, `peran`, `gaji`) VALUES
(201, 104, 'Pengajar utama', 5000000.00),
(202, 101, 'Pengajar utama', 5000000.00),
(203, 102, 'Pengajar utama', 5000000.00),
(204, 103, 'Pengajar utama', 5000000.00);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `instruktur`
--
ALTER TABLE `instruktur`
  ADD PRIMARY KEY (`ID_Instruktur`),
  ADD UNIQUE KEY `Email_Instruktur` (`Email_Instruktur`);

--
-- Indeks untuk tabel `kursus`
--
ALTER TABLE `kursus`
  ADD PRIMARY KEY (`ID_Kursus`);

--
-- Indeks untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`id_mahasiswa`),
  ADD UNIQUE KEY `Email_Mahasiswa` (`email_mahasiswa`);

--
-- Indeks untuk tabel `mendaftar`
--
ALTER TABLE `mendaftar`
  ADD PRIMARY KEY (`kode`),
  ADD KEY `id_kursusFK` (`id_kursusFK`),
  ADD KEY `NIM_FK` (`id_mhsFK`);

--
-- Indeks untuk tabel `mengampu`
--
ALTER TABLE `mengampu`
  ADD PRIMARY KEY (`id_instruktur`,`id_kursus`),
  ADD KEY `id_kursus` (`id_kursus`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  MODIFY `id_mahasiswa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT untuk tabel `mendaftar`
--
ALTER TABLE `mendaftar`
  MODIFY `kode` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `mendaftar`
--
ALTER TABLE `mendaftar`
  ADD CONSTRAINT `NIM_FK` FOREIGN KEY (`id_mhsFK`) REFERENCES `mahasiswa` (`id_mahasiswa`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `id_kursusFK` FOREIGN KEY (`id_kursusFK`) REFERENCES `kursus` (`ID_Kursus`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `mengampu`
--
ALTER TABLE `mengampu`
  ADD CONSTRAINT `mengampu_ibfk_1` FOREIGN KEY (`id_instruktur`) REFERENCES `instruktur` (`ID_Instruktur`),
  ADD CONSTRAINT `mengampu_ibfk_2` FOREIGN KEY (`id_kursus`) REFERENCES `kursus` (`ID_Kursus`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
