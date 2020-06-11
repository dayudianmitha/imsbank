import pymysql
import time

time.sleep(1)
print("=== ENGINE INTEGRASI TOKO DENGAN BANK ===")
while (1):
    connection_to_toko = 1
    try:
        connToko = pymysql.connect(host='localhost', user='root', passwd='', db='db_toko')
        curToko = connToko.cursor()
    except:
        print("can't connect to TOKO")
        connection_to_toko = 0

    try:
        connBank = pymysql.connect(host='localhost', user='root', passwd='', db='db_bankk')
        curBank = connBank.cursor()
    except:
        print("can't connect to BANK")


    sql_select = "SELECT * FROM tb_invoice"
    curBank.execute(sql_select)
    invoice = curBank.fetchall()

    sql_select = "SELECT * FROM tb_integrasi"
    curBank.execute(sql_select)
    integrasi = curBank.fetchall()

    print("invoice = %d | integrasi = %d" % (len(invoice), len(integrasi)))

#update
    if (invoice != integrasi):
        print("-- UPDATE DETECTED --")
        for data in invoice:
            for dataIntegrasi in integrasi:
                if (data[0] == dataIntegrasi[0]):
                    if (data != dataIntegrasi):
                        val = (data[1], data[2], data[0])
                        update_integrasi_bank = "update tb_integrasi set total_transaksi = %s, status = %s where id_invoice = %s"
                        curBank.execute(update_integrasi_bank, val)
                        connBank.commit()

                        if (connection_to_toko == 1):
                            update_integrasi_toko = "update tb_integrasi set total_transaksi = %s, status = %s where id_invoice = %s"
                            curToko.execute(update_integrasi_toko, val)
                            connToko.commit()

                            update_transaksi_toko = "update tb_invoice set total_transaksi = %s, status = %s where id_invoice = %s"
                            curToko.execute(update_transaksi_toko, val)
                            connToko.commit()