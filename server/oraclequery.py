#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import cx_Oracle

con = cx_Oracle.connect('iqms/zeigler17@iqora')
cur = con.cursor()
sql = """
      SELECT a.itemno
      FROM v_rt_workorders v left outer join arinvt a
      ON v.standard_id = a.standard_id
      WHERE v.workorder_id = '9997394'
      """

# print(sql)
cur.execute(sql)

for result in cur:
    print(result)

cur.close()
con.close()
