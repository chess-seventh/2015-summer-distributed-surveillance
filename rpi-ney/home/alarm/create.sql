CREATE TABLE `humidity_events` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `value` decimal(10,2) NOT NULL
);

CREATE TABLE `luminosity_events` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `value` decimal(10,2) NOT NULL
);

CREATE TABLE `pir_events` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `value` tinyint(1) NOT NULL
);

CREATE TABLE `temperature_events` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `value` decimal(10,2) NOT NULL
);

CREATE TABLE `video_events` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `stopped_at` datetime DEFAULT NULL,
  `video_key` varchar(32) NOT NULL
);


ALTER TABLE `humidity_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`,`created_at`);

ALTER TABLE `luminosity_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`,`created_at`);

ALTER TABLE `pir_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`,`created_at`);

ALTER TABLE `temperature_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`,`created_at`);

ALTER TABLE `video_events`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `video_key` (`video_key`),
  ADD KEY `device_id` (`device_id`,`created_at`,`stopped_at`);


ALTER TABLE `humidity_events`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `luminosity_events`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `pir_events`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `temperature_events`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `video_events`
  MODIFY `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
