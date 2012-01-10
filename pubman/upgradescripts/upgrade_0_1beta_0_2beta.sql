BEGIN TRANSACTION;

DROP TABLE IF EXISTS "pubman_video";
DROP TABLE IF EXISTS "pubman_caption";
DROP TABLE IF EXISTS "pubman_image_caption";
DROP TABLE IF EXISTS "pubman_image";
DROP TABLE IF EXISTS "pubman_mediaobject_video_files";
DROP TABLE IF EXISTS "pubman_mediaobject_images";
DROP INDEX IF EXISTS "pubman_mediaobject_2d21bb22";

CREATE TABLE  "pubman_video" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "video_file" varchar(100) NOT NULL,
    "html_type_attribute" varchar(200) NOT NULL
);

CREATE TABLE "pubman_caption" (
    "id" integer NOT NULL PRIMARY KEY,
    "text" varchar(200) NOT NULL,
    "language" varchar(7) NOT NULL,
    "date_last_edited" datetime NOT NULL
)
;
CREATE TABLE "pubman_image_captions" (
    "id" integer NOT NULL PRIMARY KEY,
    "image_id" integer NOT NULL,
    "caption_id" integer NOT NULL REFERENCES "pubman_caption" ("id"),
    UNIQUE ("image_id", "caption_id")
)
;
CREATE TABLE "pubman_image" (
    "id" integer NOT NULL PRIMARY KEY,
    "image" varchar(100) NOT NULL,
    "date_last_edited" datetime NOT NULL
)
;

CREATE TABLE  "pubman_mediaobject_video_files" (
    "id" integer NOT NULL PRIMARY KEY,
    "mediaobject_id" integer NOT NULL,
    "video_id" integer NOT NULL REFERENCES "pubman_video" ("id"),
    UNIQUE ("mediaobject_id", "video_id")
);

CREATE TABLE "pubman_mediaobject_images" (
    "id" integer NOT NULL PRIMARY KEY,
    "mediaobject_id" integer NOT NULL,
    "image_id" integer NOT NULL REFERENCES "pubman_image" ("id"),
    UNIQUE ("mediaobject_id", "image_id")
)
;

CREATE TABLE "pubman_mediaobject_captions" (
    "id" integer NOT NULL PRIMARY KEY,
    "mediaobject_id" integer NOT NULL,
    "caption_id" integer NOT NULL REFERENCES "pubman_caption" ("id"),
    UNIQUE ("mediaobject_id", "caption_id")
)
;



ALTER TABLE  "pubman_mediaobject" RENAME TO "pubman_mediaobject_backup";

CREATE TABLE  "pubman_mediaobject" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "subtitle" varchar(200) NOT NULL,
    "date_published" datetime,
    "publication_stage" varchar(1) NOT NULL,
    "slug" varchar(200) NOT NULL UNIQUE,
    "copyright_id" integer REFERENCES "pubman_copyright" ("id"),
    "date_last_edited" datetime NOT NULL,
    "notes" text NOT NULL,
    "tags" varchar(255) NOT NULL,
    "media_type" varchar(2) NOT NULL,
    "preload" varchar(2) NOT NULL,
    "embedded" text NOT NULL,
    "date_captured" datetime
);

CREATE INDEX  "pubman_mediaobject_2d21bb22" ON "pubman_mediaobject" ("copyright_id");


INSERT INTO "pubman_caption" 
("id", "text", "language", "date_last_edited")
SELECT "id", "caption", 'en', "date_last_edited" FROM "pubman_mediaobject_backup";

INSERT INTO "pubman_image_caption" 
("id", "image_id", "caption_id")
SELECT "id", "id", "id" FROM "pubman_mediaobject_backup";   

INSERT INTO "pubman_image" 
("id", "image", "date_last_edited")
SELECT "id", "local_image", "date_last_edited" FROM "pubman_mediaobject_backup";

INSERT INTO "pubman_mediaobject_images" 
("id","mediaobject_id","image_id" )
SELECT "id", "id", "id" FROM "pubman_mediaobject_backup";

INSERT INTO "pubman_mediaobject" 
("id", "title",  "subtitle", "date_published", "publication_stage", "slug", "copyright_id", "date_last_edited", 
"notes", "tags", "media_type", "preload", "embedded", "date_captured")
SELECT "id", "title", "subtitle", "date_published", "publication_stage", "slug", "copyright_id", "date_last_edited",
"notes", "tags", "media_type", 'D', '', "date_captured" FROM "pubman_mediaobject_backup";

DROP TABLE "pubman_mediaobject_backup";

ALTER TABLE "main"."pubman_article" RENAME TO "oXHFcGcd04oXHFcGcd04_pubman_article";
CREATE TABLE "main"."pubman_article" ("id" integer PRIMARY KEY  NOT NULL ,"title" varchar(200) NOT NULL ,"subtitle" varchar(200) NOT NULL ,"date_published" datetime,"publication_stage" varchar(1) NOT NULL ,"slug" varchar(200) NOT NULL ,"copyright_id" integer,"date_last_edited" datetime NOT NULL ,"notes" text NOT NULL ,"tags" varchar(255) NOT NULL ,"date_originally_published" date,"purpose_of_edit" text NOT NULL ,"primary_media_object_id" integer,"blurb" text NOT NULL ,"article_text" text NOT NULL ,"primary_pullout_quote" varchar(200) NOT NULL ,"text_format" varchar(1) NOT NULL ,"page_break_strategy" varchar(2) NOT NULL ,"complexity" varchar(1) NOT NULL ,"language" varchar(7) NOT NULL ,"frontpage" bool NOT NULL ,"sticky" bool NOT NULL ,"comments_allowed" bool NOT NULL ,"subscription_required" bool NOT NULL );
INSERT INTO "main"."pubman_article" SELECT "id","title","subtitle","date_published","publication_stage","slug","copyright_id","date_last_edited","notes","tags","date_originally_published","purpose_of_edit","primary_media_object_id","blurb","article_text","primary_pullout_quote","text_format","page_break_strategy","complexity","language","frontpage","sticky","comments_allowed","subscription_required" FROM "main"."oXHFcGcd04oXHFcGcd04_pubman_article";
DROP TABLE "main"."oXHFcGcd04oXHFcGcd04_pubman_article";

ALTER TABLE "main"."pubman_translation" RENAME TO "oXHFcGcd04oXHFcGcd04_pubman_translation";
CREATE TABLE "main"."pubman_translation" ("id" integer PRIMARY KEY  NOT NULL ,"title" varchar(200) NOT NULL ,"subtitle" varchar(200) NOT NULL ,"date_published" datetime,"publication_stage" varchar(1) NOT NULL ,"slug" varchar(200) NOT NULL ,"copyright_id" integer,"date_last_edited" datetime NOT NULL ,"notes" text NOT NULL ,"tags" varchar(255) NOT NULL ,"article_id" integer NOT NULL ,"language" varchar(7) NOT NULL ,"blurb" text NOT NULL ,"article_text" text NOT NULL ,"text_format" varchar(1) NOT NULL ,"primary_pullout_quote" varchar(200) NOT NULL );
INSERT INTO "main"."pubman_translation" SELECT "id","title","subtitle","date_published","publication_stage","slug","copyright_id","date_last_edited","notes","tags","article_id","language","blurb","article_text","text_format","primary_pullout_quote" FROM "main"."oXHFcGcd04oXHFcGcd04_pubman_translation";
DROP TABLE "main"."oXHFcGcd04oXHFcGcd04_pubman_translation";


END TRANSACTION;
