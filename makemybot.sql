-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jul 16, 2016 at 08:27 AM
-- Server version: 5.7.9
-- PHP Version: 5.6.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `makemybot`
--

-- --------------------------------------------------------

--
-- Table structure for table `bots`
--

DROP TABLE IF EXISTS `bots`;
CREATE TABLE IF NOT EXISTS `bots` (
  `id` int(10) UNSIGNED NOT NULL,
  `bot_id` int(15) UNSIGNED NOT NULL AUTO_INCREMENT,
  `bot_image` varchar(255) NOT NULL DEFAULT 'bot_default.png',
  `bot_name` varchar(255) NOT NULL DEFAULT 'ChatBot',
  `bot_availability` varchar(255) NOT NULL DEFAULT 'N',
  `bot_views` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`bot_id`) USING BTREE,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chatlogs`
--

DROP TABLE IF EXISTS `chatlogs`;
CREATE TABLE IF NOT EXISTS `chatlogs` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `bot_id` int(10) UNSIGNED NOT NULL,
  `date` date NOT NULL,
  `ip` varchar(32) NOT NULL,
  `log` varchar(4096) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`),
  KEY `bot_id` (`bot_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `knowledge`
--

DROP TABLE IF EXISTS `knowledge`;
CREATE TABLE IF NOT EXISTS `knowledge` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `bot_id` int(10) UNSIGNED NOT NULL,
  `type` varchar(2) NOT NULL,
  `pattern` varchar(512) NOT NULL,
  `template` varchar(4096) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type` (`type`,`pattern`),
  KEY `bot_id` (`bot_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `e-mail` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `knowledge`
--
ALTER TABLE `knowledge` ADD FULLTEXT KEY `pattern` (`pattern`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bots`
--
ALTER TABLE `bots`
  ADD CONSTRAINT `id-foreign-key` FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `chatlogs`
--
ALTER TABLE `chatlogs`
  ADD CONSTRAINT `bot_id-foreign-key-chatlog` FOREIGN KEY (`bot_id`) REFERENCES `bots` (`bot_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `knowledge`
--
ALTER TABLE `knowledge`
  ADD CONSTRAINT `bot_id-foreign-key-knowledge` FOREIGN KEY (`bot_id`) REFERENCES `bots` (`bot_id`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
--
-- Events
--
DROP EVENT `deleteUsers`$$
CREATE DEFINER=`kkm`@`%` EVENT `deleteUsers` ON SCHEDULE EVERY 1 MONTH STARTS '2016-07-16 13:38:14' ON COMPLETION PRESERVE ENABLE COMMENT 'Deletes old user records.' DO DELETE FROM users WHERE date < DATE_SUB(NOW(), INTERVAL 1 YEAR)$$

DROP EVENT `deleteChatlogs`$$
CREATE DEFINER=`kkm`@`%` EVENT `deleteChatlogs` ON SCHEDULE EVERY 1 DAY STARTS '2016-07-16 13:56:48' ON COMPLETION PRESERVE ENABLE COMMENT 'Deletes old chatlogs.' DO DELETE FROM chatlogs WHERE id > 
  ( SELECT MAX(id) FROM 
    ( SELECT id FROM chatlogs ORDER BY date DESC LIMIT 200 )
  AS id)$$

DELIMITER ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
