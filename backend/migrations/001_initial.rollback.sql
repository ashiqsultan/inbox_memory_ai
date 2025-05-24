-- Rollback for 001_initial.sql migration

-- Drop triggers first
DROP TRIGGER IF EXISTS update_updated_at_column ON emails;
DROP TRIGGER IF EXISTS update_updated_at_column ON users;

-- Drop the function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop tables in reverse order due to foreign key dependencies
DROP TABLE IF EXISTS question_answers;
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS users;
