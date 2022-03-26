DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS Drive;
DROP TABLE IF EXISTS Play;

CREATE TABLE Game (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    home_name   VARCHAR (25) NOT NULL,
    away_name   VARCHAR (25) NOT NULL,
    home_abbr   VARCHAR (10) NOT NULL,
    away_abbr   VARCHAR (10) NOT NULL,
    home_score  INTEGER NOT NULL,
    away_score  INTEGER NOT NULL,
    score_diff  INTEGER NOT NULL,
    won_toss    VARCHAR (10),
    winner_choice    VARCHAR (25),
    loser_choice     VARCHAR (25),
    open_kick   VARCHAR (10)
);

CREATE TABLE Drive (
    id     		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    game_id   	INTEGER NOT NULL,
    home_score  INTEGER NOT NULL,
    away_score  INTEGER NOT NULL,
    score_diff  INTEGER NOT NULL,
    home_tol    INTEGER NOT NULL,
    away_tol    INTEGER NOT NULL,
    q_start     BOOLEAN,
    h_start     BOOLEAN,
    quarter     INTEGER NOT NULL,
    time_remaining    INTEGER,
    possession  VARCHAR (10) NOT NULL,
    series      INTEGER NOT NULL,
    num_plays   INTEGER,
    total_yards INTEGER,
    time_elapsed_sec    INTEGER,
    drive_end   VARCHAR (25),
    FOREIGN KEY (game_id) REFERENCES Game(id)
);

CREATE TABLE Play (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    game_id    	INTEGER NOT NULL,
    drive_id   	INTEGER NOT NULL,
    play_num	INTEGER NOT NULL,
	home_score  INTEGER NOT NULL,
    away_score  INTEGER NOT NULL,
    score_diff  INTEGER NOT NULL,
    home_tol    INTEGER NOT NULL,
    away_tol    INTEGER NOT NULL,
    quarter    	INTEGER NOT NULL,
    time_remaining    INTEGER,
    possession  VARCHAR (10) NOT NULL,
    series_num	INTEGER NOT NULL,
	down    	INTEGER NOT NULL,
    distance    INTEGER NOT NULL,
    yard_line   INTEGER NOT NULL,
	gain_loss   INTEGER,
    FOREIGN KEY (game_id) REFERENCES Game(id),
    FOREIGN KEY (drive_id) REFERENCES Drive(id)
);