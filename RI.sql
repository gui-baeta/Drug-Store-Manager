/*Regra de Integridade nº1 - ri_100*/

create or replace function ri100() returns
  trigger as $$
  declare i integer;
  begin
  select count(*) into i
      from Appointment
      where certificate_num=new.certificate_num and
      institution_name=new.institution_name and
      extract(week from appo_date)=extract(week from new.appo_date);
    if i > 100 then
      raise exception 'Doctor #% exceded number of appointments this week.',new.certificate_num
      using hint = 'Nao pode dar mais consultas nesta instituicao ate ao final da semana';
    end if;
    return new;
  end;
$$ language plpgsql;

drop trigger if exists ri100_update on Appointment;
drop trigger if exists ri100_insert on Appointment;

create trigger ri100_update before update on Appointment for each row execute procedure ri100();
create trigger ri100_insert before insert on Appointment for each row execute procedure ri100();


/*Regra de Integridade nº2 - ri_análise*/


create or replace function rianalise() returns
  trigger as $$
  declare s varchar(80);
  begin
  select doc_speciality into s
  from Doctor
  where certificate_num=new.certificate_num;

  if not(s=new.analysis_speciality) then
    raise exception 'Specialitys dont match.'
    using hint = 'It must be another doctor with the right speciality';
  end if;
  return new;
  end;
$$ language plpgsql;

drop trigger if exists rianalise_update on Analysis;
drop trigger if exists rianalise_insert on Analysis;

create trigger rianalise_update before update on Analysis for each row execute procedure rianalise();
create trigger rianalise_insert before insert on Analysis for each row execute procedure rianalise();
