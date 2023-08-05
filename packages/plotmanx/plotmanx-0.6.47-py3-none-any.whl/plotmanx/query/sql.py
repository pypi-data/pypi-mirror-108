import itertools
import json
import sqlite3
from datetime import datetime

from ..configuration import get_db_path


def txtBlock(s: any) -> str:
    if s:
        return str(s)
    else:
        return ""

def txtJson(s: any)->str:
    return json.dumps(s)



def commaInt(x: str) -> int:
    return int(x.replace(',', ''))


class SQLX:
    def __init__(self):
        self.con = sqlite3.connect(get_db_path())
        self.cur = self.con.cursor()

    def end(self):
        self.con.commit()
        self.con.close()

    def schema_plan(self):

        self.cur.execute('''CREATE TABLE IF NOT EXISTS nodeInfo (
        
                                   
                                   tid INTEGER PRIMARY KEY AUTOINCREMENT,
                                   host text NOT NULL,
                                   
                                   
                                   tmp_plots INTEGER NOT NULL,
                                   mv_channels INTEGER NOT NULL,
                                   cpu_count INTEGER NOT NULL,
                                   cpu_percent REAL NOT NULL,
                                   bucket_sum_t REAL NOT NULL,
                                   bucket_count INTEGER NOT NULL,
                                   
                                   swap_percent REAL NOT NULL,
                                   disk_percent_block text NOT NULL,
                                   io_nvme_block text NOT NULL,
                                   io_list_plmo text NOT NULL,
                                   io_list_nfs text NOT NULL,
                                   io_read_issues INTEGER NOT NULL,
                                   
                                   memory_percent REAL NOT NULL,
                                                                      
                                   net_read_gb_s REAL NOT NULL,
                                   net_write_gb_s REAL NOT NULL,
                                   disk_read_gb_s REAL NOT NULL,
                                   disk_write_gb_s REAL NOT NULL,

                                   net_fds INTEGER NOT NULL,
                                   version text NOT NULL,
                                   chia_ver text NOT NULL,
                                   timen INTEGER NOT NULL
                                   
                                
                           );''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS plotv2 (
                           pcid INTEGER PRIMARY KEY AUTOINCREMENT,
                           plotid text NOT NULL,
                           k INTEGER NOT NULL,
                           r INTEGER NOT NULL,
                           b INTEGER NOT NULL,
                           u INTEGER NOT NULL,
                           pid INTEGER NOT NULL,
                           progress REAL NOT NULL,
                           phase text NOT NULL,
                           host text NOT NULL,
                           freeze text NOT NULL,
                           readerr text NOT NULL,
                           wroteerr text NOT NULL,
                           time INTEGER NOT NULL
                   );''')
    """
    host name as return
    """
    def datainput(self, j: dict, ts: int) -> str:
        host = txtBlock(j['identity'])
        if len(j['jobls']) > 0:

            try:
                for h in j['jobls']:

                    plot_id = h['plot_id']

                    content_find = f"""

                    SELECT COUNT(*) FROM plotv2 WHERE plotid='{plot_id}';
                    """

                    (n,) = self.cur.execute(content_find).fetchone()

                    if int(n) == 0:
                        content_insert = f"""
                       INSERT INTO plotv2 (
                            plotid, k, r, b, u, pid, 
                            progress, phase,
                            freeze,readerr,wroteerr,
                            host, time)
                            VALUES (
                            '{plot_id}', {int(h['k'])}, {int(h['r'])}, {int(h['b'])}, {int(h['u'])}, {int(h['pid'])}, 
                            {float(h['progress'])}, '{txtBlock(h['phase'])}',
                            '{txtBlock(h['freeze'])}','{txtBlock(h['readerr'])}','{txtBlock(h['wroteerr'])}',
                            '{host}', {ts}
                            )
                           ;
                        """

                        self.cur.execute(content_insert)

                        print(f"ID - {plot_id}")
                    else:
                        content_update = f"""
                        UPDATE plotv2

                            SET time={ts},
                            progress={float(h['progress'])},
                            phase='{txtBlock(h['phase'])}',
                            freeze='{txtBlock(h['freeze'])}',
                            readerr='{txtBlock(h['readerr'])}',
                            wroteerr='{txtBlock(h['wroteerr'])}'

                        WHERE plotid='{plot_id}'
                        ;
                        """
                        self.cur.execute(content_update)

            except sqlite3.OperationalError as r:
                print(f"there is a things that doesnt work on - job. {r}")
        else:
            print("body is not empty")

        try:

            print(j)
            content_insert = f"""
            INSERT INTO nodeInfo (

                host,tmp_plots,mv_channels,cpu_count,cpu_percent,bucket_sum_t,bucket_count,swap_percent,

                disk_percent_block,io_nvme_block,io_list_plmo,io_list_nfs,io_read_issues,

                memory_percent,net_read_gb_s,net_write_gb_s,disk_read_gb_s,disk_write_gb_s,

                version,chia_ver,

                timen

            ) VALUES(

                '{host}',
                {int(j['plotcount'])},
                {int(j['movingcount'])},
                {int(j['cpucount'])},
                {float(j['cpu_percent'])},
                {float(j['sizet'])},
                {float(j['historyplots'])},
                {float(j['swap_percent'])},

                '{txtJson(j['disk_info'])}',
                '{txtJson(j['disk_nvme_io'])}',
                '{txtJson(j['movingdetail'])}',
                '{txtJson(j['nfsips'])}',
                {int(j['io_read_issues'])},

                {float(j['memory_percent'])},
                {float(j['net_read_mb_s'])},
                {float(j['net_write_mb_s'])},
                {float(j['disk_read_mb_s'])},
                {float(j['disk_write_mb_s'])},
                
                '{txtBlock(j['version'])}',
                '{txtBlock(j['chia_ver'])}',
                {int(datetime.now().timestamp())}
            )
            """

            self.cur.execute(content_insert)

        except sqlite3.OperationalError as r:
            print(f"there is a things that doesnt work - machine. {r}")

        return host

    def getNodes(self) -> list:
        block = """
        SELECT * FROM nodeInfo GROUP BY host ORDER BY timen DESC
        """

        listd = self.cur.execute(block).fetchall()

        """for company, orders_iter in itertools.groupby(listd, key=lambda r: r[0]):
            orders = list(orders_iter)
            total_qty = sum(order[2] for order in orders)"""



        return listd
