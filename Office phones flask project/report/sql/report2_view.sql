select rep_id, pay_id, surname, rep_phone, p_summ from report_unpaid_exc
where pay_month=$rep_month and pay_year=$rep_year