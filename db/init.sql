
-- ==========================================
-- PicSphere Database Schema
-- PostgreSQL
-- ==================================


-- 1. Users Table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    bio TEXT,
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- 2. Posts Table
CREATE TABLE IF NOT EXISTS post (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    caption TEXT,
    image_path VARCHAR(500) NOT NULL
        CHECK (LENGTH(TRIM(image_path)) > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Comments Table
CREATE TABLE IF NOT EXISTS comment (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    commenter_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES post(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 4. Like Tracker
CREATE TABLE IF NOT EXISTS liketracker (
    liker_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES post(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (liker_id, post_id)
);


-- 5. User Follows
CREATE TABLE IF NOT EXISTS userfollow (
    follower_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    followed_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followed_id),

    CONSTRAINT prevent_self_follow
        CHECK (follower_id != followed_id)
);


-- ==========================================
-- 6. Indexes for Query Optimization
-- ==========================================


-- User Indexes
CREATE INDEX IF NOT EXISTS ix_user_username
ON "user"(username);


CREATE INDEX IF NOT EXISTS ix_user_email
ON "user"(email);


-- Post Indexes
CREATE INDEX IF NOT EXISTS ix_post_user_id
ON post(user_id);


CREATE INDEX IF NOT EXISTS ix_post_created_at
ON post(created_at DESC);


CREATE INDEX IF NOT EXISTS ix_post_user_created
ON post(user_id, created_at DESC);


-- Comment Indexes
CREATE INDEX IF NOT EXISTS ix_comment_post_id
ON comment(post_id);


CREATE INDEX IF NOT EXISTS ix_comment_commenter_id
ON comment(commenter_id);


CREATE INDEX IF NOT EXISTS ix_comment_post_created
ON comment(post_id, created_at DESC);


-- Like Indexes
CREATE INDEX IF NOT EXISTS ix_liketracker_post_id
ON liketracker(post_id);


-- Follow Indexes
CREATE INDEX IF NOT EXISTS ix_userfollow_followed
ON userfollow(followed_id);


-- ==========================================
-- DATABASE INITIALIZATION COMPLETE
-- ==========================================
