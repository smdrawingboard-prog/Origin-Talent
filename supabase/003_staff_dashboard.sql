-- Origin Talent — staff dashboard schema
-- Adds pipeline tracking + a staff directory on top of the existing
-- client_enquiries / candidate_applications tables, and opens read/update
-- access to authenticated staff (the public anon insert-only policies from
-- 001_init.sql / 002_tighten_rls.sql are untouched).
-- Run this in: Supabase Dashboard > SQL Editor > New query (after 001, 002)

-- ---------------------------------------------------------------------
-- Staff directory
-- ---------------------------------------------------------------------
create table if not exists public.staff (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null,
  email text not null,
  role text not null default 'consultant', -- 'admin' | 'consultant'
  active boolean not null default true,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------
-- Helper functions (security definer so RLS policies can check staff
-- membership without recursing back through the staff table's own RLS)
-- ---------------------------------------------------------------------
create or replace function public.is_active_staff()
returns boolean
language sql
security definer
set search_path = public
stable
as $$
  select exists (
    select 1 from public.staff s
    where s.id = auth.uid() and s.active
  );
$$;

create or replace function public.is_admin_staff()
returns boolean
language sql
security definer
set search_path = public
stable
as $$
  select exists (
    select 1 from public.staff s
    where s.id = auth.uid() and s.active and s.role = 'admin'
  );
$$;

-- ---------------------------------------------------------------------
-- Pipeline tracking columns
-- ---------------------------------------------------------------------
alter table public.client_enquiries
  add column if not exists stage text not null default 'New Enquiry',
  add column if not exists assigned_staff_id uuid references public.staff(id) on delete set null,
  add column if not exists stage_updated_at timestamptz not null default now(),
  add column if not exists internal_notes text;

alter table public.candidate_applications
  add column if not exists stage text not null default 'New Application',
  add column if not exists assigned_staff_id uuid references public.staff(id) on delete set null,
  add column if not exists stage_updated_at timestamptz not null default now(),
  add column if not exists internal_notes text;

-- Bump stage_updated_at automatically whenever stage changes, so the
-- dashboard's "days in stage" ageing indicator is accurate without the
-- client having to set it manually.
create or replace function public.set_stage_updated_at()
returns trigger
language plpgsql
as $$
begin
  if new.stage is distinct from old.stage then
    new.stage_updated_at = now();
  end if;
  return new;
end;
$$;

drop trigger if exists trg_client_enquiries_stage on public.client_enquiries;
create trigger trg_client_enquiries_stage
  before update on public.client_enquiries
  for each row execute function public.set_stage_updated_at();

drop trigger if exists trg_candidate_applications_stage on public.candidate_applications;
create trigger trg_candidate_applications_stage
  before update on public.candidate_applications
  for each row execute function public.set_stage_updated_at();

-- ---------------------------------------------------------------------
-- RLS: staff (authenticated) can read/update; only admins can delete.
-- Public anon insert-only policies already exist from 001/002 and are
-- untouched by this migration.
-- ---------------------------------------------------------------------
create policy "Staff can view client enquiries"
  on public.client_enquiries for select
  to authenticated
  using (public.is_active_staff());

create policy "Staff can update client enquiries"
  on public.client_enquiries for update
  to authenticated
  using (public.is_active_staff())
  with check (public.is_active_staff());

create policy "Admins can delete client enquiries"
  on public.client_enquiries for delete
  to authenticated
  using (public.is_admin_staff());

create policy "Staff can view candidate applications"
  on public.candidate_applications for select
  to authenticated
  using (public.is_active_staff());

create policy "Staff can update candidate applications"
  on public.candidate_applications for update
  to authenticated
  using (public.is_active_staff())
  with check (public.is_active_staff());

create policy "Admins can delete candidate applications"
  on public.candidate_applications for delete
  to authenticated
  using (public.is_admin_staff());

alter table public.staff enable row level security;

create policy "Staff can view the staff directory"
  on public.staff for select
  to authenticated
  using (public.is_active_staff());

create policy "Admins can manage staff"
  on public.staff for all
  to authenticated
  using (public.is_admin_staff())
  with check (public.is_admin_staff());

-- ---------------------------------------------------------------------
-- Bootstrapping the first admin
-- ---------------------------------------------------------------------
-- The policies above are circular by design (you need an active admin row
-- to create staff rows), which is fine because the SQL Editor runs as the
-- Postgres owner and bypasses RLS entirely. To create the first admin:
--   1. Supabase Dashboard > Authentication > Users > Add user (set email
--      + password, or send an invite).
--   2. Copy that user's UID.
--   3. Run, still in the SQL Editor:
--        insert into public.staff (id, full_name, email, role)
--        values ('<uid>', 'Full Name', 'person@origintalent.co.za', 'admin');
-- Every staff member after that can be added the same way (role
-- 'consultant' for non-admins), or by an admin from within the dashboard's
-- Staff panel using the Supabase Auth invite flow.
