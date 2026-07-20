-- Origin Talent — Supabase schema for the two website forms
-- Run this in: Supabase Dashboard > SQL Editor > New query

create table if not exists public.client_enquiries (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text,
  company text,
  email text,
  mobile text,
  alt_phone text,
  contact_method text,
  address text,
  role text,
  employment_type text,
  arrangement text,
  hours text,
  urgency text,
  salary text,
  driving text,
  languages text,
  days text,
  duties text,
  notes text,
  popia boolean not null default false
);

create table if not exists public.candidate_applications (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text,
  dob text,
  id_number text,
  nationality text,
  address text,
  province text,
  mobile text,
  email text,
  kin_name text,
  kin_number text,
  role text,
  position_type text,
  licence text,
  transport text,
  availability text,
  skills text,
  quals text,
  languages text,
  legal text,
  able text,
  screening text,
  declare boolean not null default false,
  popia boolean not null default false
);

alter table public.client_enquiries enable row level security;
alter table public.candidate_applications enable row level security;

-- Public website visitors may INSERT (submit a form) but never read, edit or delete.
create policy "Public can submit client enquiries"
  on public.client_enquiries for insert
  to anon
  with check (true);

create policy "Public can submit candidate applications"
  on public.candidate_applications for insert
  to anon
  with check (true);
