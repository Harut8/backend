/* Get company info from temp
 * using temp id
 * generate random unique id for company table 
 * insert these information */
DROP function del_tmp_add_company;
drop type temp_table_info;
drop type unique_and_email;
create type temp_table_info as (
t_c_name text,
		   t_c_pass text,
		   t_c_contact_name text,
		   t_c_phone text,
		   t_c_email text,
		   t_c_inn text,
		   t_c_kpp text,
		   t_c_k_schet text,
		   t_c_r_schet text,
		   t_c_bik text,
		   t_c_bank_name text,
		   t_c_address text
);
create type unique_and_email as (
c_unique_id text,
c_email text);
CREATE OR REPLACE FUNCTION del_tmp_add_company(temp_id int)
returns unique_and_email
language plpgsql
AS $$
DECLARE
temp_info temp_table_info;
res_data unique_and_email;
rand_id int;
find_id int;
check_point bool:= false;
diller_id int:=1;
BEGIN 
	--SELECT d_id INTO diller_id FROM diller WHERE d_name = 'EKey';
	/* try to get diller_id for adding to the company table  */
	if diller_id is null then
		return 'ERROR';
	end if;
	select t_c_name,
		   t_c_pass,
		   t_c_contact_name,
		   t_c_phone,
		   t_c_email,
		   t_c_inn,
		   t_c_kpp,
		   t_c_k_schet,
		   t_c_r_schet,
		   t_c_bik,
		   t_c_bank_name,
		   t_c_address
	into temp_info
	FROM temp_company WHERE t_id = temp_id;
	--FAILED GETTING INFO/ WRONG temp_id
	IF temp_info.t_c_name IS NULL THEN
	select null,null into res_data;
		RETURN res_data;
	END IF;
	--END 
	WHILE not check_point LOOP
		/* generate random id for company user*/
		SELECT floor(random()* (10000000-99999999 + 1) + 99999999) into rand_id;
		SELECT c_id INTO find_id FROM company WHERE c_id = rand_id;--TRY GENERATE AND CHECK ARE THERE similar ID
		
		IF find_id IS NULL THEN
			INSERT INTO company(c_unique_id,
						c_diller_id,
						c_name,
						c_pass,
						c_contact_name,
						c_phone,
						c_email,
						c_inn,
						c_kpp,
						c_k_schet,
						c_r_schet,
						c_bik,
						c_bank_name,
						c_address)
			VALUES(rand_id, 1 ,temp_info.*);
			delete from temp_company where t_id  = temp_id;
		select c_unique_id, c_email into res_data from company where c_unique_id = rand_id;
			check_point := true;
		end if;
		
	END LOOP;
if res_data.c_email is null then
 select null,null into res_data;
else
return res_data;
end if;
END;
$$
