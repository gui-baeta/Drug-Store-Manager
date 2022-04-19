-- 1

select doc_speciality, month, year, count(analysis_name)
from (
    f_analysis f inner join Doctor d on f.id_doctor=d.certificate_num
) c inner join d_time t on c.id_reg_date=t.id_time
where year between 2017 and 2020 and analysis_name = 'glicémia'
GROUP BY GROUPING SETS(doc_speciality, month, year);


-- 2

select week_day, month, county_num, sum(subs_quant), round(avg(subs_quant), 3) as avg
from (
    (f_presc_sale s inner join d_institution i on s.id_inst=i.id_inst) c
        inner join Region r on c.region_num=r.region_num
) d
inner join d_time t on d.id_reg_date=t.id_time
    where region_name = 'Lisboa' and month between 1 and 4 and year = '2020'
    group by rollup(county_num, week_day, month);
