-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-05-2024 a las 17:54:12
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestionar`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_tarea` int(6) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `fechainicio` datetime DEFAULT NULL,
  `fechafinal` datetime DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `id_user` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_tarea`, `nombre`, `fechainicio`, `fechafinal`, `estado`, `id_user`) VALUES
(1, 'Programar', '2024-05-14 00:00:00', '2024-05-15 00:00:00', 'en_progreso', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_user` int(6) NOT NULL,
  `nombre_user` varchar(100) DEFAULT NULL,
  `apellido_user` varchar(100) DEFAULT NULL,
  `email_user` varchar(100) DEFAULT NULL,
  `usuario_user` varchar(100) DEFAULT NULL,
  `contraseña_user` varchar(255) DEFAULT NULL,
  `rol_user` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_user`, `nombre_user`, `apellido_user`, `email_user`, `usuario_user`, `contraseña_user`, `rol_user`) VALUES
(1, 'Aria', 'hiromori', 'arita@gmail.com', 'arita', 'scrypt:32768:8:1$y0yR2RDgkE7jkZRR$e57d21d7e564a7941e5d09b0083a18fd1e90a084ff98f4baede80706122c4518174baab84924b7fac3e36e5684b6677221195a316bdb7c7bb4ef4f400ab9097d', 'administrador'),
(2, 'juan', 'garcia', 'garciatroll@gmail.com', 'juanito', 'scrypt:32768:8:1$HrJxCc6K3I27IYD0$f4142e00c25e85d5c113446a07b79ebd31073d8aa56b294cbc806e813e30062fabe6b9810902b603bca51ca6dca470791769dbe995c2cef94244be4c8c727f30', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `fk_id1` (`id_user`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_tarea` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_user` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `fk_id1` FOREIGN KEY (`id_user`) REFERENCES `usuario` (`id_user`);
COMMIT;

use gestionar

SELECT * FROM tareas WHERE id_tarea = 4 OR nombre LIKE "Programar"

SELECT * FROM tareas WHERE (id_tarea = 8 OR nombre LIKE "Jugar Halo") AND id_user = 2

SELECT id_user FROM usuario WHERE usuario_user = "juanito";
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
