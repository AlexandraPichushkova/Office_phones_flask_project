select min_kol, gb_kol, sms_kol from
tariffs t join occ o on t.t_id=o.tar_id join worker w on o.phone_numb=w.phone_numb
where worker_id=$user_id