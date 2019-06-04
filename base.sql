-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Mar 04 Juin 2019 à 07:54
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `android_chat`
--

-- --------------------------------------------------------

--
-- Structure de la table `conversations`
--

CREATE TABLE `conversations` (
  `id` int(11) NOT NULL COMMENT 'Clé primaire',
  `active` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'indique si la conversation est active',
  `theme` varchar(40) NOT NULL COMMENT 'Thème de la conversation'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `conversations`
--

INSERT INTO `conversations` (`id`, `active`, `theme`) VALUES
(12, 1, 'Les cours en IAM'),
(2, 1, 'Ballon d\'Or');

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL COMMENT 'Identifiant du message',
  `idConversation` int(11) NOT NULL COMMENT 'Clé étrangère vers la table des conversations',
  `idAuteur` int(11) NOT NULL COMMENT 'clé étrangère vers la table des auteurs',
  `contenu` varchar(100) NOT NULL COMMENT 'Contenu du message'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `messages`
--

INSERT INTO `messages` (`id`, `idConversation`, `idAuteur`, `contenu`) VALUES
(3, 2, 1, 'D\'après vous, qui sera ballon d\'Or ?'),
(35, 12, 1, 'Que pensez-vous des cours en IAM ?');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL COMMENT 'clé primaire, identifiant numérique auto incrémenté',
  `pseudo` varchar(20) NOT NULL COMMENT 'pseudo',
  `passe` varchar(200) NOT NULL COMMENT 'mot de passe',
  `blacklist` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'indique si l''utilisateur est en liste noire',
  `admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'indique si l''utilisateur est un administrateur',
  `connecte` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'indique si l''utilisateur est connecte',
  `couleur` varchar(10) NOT NULL DEFAULT 'black' COMMENT 'indique la couleur préférée de l''utilisateur, en anglais'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Contenu de la table `users`
--

INSERT INTO `users` (`id`, `pseudo`, `passe`, `blacklist`, `admin`, `connecte`, `couleur`) VALUES
(1, 'Tom', 'a75c0838e8467bc03dcdc6f75c12de9c1f825ffc14c859404e1b13fcf5f27b98', 0, 1, 0, '#ff0000'),
(2, 'Jean-Pierre', '35ed65b1eb2e87086e8d7ea0154e88d77febb8fc53af307f2a543b2d44767df0', 0, 0, 0, '#00ff00'),
(3, 'user', '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb', 1, 0, 0, '#0000ff'),
(11, 'Melvin_Harris', 'c45de59d8ce12054569c04487b7a0a0c2c87a9466f9925134926c413790a9e5e', 1, 0, 0, '#000000');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `conversations`
--
ALTER TABLE `conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire', AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant du message', AUTO_INCREMENT=45;
--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'clé primaire, identifiant numérique auto incrémenté', AUTO_INCREMENT=14;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
