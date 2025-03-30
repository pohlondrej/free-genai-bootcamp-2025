-- JLPT N5 Adverb Import Script

BEGIN TRANSACTION;

INSERT INTO words (id, word_level, japanese, kana, romaji, english) VALUES
(50001,'N5', 'ちょっと', 'ちょっと', 'chotto', 'a little'),
(50002,'N5', '丁度', 'ちょうど', 'choudo', 'exactly'),
(50003,'N5', 'だんだん', 'だんだん', 'dandan', 'gradually'),
(50004,'N5', 'どう', 'どう', 'dou', 'in what way'),
(50005,'N5', 'どうも', 'どうも', 'doumo', 'thank you'),
(50006,'N5', 'どうして', 'どうして', 'doushite', 'why'),
(50007,'N5', 'どうぞ', 'どうぞ', 'douzo', 'please'),
(50008,'N5', '初めて', 'はじめて', 'hajimete', 'for the first time'),
(50009,'N5', 'いかが', 'いかが', 'ikaga', 'how about'),
(50010,'N5', 'いくら', 'いくら', 'ikura', 'how much'),
(50011,'N5', 'いくつ', 'いくつ', 'ikutsu', 'how many'),
(50012,'N5', '色々', 'いろいろ', 'iroiro', 'various'),
(50013,'N5', '一緒に', 'いっしょに', 'isshoni', 'together'),
(50014,'N5', 'いつも', 'いつも', 'itsumo', 'always'),
(50015,'N5', '結構', 'けっこう', 'kekkou', 'splendid'),
(50016,'N5', 'まだ', 'まだ', 'mada', 'not yet'),
(50017,'N5', '前に', 'まえに', 'maeni', 'before'),
(50018,'N5', '真っ直ぐ', 'まっすぐ', 'massugu', 'straight ahead'),
(50019,'N5', 'もっと', 'もっと', 'motto', 'more'),
(50020,'N5', 'もう', 'もう', 'mou', 'already'),
(50021,'N5', '何故', 'なぜ', 'naze', 'why'),
(50022,'N5', '同じ', 'おなじ', 'onaji', 'same'),
(50023,'N5', '直ぐに', 'すぐに', 'suguni', 'immediately'),
(50024,'N5', '少し', 'すこし', 'sukoshi', 'a little bit'),
(50025,'N5', '多分', 'たぶん', 'tabun', 'probably'),
(50026,'N5', '大変', 'たいへん', 'taihen', 'very'),
(50027,'N5', '時々', 'ときどき', 'tokidoki', 'sometimes'),
(50028,'N5', 'とても', 'とても', 'totemo', 'very'),
(50029,'N5', 'よく', 'よく', 'yoku', 'often'),
(50030,'N5', 'ゆっくり', 'ゆっくり', 'yukkuri', 'slowly');

COMMIT;

-- Add JLPT N5 Adverbs to JLPT N5 Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1001,'word',50001),
(1001,'word',50002),
(1001,'word',50003),
(1001,'word',50004),
(1001,'word',50005),
(1001,'word',50006),
(1001,'word',50007),
(1001,'word',50008),
(1001,'word',50009),
(1001,'word',50010),
(1001,'word',50011),
(1001,'word',50012),
(1001,'word',50013),
(1001,'word',50014),
(1001,'word',50015),
(1001,'word',50016),
(1001,'word',50017),
(1001,'word',50018),
(1001,'word',50019),
(1001,'word',50020),
(1001,'word',50021),
(1001,'word',50022),
(1001,'word',50023),
(1001,'word',50024),
(1001,'word',50025),
(1001,'word',50026),
(1001,'word',50027),
(1001,'word',50028),
(1001,'word',50029),
(1001,'word',50030);

COMMIT;

-- Add JLPT N5 Adverbs to JLPT N5 Words Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1003,'word',50001),
(1003,'word',50002),
(1003,'word',50003),
(1003,'word',50004),
(1003,'word',50005),
(1003,'word',50006),
(1003,'word',50007),
(1003,'word',50008),
(1003,'word',50009),
(1003,'word',50010),
(1003,'word',50011),
(1003,'word',50012),
(1003,'word',50013),
(1003,'word',50014),
(1003,'word',50015),
(1003,'word',50016),
(1003,'word',50017),
(1003,'word',50018),
(1003,'word',50019),
(1003,'word',50020),
(1003,'word',50021),
(1003,'word',50022),
(1003,'word',50023),
(1003,'word',50024),
(1003,'word',50025),
(1003,'word',50026),
(1003,'word',50027),
(1003,'word',50028),
(1003,'word',50029),
(1003,'word',50030);

COMMIT;

-- Add JLPT N5 Adverbs to JLPT N5 Adverbs Group

BEGIN TRANSACTION;

INSERT INTO group_items (group_id, item_type, item_id) VALUES
(1007,'word',50001),
(1007,'word',50002),
(1007,'word',50003),
(1007,'word',50004),
(1007,'word',50005),
(1007,'word',50006),
(1007,'word',50007),
(1007,'word',50008),
(1007,'word',50009),
(1007,'word',50010),
(1007,'word',50011),
(1007,'word',50012),
(1007,'word',50013),
(1007,'word',50014),
(1007,'word',50015),
(1007,'word',50016),
(1007,'word',50017),
(1007,'word',50018),
(1007,'word',50019),
(1007,'word',50020),
(1007,'word',50021),
(1007,'word',50022),
(1007,'word',50023),
(1007,'word',50024),
(1007,'word',50025),
(1007,'word',50026),
(1007,'word',50027),
(1007,'word',50028),
(1007,'word',50029),
(1007,'word',50030);

COMMIT;
