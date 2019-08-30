-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 30-Ago-2019 às 21:03
-- Versão do servidor: 10.1.38-MariaDB
-- versão do PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uniplacdigital`
--
CREATE DATABASE IF NOT EXISTS `uniplacdigital` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `uniplacdigital`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `category`
--

CREATE TABLE `category` (
  `ID` int(11) NOT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `category`
--

INSERT INTO `category` (`ID`, `Category`, `Description`) VALUES
(1, 'Sistemas de Informação', 'Conteúdo sobtre Sistemas de Informação'),
(2, 'Engenharia', 'Conteúdo sobre Engenharia');

-- --------------------------------------------------------

--
-- Estrutura da tabela `configuration`
--

CREATE TABLE `configuration` (
  `ID` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `UpdatedBy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `configuration`
--

INSERT INTO `configuration` (`ID`, `Name`, `Phone`, `Email`, `CreatedAt`, `UpdatedAt`, `UpdatedBy`) VALUES
(2, 'Uniplac Lages', '9999-9977', 'uniplaclages@email.com', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `configurationimage`
--

CREATE TABLE `configurationimage` (
  `ConfigurationID` int(11) NOT NULL,
  `ImageID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `configurationimage`
--

INSERT INTO `configurationimage` (`ConfigurationID`, `ImageID`) VALUES
(2, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Estrutura da tabela `image`
--

CREATE TABLE `image` (
  `ID` int(11) NOT NULL,
  `ImageData` mediumtext NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `UpdatedBy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `image`
--

INSERT INTO `image` (`ID`, `ImageData`, `CreatedAt`, `UpdatedAt`, `UpdatedBy`) VALUES
(1, 'base64 here', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 1),
(2, 'base64 here', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 2);

-- --------------------------------------------------------

--
-- Estrutura da tabela `post`
--

CREATE TABLE `post` (
  `ID` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Content` text NOT NULL,
  `ImageID` int(11) DEFAULT NULL,
  `EntryDate` datetime NOT NULL,
  `DepartureDate` datetime NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `StatusID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `TypeID` int(11) NOT NULL,
  `CategoryID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `post`
--

INSERT INTO `post` (`ID`, `Title`, `Description`, `Content`, `ImageID`, `EntryDate`, `DepartureDate`, `CreatedAt`, `UpdatedAt`, `StatusID`, `UserID`, `TypeID`, `CategoryID`) VALUES
(3, 'Título 1', 'Descrição 1', 'Conteúdo 1', 1, '2019-08-31 00:00:00', '2019-09-27 00:00:00', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 1, 1, 2, NULL),
(4, 'Título 2', 'Descrição 2', 'Conteúdo 2', 2, '2019-08-30 00:00:00', '2019-10-05 00:00:00', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 2, 2, 3, NULL);

-- --------------------------------------------------------

--
-- Estrutura da tabela `role`
--

CREATE TABLE `role` (
  `ID` int(11) NOT NULL,
  `Role` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `role`
--

INSERT INTO `role` (`ID`, `Role`) VALUES
(1, 'Administrador'),
(2, 'Editor'),
(3, 'Publicador'),
(4, 'Usuário');

-- --------------------------------------------------------

--
-- Estrutura da tabela `status`
--

CREATE TABLE `status` (
  `ID` int(11) NOT NULL,
  `Status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `status`
--

INSERT INTO `status` (`ID`, `Status`) VALUES
(1, 'Publicado'),
(2, 'Em espera');

-- --------------------------------------------------------

--
-- Estrutura da tabela `type`
--

CREATE TABLE `type` (
  `ID` int(11) NOT NULL,
  `Type` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `type`
--

INSERT INTO `type` (`ID`, `Type`) VALUES
(1, 'Anúncio'),
(2, 'Notícia'),
(3, 'Aviso');

-- --------------------------------------------------------

--
-- Estrutura da tabela `user`
--

CREATE TABLE `user` (
  `ID` int(11) NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Registry` varchar(10) NOT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `RoleID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `user`
--

INSERT INTO `user` (`ID`, `FirstName`, `LastName`, `Email`, `Password`, `Registry`, `Phone`, `CreatedAt`, `UpdatedAt`, `RoleID`) VALUES
(1, 'Welison', 'Menezes', 'welisonmenezes@email.com', '123456', '111111', '9999-9999', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 1),
(2, 'Fulano', 'de Tal', 'fulano@email.com', '123456', '121212', '9999-9988', '2019-08-30 00:00:00', '2019-08-30 00:00:00', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `configuration`
--
ALTER TABLE `configuration`
  ADD PRIMARY KEY (`ID`,`UpdatedBy`),
  ADD KEY `fk_Configuration_Users1_idx` (`UpdatedBy`);

--
-- Indexes for table `configurationimage`
--
ALTER TABLE `configurationimage`
  ADD PRIMARY KEY (`ConfigurationID`,`ImageID`),
  ADD KEY `fk_Configuration_has_Images_Images1_idx` (`ImageID`),
  ADD KEY `fk_Configuration_has_Images_Configuration_idx` (`ConfigurationID`);

--
-- Indexes for table `image`
--
ALTER TABLE `image`
  ADD PRIMARY KEY (`ID`,`UpdatedBy`),
  ADD KEY `fk_Images_Users1_idx` (`UpdatedBy`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`ID`,`StatusID`,`UserID`,`TypeID`),
  ADD KEY `fk_Announcements_Statuses1_idx` (`StatusID`),
  ADD KEY `fk_Announcement_User1_idx` (`UserID`),
  ADD KEY `fk_Announcement_Image1_idx` (`ImageID`),
  ADD KEY `fk_Post_PostType1_idx` (`TypeID`),
  ADD KEY `fk_Post_Category1_idx` (`CategoryID`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`,`RoleID`),
  ADD UNIQUE KEY `Registry_UNIQUE` (`Registry`),
  ADD UNIQUE KEY `Email_UNIQUE` (`Email`),
  ADD KEY `fk_Users_Role1_idx` (`RoleID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `configuration`
--
ALTER TABLE `configuration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `image`
--
ALTER TABLE `image`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `type`
--
ALTER TABLE `type`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `configuration`
--
ALTER TABLE `configuration`
  ADD CONSTRAINT `fk_Configuration_Users1` FOREIGN KEY (`UpdatedBy`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `configurationimage`
--
ALTER TABLE `configurationimage`
  ADD CONSTRAINT `fk_Configuration_has_Images_Configuration` FOREIGN KEY (`ConfigurationID`) REFERENCES `configuration` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Configuration_has_Images_Images1` FOREIGN KEY (`ImageID`) REFERENCES `image` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `image`
--
ALTER TABLE `image`
  ADD CONSTRAINT `fk_Images_Users1` FOREIGN KEY (`UpdatedBy`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `fk_Announcement_Image1` FOREIGN KEY (`ImageID`) REFERENCES `image` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Announcement_User1` FOREIGN KEY (`UserID`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Announcements_Statuses1` FOREIGN KEY (`StatusID`) REFERENCES `status` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Post_Category1` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Post_PostType1` FOREIGN KEY (`TypeID`) REFERENCES `type` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_Users_Role1` FOREIGN KEY (`RoleID`) REFERENCES `role` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
