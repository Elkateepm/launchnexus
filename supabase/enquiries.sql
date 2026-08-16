-- LaunchNexus — website enquiries
-- Run this in the Supabase SQL editor of whichever project hosts the site's data.
--
-- Security model: the anon key is public (it ships in the page), so the table is
-- INSERT-only for anon and readable by nobody through the API. Read enquiries in
-- the Supabase dashboard, or later through an authenticated admin view.

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
    check (char_length(name) between 1 and 200)
);

create index if not exists enquiries_created_at_idx on public.enquiries (created_at desc);
create index if not exists enquiries_status_idx     on public.enquiries (status);

alter table public.enquiries enable row level security;

-- Anyone may submit an enquiry...
drop policy if exists "anon can submit enquiries" on public.enquiries;
create policy "anon can submit enquiries"
  on public.enquiries for insert
  to anon
  with check (true);

-- ...and nobody may read, update or delete through the API.
-- (No select/update/delete policies exist, so RLS denies them by default.)

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
