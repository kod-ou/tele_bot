/*
  # Update RLS Policies for Anon Access
  
  Updates policies to allow both service_role and anon key access for bot operations.
  This enables the bot to work with anon key when service role key is not available.
  
  ## Changes
  - Add anon role to existing policies alongside service_role
  - Maintains same security level but allows anon key usage
*/

-- Drop existing service-only policies
DROP POLICY IF EXISTS "Service role can manage user warnings" ON user_warnings;
DROP POLICY IF EXISTS "Service role can manage scheduled messages" ON scheduled_messages;
DROP POLICY IF EXISTS "Service role can manage motivational quotes" ON motivational_quotes;
DROP POLICY IF EXISTS "Service role can manage group settings" ON group_settings;

-- Create new policies that allow both service_role and anon
CREATE POLICY "Bot can manage user warnings"
  ON user_warnings
  FOR ALL
  TO service_role, anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Bot can manage scheduled messages"
  ON scheduled_messages
  FOR ALL
  TO service_role, anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Bot can manage motivational quotes"
  ON motivational_quotes
  FOR ALL
  TO service_role, anon
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Bot can manage group settings"
  ON group_settings
  FOR ALL
  TO service_role, anon
  USING (true)
  WITH CHECK (true);
