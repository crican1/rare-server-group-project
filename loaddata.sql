CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "content" varchar,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO `Users` VALUES (null, "Charles", "Bridgers", "mcmaster@gmail.com", "This is your favorite local hip-hop host!", "c4theexplosive", "password", 8/6/2022, False);
INSERT INTO `Users` VALUES (null, "Instructor", "Danny", "pythonnerd12@gmail.com", "Junior instructor for NSS!", "dantheman", "password", 6/12/2022, False);
INSERT INTO `Users` VALUES (null, "Angie", "Gonzalez", "eagleeyeangie@gmail.com", "Music theory and coding wiz!", "eagleeyeangie", "password", 2/4/2023, False);

DROP TABLE Users;
CREATE TABLE `Comment` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `author_id`    TEXT NOT NULL,
    `post_id`    TEXT NOT NULL,
    `content`    TEXT NOT NULL
);

INSERT INTO `Comment` VALUES (1, 1, 1, "This is a comment for a post.");
INSERT INTO `Comment` VALUES (2, 2, 2, "This is a comment for another post.");
INSERT INTO `Comment` VALUES (3, 3, 3, "This is a comment for yet another post.");

CREATE TABLE "Comments" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER NOT NULL,
  "author_id" INTEGER NOT NULL,
  "content" TEXT NOT NULL,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

INSERT INTO `Comments` VALUES (null, 1, 1, "This is a comment for a post.");
INSERT INTO `Comments` VALUES (2, 2, 2, "This is a comment for another post.");
INSERT INTO `Comments` VALUES (3, 3, 3, "This is a comment for yet another post.");


INSERT INTO `Posts` VALUES (1, 1, "Love Effects", "5/9/2023", "Love Makes Everything Better" );
INSERT INTO `Posts` VALUES (2, 2, "Hate Effects", "5/10/2023", "Hate Makes Everything Worst" );
INSERT INTO `Posts` VALUES (3, 3, "I Need Food", "5/11/2023", "Food Makes Everything Better" );
INSERT INTO `Posts` VALUES (4, 4, "I Adore Water", "5/12/2023", "Water Makes Everything Wetter" );

DROP TABLE `Posts`


INSERT INTO `Subscriptions` VALUES (null, 1, 3, CURRENT_DATE);
INSERT INTO `Subscriptions` VALUES (2, 2, 3, CURRENT_DATE);


SELECT
    p.id,
    p.user_id,
    p.title,
    p.publication_date,
    p.content,
    u.first_name user_first_name,
    u.last_name user_last_name,    
FROM Posts p
JOIN Users u
    ON u.id = p.user_id
