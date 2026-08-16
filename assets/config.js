/* LaunchNexus — front-end configuration.
   Fill these in to store enquiries in Supabase. While they are empty the
   enquiry form falls back to opening the visitor's email client.

   The anon key is safe to expose ONLY if the enquiries table has RLS enabled
   with an insert-only policy for the anon role and no select policy.
   See supabase/enquiries.sql in this repo. */
window.LNX_CONFIG = {
  supabaseUrl: '',
  supabaseAnonKey: ''
};
