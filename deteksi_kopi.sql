-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2022 at 07:21 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `deteksi_kopi`
--

-- --------------------------------------------------------

--
-- Table structure for table `hasil_panen`
--

CREATE TABLE `hasil_panen` (
  `id_kopi` int(15) NOT NULL,
  `jenis_kopi` varchar(50) NOT NULL,
  `harga` varchar(100) NOT NULL,
  `kuantitas` varchar(100) NOT NULL,
  `waktu` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hasil_panen`
--

INSERT INTO `hasil_panen` (`id_kopi`, `jenis_kopi`, `harga`, `kuantitas`, `waktu`) VALUES
(6, 'robusta', '100000', '20', '0000-00-00'),
(8, 'lampung', '1', '2', '2022-12-02'),
(10, 'kalimantan', '100000', '20', '0000-00-00'),
(13, 'kapal api', '1000', '200', '2022-12-01');

-- --------------------------------------------------------

--
-- Table structure for table `penyakit`
--

CREATE TABLE `penyakit` (
  `nama_penyakit` varchar(100) NOT NULL,
  `ciri` varchar(100) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `deskripsi` text NOT NULL,
  `penanganan` text NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `id_penyakit` int(11) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `penyakit`
--

INSERT INTO `penyakit` (`nama_penyakit`, `ciri`, `url`, `deskripsi`, `penanganan`, `latitude`, `longitude`, `id_penyakit`, `image`) VALUES
('', 'Rust', 'static/miner_7328.jpg', 'blablablalblab', 'nananana', 111, 222, 6, 'miner_7328.jpg'),
('', 'Rust', 'static/miner_73236.jpg', 'blablablalblab', 'nananana', 111, 3333, 7, 'miner_73236.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'aaaaa', '$2b$12$FODUoDzPm16qlK3quB2YTu.ktiH9/Esm/yzGCnn7pAD6HWbAClOj.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hasil_panen`
--
ALTER TABLE `hasil_panen`
  ADD PRIMARY KEY (`id_kopi`);

--
-- Indexes for table `penyakit`
--
ALTER TABLE `penyakit`
  ADD PRIMARY KEY (`id_penyakit`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hasil_panen`
--
ALTER TABLE `hasil_panen`
  MODIFY `id_kopi` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `penyakit`
--
ALTER TABLE `penyakit`
  MODIFY `id_penyakit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
