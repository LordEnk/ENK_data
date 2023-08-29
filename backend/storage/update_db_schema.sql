-- Update the User table to add reset_token and reset_token_expiration columns
ALTER TABLE user
ADD COLUMN reset_token TEXT;

ALTER TABLE user
ADD COLUMN reset_token_expiration DATETIME;

