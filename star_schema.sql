-- Group 17
--      92422 - André João De Almeida Avelar
--      92470 - Guilherme Baeta Campos da Rocha Fontes
--      92504 - José Francisco Giro Pinto Moreira

drop table d_time cascade;
drop table d_institution cascade;
drop table f_presc_sale cascade;
drop table f_analysis cascade;

create table d_time(
    id_time integer not null unique,
    day integer not null,
    week_day integer not null,
    week integer not null,
    month integer not null,
    trimester integer not null,
    year integer not null);


create table d_institution(
    id_inst integer not null unique,
    inst_name varchar(80) not null,
    inst_kind varchar(80) not null,
    region_num integer not null,
    county_num integer not null,
    constraint fk_dInstitution_institution
        foreign key(inst_name)
            references Institution(inst_name) on delete cascade on update cascade,
    constraint fk_dInstitution_region
        foreign key(region_num)
            references Region(region_num) on delete cascade on update cascade,
    constraint fk_dInstitution_county
        foreign key(county_num)
            references County(county_num) on delete cascade on update cascade);


create table f_presc_sale(
    id_presc_sale integer not null unique,
    id_doctor integer not null,
    patient_num integer not null,
    id_reg_date integer not null,
    id_inst integer not null,
    substance varchar(80) not null,
    subs_quant integer not null,
    constraint pk_f_presc_sale
          primary key(id_presc_sale),
    constraint fk_fpresc_sale_prescription_sale
          foreign key(id_presc_sale)
              references PrescriptionSale(sale_num) on delete cascade on update cascade,
    constraint fk_fpresc_sale_doctor
          foreign key(id_doctor)
              references Doctor(certificate_num) on delete cascade on update cascade,
    constraint fk_time
          foreign key(id_reg_date)
              references d_time(id_time) on delete cascade on update cascade,
    constraint fk_dInstitution
        foreign key(id_inst)
            references d_institution(id_inst) on delete cascade on update cascade);


create table f_analysis(
    id_analysis integer not null unique,
    id_doctor integer not null,
    patient_num integer not null,
    id_reg_date integer not null,
    id_inst integer not null,
    analysis_name varchar(80) not null,
    subs_quant integer not null,
    constraint pk_d_analise
          primary key(id_analysis),
    constraint fk_analysis
          foreign key(id_analysis)
              references Analysis(analysis_num) on delete cascade on update cascade,
    constraint fk_fanalysis_doctor
          foreign key(id_doctor)
              references Doctor(certificate_num) on delete cascade on update cascade,
    constraint fk_fanalysis_time
          foreign key(id_reg_date)
              references d_time(id_time) on delete cascade on update cascade,
    constraint fk_dInstitution
        foreign key(id_inst)
            references d_institution(id_inst) on delete cascade on update cascade);
