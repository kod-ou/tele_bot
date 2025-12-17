/*
  # Telegram Bot Database Schema
  
  This migration creates the database schema for a Telegram group management bot.
  
  ## New Tables
  
  ### `user_warnings`
  Tracks warnings issued to users for posting unauthorized links.
  - `id` (uuid, primary key) - Unique identifier for each warning
  - `user_id` (bigint) - Telegram user ID
  - `chat_id` (bigint) - Telegram chat ID
  - `username` (text) - User's Telegram username
  - `warning_count` (integer) - Number of warnings issued
  - `last_warning_at` (timestamptz) - Timestamp of the last warning
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Record last update timestamp
  
  ### `scheduled_messages`
  Stores scheduled messages to be sent to groups.
  - `id` (uuid, primary key) - Unique identifier
  - `chat_id` (bigint) - Target Telegram chat ID
  - `message_text` (text) - The message content
  - `schedule_time` (text) - Time to send (format: "HH:MM")
  - `schedule_days` (text[]) - Days of week (e.g., ["monday", "friday"])
  - `is_active` (boolean) - Whether the schedule is active
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Record last update timestamp
  
  ### `motivational_quotes`
  Stores motivational quotes to be sent randomly.
  - `id` (uuid, primary key) - Unique identifier
  - `quote_text` (text) - The motivational quote
  - `author` (text) - Author of the quote (optional)
  - `is_active` (boolean) - Whether the quote is active
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### `group_settings`
  Stores settings for each Telegram group.
  - `id` (uuid, primary key) - Unique identifier
  - `chat_id` (bigint, unique) - Telegram chat ID
  - `chat_title` (text) - Group name
  - `welcome_message` (text) - Custom welcome message
  - `link_moderation_enabled` (boolean) - Enable/disable link moderation
  - `max_warnings` (integer) - Maximum warnings before kick
  - `quotes_enabled` (boolean) - Enable/disable motivational quotes
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Record last update timestamp
  
  ## Security
  
  - Enable RLS on all tables
  - Add policies for service role access (bot will use service role key)
*/

-- Create user_warnings table
CREATE TABLE IF NOT EXISTS user_warnings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id bigint NOT NULL,
  chat_id bigint NOT NULL,
  username text DEFAULT '',
  warning_count integer DEFAULT 1,
  last_warning_at timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_user_warnings_user_chat ON user_warnings(user_id, chat_id);

-- Create scheduled_messages table
CREATE TABLE IF NOT EXISTS scheduled_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  chat_id bigint NOT NULL,
  message_text text NOT NULL,
  schedule_time text NOT NULL,
  schedule_days text[] DEFAULT ARRAY[]::text[],
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_scheduled_messages_chat ON scheduled_messages(chat_id);

-- Create motivational_quotes table
CREATE TABLE IF NOT EXISTS motivational_quotes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  quote_text text NOT NULL,
  author text DEFAULT '',
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- Create group_settings table
CREATE TABLE IF NOT EXISTS group_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  chat_id bigint UNIQUE NOT NULL,
  chat_title text DEFAULT '',
  welcome_message text DEFAULT 'Selamat datang ke group! Sila patuhi peraturan group.',
  link_moderation_enabled boolean DEFAULT true,
  max_warnings integer DEFAULT 3,
  quotes_enabled boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_group_settings_chat ON group_settings(chat_id);

-- Enable Row Level Security
ALTER TABLE user_warnings ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE motivational_quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_settings ENABLE ROW LEVEL SECURITY;

-- Create policies for service role access (bot operations)
CREATE POLICY "Service role can manage user warnings"
  ON user_warnings
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Service role can manage scheduled messages"
  ON scheduled_messages
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Service role can manage motivational quotes"
  ON motivational_quotes
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Service role can manage group settings"
  ON group_settings
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Insert some default motivational quotes
INSERT INTO motivational_quotes (quote_text, author, is_active) VALUES
  ('Kejayaan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.', 'Colin Powell', true),
  ('Jangan tunggu peluang yang sempurna, ambil peluang dan jadikannya sempurna.', 'Unknown', true),
  ('Kegagalan adalah kesempatan untuk memulakan semula dengan lebih bijak.', 'Henry Ford', true),
  ('Anda tidak perlu menjadi hebat untuk memulakan, tetapi anda perlu memulakan untuk menjadi hebat.', 'Zig Ziglar', true),
  ('Setiap hari adalah kesempatan baru untuk mengubah hidup anda.', 'Unknown', true)
ON CONFLICT DO NOTHING;
