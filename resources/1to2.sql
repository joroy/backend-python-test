-- Migration script Task1ToTask2

-- INTEGER because no boolean in sqlite
ALTER TABLE todos ADD COLUMN done INTEGER DEFAULT 0;