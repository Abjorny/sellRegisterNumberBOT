import aiosqlite

class Database:
    _instance = None

    def __new__(cls, db_file):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_file = db_file
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance

    async def connect(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_file)
            self.cursor = await self.connection.cursor()

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.cursor = None

    async def add_user(self, userid, firstname, lastname):
        user = await self.get_user_userid(userid)
        if user is None:
            await self.cursor.execute("INSERT INTO users (userid,firstname,lastname) VALUES (?,?,?)", (userid,firstname,lastname))
            await self.connection.commit()
            user = await self.get_user_userid(userid)
        return user
        
    async def get_user_userid(self, userid):
        await self.cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,))
        return await self.cursor.fetchone()
    
    async def get_users(self):
        await self.cursor.execute("SELECT * FROM users")
        return await self.cursor.fetchall()
    
    async def get_admins(self):
        await self.cursor.execute("SELECT * FROM users WHERE role ='admin'")
        return await self.cursor.fetchall()
    async def get_users_moderations(self):
        await self.cursor.execute("SELECT * FROM users WHERE role ='moderation'")
        return await self.cursor.fetchall()
    async def set_user_data(self, userid, key, value):
        await self.cursor.execute(
            f"UPDATE users SET {key} = ? WHERE userid = ?", (value, userid)
        )
        await self.connection.commit()
    
    async def set_order_data(self, ids ,key, value ):
        await self.cursor.execute(f"UPDATE orders SET {key} = ? WHERE id = ?",(value,ids))
        await self.connection.commit() 
        
    async def add_order(self, userid, url, number, comment, price, photo = None):
        await self.cursor.execute("INSERT INTO orders (userid, url, number, comment, price, photo) VALUES (?,?,?,?,?,?)", (userid, url, number, comment, price, photo))
        order_id = self.cursor.lastrowid  
        await self.connection.commit()
        return order_id 
    
    async def get_all_orders_userid(self, userid):
        await self.cursor.execute("SELECT * FROM orders where userid = ?",(userid,))
        return await self.cursor.fetchall()
    
    async def get_all_orders(self):
        await self.cursor.execute("SELECT * FROM orders")
        return await self.cursor.fetchall()
    async def get_all_orders_active(self):
        await self.cursor.execute("SELECT * FROM orders where status = 'active'")
        return await self.cursor.fetchall()
    
    async def get_all_orders_moderation(self):
        await self.cursor.execute("SELECT * FROM orders where status = 'moderation'")
        return await self.cursor.fetchall()
    async def get_order_id(self, ids):
        await self.cursor.execute("SELECT * FROM orders where id = ?",(ids,))
        return await self.cursor.fetchone()
    
    async def delete_order_id(self, ids):
        await self.cursor.execute("DELETE FROM orders WHERE id = ?", (int(ids),))
        await self.connection.commit()
    
    async def set_settings_data(self ,key, value ):
        await self.cursor.execute(f"UPDATE settings SET {key} = ? WHERE id = 0",(value,))
        await self.connection.commit()
        
    async def get_settings(self, key):
        await self.cursor.execute(f"SELECT {key} FROM settings where id = 0")
        return await self.cursor.fetchone()

    async def add_archive(self, text, userid):
        await self.cursor.execute("INSERT INTO archive (text, userid) VALUES (?, ?)", (text, userid))
        order_id = self.cursor.lastrowid  
        await self.connection.commit()
        return order_id 