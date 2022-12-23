/* Get company info from temp
 * using temp id
 * generate random unique id for company table 
 * insert these information */
DROP function del_tmp_add_company;
drop type temp_table_info;
create type temp_table_info as (
t_c_name text,
		   t_c_pass varchar(20),
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
CREATE OR REPLACE FUNCTION del_tmp_add_company(temp_id int)
returns text
language plpgsql
AS $$
DECLARE
x temp_table_info;
rand_id int;
find_id int;
check_point bool:= false;
diller_id int:=1;
BEGIN 
	--SELECT d_id INTO diller_id FROM diller WHERE d_name = 'EKey';
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
	into x
	FROM temp_company WHERE t_id = temp_id;
	IF x.t_c_name IS NULL THEN
		RETURN 'ERROR';
	END IF;
	WHILE not check_point LOOP
		SELECT floor(random()* (10000000-99999999 + 1) + 99999999) into rand_id;
		SELECT c_id INTO find_id FROM company WHERE c_id = rand_id;
	
		IF find_id IS NULL THEN
			INSERT INTO company(c_unique_id,
						c_diller_id,
						c_pass,
						c_name,
						c_contacname,
						c_phone,
						c_email,
						c_inn,
						c_kpp,
						c_k_schet,
						c_r_schet,
						c_bik,
						c_bank_name,
						c_address)
			VALUES(rand_id, 1 ,x.*);
			check_point := true;
		end if;
		
	END LOOP;
		
return 'success';
END;
$$
