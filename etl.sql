
-- d_time

insert into d_time(id_time, day, week_day, week, month, trimester, year)
    select distinct row_number() over (order by _date) as id_time, extract (day from _date) as day, extract(isodow from _date) as week_day, extract(week from _date) as week, extract (month from _date) as month, extract (quarter from _date) as trimester,extract (year from _date) as year from (
        (select distinct presc_date as _date from PrescriptionSale)
        union
        (select distinct reg_date as _date from Analysis)) table1;


-- d_institution

insert into d_institution(id_inst, inst_name, inst_kind, region_num, county_num)
    select row_number() over (order by inst_name, inst_kind, region_num, county_num) id_inst, * from Institution;


-- f_presc_sale

insert into f_presc_sale(id_presc_sale, id_doctor, patient_num, id_reg_date, id_inst, substance, subs_quant)
    select distinct sale_num as id_presc_sale, certificate_num as id_doctor, patient_num, id_time as id_reg_date, id_inst, substance, subs_quant from (
        with a as (
            with c as (
                select a.sale_num, certificate_num, a.patient_num, presc_date, inst_name, a.substance, subs_quant from PrescriptionSale a inner join PharmacySale b
                on a.sale_num=b.sale_num
            )
            select d.id_inst, c.sale_num, c.certificate_num, c.patient_num, c.presc_date, c.substance, c.subs_quant from c inner join d_institution d on c.inst_name=d.inst_name
        )
        select * from a inner join d_time t
            on extract(year from a.presc_date)=t.year
                and extract(month from a.presc_date)=t.month
                and extract(day from a.presc_date)=t.day
    ) z;


-- f_analysis

insert into f_analysis(id_analysis, id_doctor, patient_num, id_reg_date, id_inst, analysis_name, subs_quant)
    select analysis_num as id_analysis, certificate_num as id_doctor, patient_num, id_time as id_reg_date, id_inst, analysis_name, subs_quant from (
        with c as (
            with a as (
                select analysis_num, certificate_num, patient_num, reg_date, institution_name, analysis_name, subs_quant from Analysis
            )
            select d.id_inst, a.analysis_num, a.certificate_num, a.patient_num, a.reg_date, a.analysis_name,a.subs_quant from a inner join d_institution d on a.institution_name=d.inst_name
        )
        select * from c inner join d_time t
        on extract(year from c.reg_date)=t.year
            and extract(month from c.reg_date)=t.month
            and extract(day from c.reg_date)=t.day
    ) z;
