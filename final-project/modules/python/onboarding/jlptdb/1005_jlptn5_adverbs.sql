-- JLPT N5 Adverb Import Script

BEGIN TRANSACTION;

INSERT INTO words (word_level, japanese, kana, romaji, english) VALUES
('N5', 'ちょっと', 'ちょっと', 'chotto', 'a little'),
('N5', '丁度', 'ちょうど', 'choudo', 'exactly'),
('N5', 'だんだん', 'だんだん', 'dandan', 'gradually'),
('N5', 'どう', 'どう', 'dou', 'in what way'),
('N5', 'どうも', 'どうも', 'doumo', 'thank you'),
('N5', 'どうして', 'どうして', 'doushite', 'why'),
('N5', 'どうぞ', 'どうぞ', 'douzo', 'please'),
('N5', '初めて', 'はじめて', 'hajimete', 'for the first time'),
('N5', 'いかが', 'いかが', 'ikaga', 'how about'),
('N5', 'いくら', 'いくら', 'ikura', 'how much'),
('N5', 'いくつ', 'いくつ', 'ikutsu', 'how many'),
('N5', '色々', 'いろいろ', 'iroiro', 'various'),
('N5', '一緒に', 'いっしょに', 'isshoni', 'together'),
('N5', 'いつも', 'いつも', 'itsumo', 'always'),
('N5', '結構', 'けっこう', 'kekkou', 'splendid'),
('N5', 'まだ', 'まだ', 'mada', 'not yet'),
('N5', '前に', 'まえに', 'maeni', 'before'),
('N5', '真っ直ぐ', 'まっすぐ', 'massugu', 'straight ahead'),
('N5', 'もっと', 'もっと', 'motto', 'more'),
('N5', 'もう', 'もう', 'mou', 'already'),
('N5', '何故', 'なぜ', 'naze', 'why'),
('N5', '同じ', 'おなじ', 'onaji', 'same'),
('N5', '直ぐに', 'すぐに', 'suguni', 'immediately'),
('N5', '少し', 'すこし', 'sukoshi', 'a little bit'),
('N5', '多分', 'たぶん', 'tabun', 'probably'),
('N5', '大変', 'たいへん', 'taihen', 'very'),
('N5', '時々', 'ときどき', 'tokidoki', 'sometimes'),
('N5', 'とても', 'とても', 'totemo', 'very'),
('N5', 'よく', 'よく', 'yoku', 'often'),
('N5', 'ゆっくり', 'ゆっくり', 'yukkuri', 'slowly');

COMMIT;
