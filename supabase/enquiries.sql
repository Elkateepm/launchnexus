-- LaunchNexus — website enquiries
-- Run this in the Supabase SQL editor of whichever project hosts the site's data.
--
-- Security model: nothing in the browser touches this table. Enquiries arrive
-- through api/enquiry.js, which uses the service-role key server-side and so
-- bypasses RLS. There is therefore NO anon policy at all: RLS is enabled with
-- no policies, which denies every anon/authenticated request by default.
--
-- Do not add an anon insert policy. It would let anyone with the (public) anon
-- key write straight to this table, skipping the endpoint's validation,
-- honeypot, service allowlist and length limits.
--
-- Read enquiries in the Supabase dashboard, or later through an authenticated
-- admin view with its own policy.

create table if not exists public.enquiries (
  id            uuid primary key default gen_random_uuid(),
  name          text not null,
  organisation  text,
  email         text not null,
  service       text not null default 'Not sure yet',
  message       text not null,
  budget        text,
  target_date   date,
  status        text not null default 'New',
  created_at    timestamptz not null default now(),

  constraint enquiries_status_check
    check (status in ('New','Contacted','Discovery','Proposal','Won','Lost')),
  constraint enquiries_service_check
    check (service in ('Personalised CRM','Website','App','Not sure yet')),
  constraint enquiries_email_check
    check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  constraint enquiries_message_length
    check (char_length(message) between 1 and 5000),
  constraint enquiries_name_length
    check (char_length(name) between 1 and 200),
  constraint enquiries_organisation_length
    check (organisation is null or char_length(organisation) <= 200),
  constraint enquiries_email_length
    check (char_length(email) <= 320),
  constraint enquiries_budget_length
    check (budget is null or char_length(budget) <= 100)
);

create index if not exists enquiries_created_at_idx on public.enquiries (created_at desc);
create index if not exists enquiries_status_idx     on public.enquiries (status);

alter table public.enquiries enable row level security;

-- Deliberately no policies. RLS with zero policies denies all API access for
-- anon and authenticated roles. The service role used by api/enquiry.js
-- bypasses RLS, which is the only intended write path.
--
-- If an earlier version of this file was already run, remove the old policy:
drop policy if exists "anon can submit enquiries" on public.enquiries;

-- Force status to 'New' on insert so a submitter can't set their own pipeline stage.
create or replace function public.enquiries_force_new_status()
returns trigger language plpgsql as $$
begin
  new.status := 'New';
  new.created_at := now();
  return new;
end;
$$;

drop trigger if exists enquiries_force_new_status_trg on public.enquiries;
create trigger enquiries_force_new_status_trg
  before insert on public.enquiries
  for each row execute function public.enquiries_force_new_status();
