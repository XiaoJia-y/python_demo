import MySQLdb
class Save_data(object):

    def insert_data(self, conn, data):        
        cursor = conn.cursor()
        for i in data:
            sql = """insert into 
            trip_data (name, href, price, agree, people, about)
            values ('{name}', '{href}', '{price}', '{agree}', '{people}', '{about}')
            """.format(name = i[0], href = i[1], price = i[2], agree = i[3], people = i[4], about = i[5])
            cursor.execute(sql)
        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    conn = MySQLdb.Connect(host = "42.193.255.161", port = 3306, user = 'root', passwd = '123456', db = 'trip', charset="utf8")
    s = Save_data()
    data = [['南澳+汕头4日自由行·|1晚南澳岛酒店+2晚汕头酒店|"美食&海岛"热气牛肉垂涎·凉爽鱼生惹人馋·错峰海岛悠闲度假·海鲜吃到爽！', 'https://vacations.ctrip.com/travel/detail/p1021829619/?city=', '￥1270起', '', '累计9人出游', '']]
    print(len(data))
    #data = ['汕头4日自由行·"潮汕美食"|2晚汕头酒店+1晚南澳岛酒店|错峰出游·热气牛肉·美味人间·吃货朝圣之旅！', 'https://vacations.ctrip.com/travel/detail/p1021590844/?city=', '￥1272起', '', '累计10人出游', '']
    s.insert_data(conn, data)



