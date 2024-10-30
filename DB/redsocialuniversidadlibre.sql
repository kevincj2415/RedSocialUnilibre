-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-10-2024 a las 22:57:19
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
-- Base de datos: `redsocialuniversidadlibre`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensaje`
--

CREATE TABLE `mensaje` (
  `id` int(11) NOT NULL,
  `emisor_id` int(11) DEFAULT NULL,
  `receptor_id` int(11) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `fecha_envio` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `muro`
--

CREATE TABLE `muro` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `publicacion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisomensaje`
--

CREATE TABLE `permisomensaje` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `emisor_id` int(11) DEFAULT NULL,
  `permiso` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicacion`
--

CREATE TABLE `publicacion` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `privacidad` enum('Publico','Privado') DEFAULT NULL,
  `fecha_publicacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('Estudiante','Profesor','Directivo','Administrador') DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `contraseña`, `rol`, `foto_perfil`, `fecha_registro`) VALUES
(7, 'kevin jose garcia carvajal ', 'kevinj-garciac@unilibre.edu.co', 'scrypt:32768:8:1$g0LQQEWhotpJOrNF$ce175adc9ec85a622dfd4458600a0a0f3cab064534e878cadd45b36dd9491b650c0020c20794560d9db3bc49363389979ceed4e27aaae3c1964ceb2fbc173397', 'Estudiante', 'https://via.placeholder.com/150', '2024-10-06 19:10:32'),
(8, 'juan manuel', 'juanma@gmail.com', 'scrypt:32768:8:1$f1M80u0TVMIY8SpF$62baffb2f48a1412cd37fceceaede8d75c967b0ed4c1bf2acfbeeac4b67157cf8239e18db632de3c7061c57e0625799d3d6bb3c8d1f15c21c889eb2115ae71ae', 'Estudiante', 'https://via.placeholder.com/150', '2024-10-06 19:18:33'),
(9, 'alex martinez', 'alex@gmail.com', 'scrypt:32768:8:1$aqvNNmM4w2BlDKlM$f2deaea10d0a44a5b8ad8625df1f047ed3e84b58e6c580ea2436b5f2ff202370a88eda5fa19c79556592c843a04d90c45af9cd3b488edb48b77057676e89bc54', 'Profesor', 'https://images3.alphacoders.com/135/1350069.jpeg', '2024-10-06 19:19:31'),
(11, 'andres carvajal', 'an@an.com', 'scrypt:32768:8:1$HdeY7Df550y7NU5v$ac76bcb6e5a6b295ad8544e9cd897a5974ca8ec65b5fd2d5a51ee165238a111820b211018de2359e0d6e93d0846f99a2442c1ee256be28cd0b7a905c924e11f8', 'Estudiante', 'https://images.squarespace-cdn.com/content/v1/5fe4caeadae61a2f19719512/90b2b60d-1dbb-4e7e-9f20-6eb315d2740b/Space', '2024-10-15 22:34:54'),
(12, 'alexander grajam', 'ale@ale.com', 'scrypt:32768:8:1$HqbnKxluMDwnWm9a$52a8d4b58b4da9820c9fd5a5a62148f08ab6a2b4582c45c2e054b00e13b38b5e607ca2704eab34e76df4d340b48c3dcd90e8fe2aa622719af3c600693a21c671', 'Administrador', 'https://i.imgur.com/5fQUPDl.jpg', '2024-10-19 22:41:54'),
(13, 'alexander gram', 'ag@ag.com', 'scrypt:32768:8:1$vnGM1is9J9tSYVPo$c9a2c878a3908ed22c0ca8a15d23a4de70e3fdb8085d56c91ddd83b01cbef17061ec0ac3e50d13b4b56549b65950271ab7bfd7f9aff3a9c5949e366a65309032', 'Estudiante', 'https://via.placeholder.com/150', '2024-10-19 22:42:18'),
(15, 'KJGC', 'kj@kj.com', 'scrypt:32768:8:1$51lBuJ0CGquZc8GX$4f961da1302b1e4217c2c02f9f8e58c4df98760d902702d76270806f9e27bf3d4f3ce43bfee9c7a7b6f4c196719d84d4ddc0b326937b96faf6e7ce076faddcd7', 'Administrador', 'https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg?cs=srgb&dl=pexels-veeterzy-39811.jpg&fm=jpg', '2024-10-19 23:39:33'),
(16, 'Adiran Martinez', 'ad@ad.com', 'scrypt:32768:8:1$YuBI1omT4boFBBqP$97bb7cf22a9ad7b9d272b0f3d6fdc6b976387611137838443134c0d4a37c947d4134358e5bf6eeff781b26b6ebbc66491f2ec61cc600781682246f384fe05b73', 'Administrador', 'https://images3.alphacoders.com/135/1350069.jpeg', '2024-10-23 19:02:33'),
(17, 'Kevin', 'ke@ke.com', 'scrypt:32768:8:1$6XRHe9qRi3KoCDcE$eaefb37d3bb83e78b5b40830e119fba7d2364eb29c0a9fd588c01315f17030477901d837fbfe4997751d8000b2f9f7ef75729cc79a82269f7802fd20c1d9b4bc', 'Directivo', 'https://4kwallpapers.com/images/walls/thumbs_2t/17525.jpg', '2024-10-23 19:07:04'),
(18, 'Marta Martines', 'ma@ma.com', 'scrypt:32768:8:1$TEevaIcQw64pINnd$0909c82a7d275c341a5fffc4328856a50b93c841671add08a93376e69ef2704e5bcc0151401d36d8bed9677b5559b24cff6ec6b6dbdd56501fd55d858383cb93', 'Estudiante', 'https://i.imgur.com/5fQUPDl.jpg', '2024-10-30 20:48:16'),
(19, 'Paul', 'pa@pa.com', 'scrypt:32768:8:1$AHgbftnWjv2uSI46$b3a479a6eb707606af20ddc17e3d08ebc4047cc6a74fed49246d1598cb4dc96233014efa394425ee50d803987056b88c2466bf38e22fb64b4eaaa8d3aca10bf0', 'Administrador', 'https://via.placeholder.com/150', '2024-10-30 21:24:04');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `emisor_id` (`emisor_id`),
  ADD KEY `receptor_id` (`receptor_id`);

--
-- Indices de la tabla `muro`
--
ALTER TABLE `muro`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `publicacion_id` (`publicacion_id`);

--
-- Indices de la tabla `permisomensaje`
--
ALTER TABLE `permisomensaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `emisor_id` (`emisor_id`);

--
-- Indices de la tabla `publicacion`
--
ALTER TABLE `publicacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `muro`
--
ALTER TABLE `muro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `permisomensaje`
--
ALTER TABLE `permisomensaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `publicacion`
--
ALTER TABLE `publicacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `mensaje`
--
ALTER TABLE `mensaje`
  ADD CONSTRAINT `mensaje_ibfk_1` FOREIGN KEY (`emisor_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `mensaje_ibfk_2` FOREIGN KEY (`receptor_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `muro`
--
ALTER TABLE `muro`
  ADD CONSTRAINT `muro_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `muro_ibfk_2` FOREIGN KEY (`publicacion_id`) REFERENCES `publicacion` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `permisomensaje`
--
ALTER TABLE `permisomensaje`
  ADD CONSTRAINT `permisomensaje_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `permisomensaje_ibfk_2` FOREIGN KEY (`emisor_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `publicacion`
--
ALTER TABLE `publicacion`
  ADD CONSTRAINT `publicacion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
