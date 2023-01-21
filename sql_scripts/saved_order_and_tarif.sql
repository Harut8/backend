 --select timestamp '2005-04-02 12:00:00-07' + interval '1 month' 
create table saved_order_and_tarif( 
order_id SERIAL primary key,
order_summ money not null,
cass_stantion_count int not null,
mobile_cass_count int not null,
mobile_manager_count int not null,
web_manager_count int not null,
company_id int not null,
order_date timestamp default current_timestamp,
order_ending timestamp not null,
order_state bool not null default FALSE,
foreign key (company_id) references company(c_id)
)