-- Origin Talent — tighten the public INSERT policies flagged by the
-- Supabase advisor (WITH CHECK (true) effectively bypasses RLS for anon).
-- Run this in: Supabase Dashboard > SQL Editor > New query

drop policy if exists "Public can submit candidate applications" on public.candidate_applications;
drop policy if exists "Public can submit client enquiries" on public.client_enquiries;

create policy "Public can submit candidate applications"
  on public.candidate_applications for insert
  to anon
  with check (
    coalesce(btrim(name), '') <> ''
    and coalesce(btrim(mobile), '') <> ''
    and declare is true
    and popia is true
    and length(coalesce(name, ''))       <= 200
    and length(coalesce(mobile, ''))     <= 50
    and length(coalesce(email, ''))      <= 200
    and length(coalesce(address, ''))    <= 500
    and length(coalesce(nationality, '')) <= 100
    and length(coalesce(province, ''))   <= 100
    and length(coalesce(kin_name, ''))   <= 200
    and length(coalesce(kin_number, '')) <= 50
    and length(coalesce(role, ''))       <= 100
    and length(coalesce(position_type, '')) <= 100
    and length(coalesce(licence, ''))    <= 100
    and length(coalesce(transport, ''))  <= 100
    and length(coalesce(availability, '')) <= 500
    and length(coalesce(skills, ''))     <= 4000
    and length(coalesce(quals, ''))      <= 4000
    and length(coalesce(languages, ''))  <= 500
    and length(coalesce(legal, ''))      <= 2000
    and length(coalesce(able, ''))       <= 2000
    and length(coalesce(screening, ''))  <= 500
  );

create policy "Public can submit client enquiries"
  on public.client_enquiries for insert
  to anon
  with check (
    coalesce(btrim(name), '') <> ''
    and coalesce(btrim(mobile), '') <> ''
    and popia is true
    and length(coalesce(name, ''))    <= 200
    and length(coalesce(company, '')) <= 200
    and length(coalesce(mobile, '')) <= 50
    and length(coalesce(alt_phone, '')) <= 50
    and length(coalesce(email, ''))  <= 200
    and length(coalesce(contact_method, '')) <= 100
    and length(coalesce(address, '')) <= 500
    and length(coalesce(role, ''))    <= 100
    and length(coalesce(employment_type, '')) <= 100
    and length(coalesce(arrangement, '')) <= 100
    and length(coalesce(hours, ''))   <= 100
    and length(coalesce(urgency, '')) <= 100
    and length(coalesce(salary, ''))  <= 100
    and length(coalesce(driving, '')) <= 100
    and length(coalesce(languages, '')) <= 500
    and length(coalesce(days, ''))    <= 200
    and length(coalesce(duties, '')) <= 4000
    and length(coalesce(notes, ''))  <= 4000
  );
